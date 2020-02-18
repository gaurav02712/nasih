import os
import sys
from functools import partial as _partial, lru_cache
import importlib._bootstrap_external
from importlib.util import find_spec
from importlib import invalidate_caches, import_module
import logging
import locale
from pathlib import Path
from operator import attrgetter
from contextlib import contextmanager
import yaml
import yaml.nodes
import yaml.constructor
import yaml.resolver
import attr
import devconfig
import devconfig.merge

import pkg_resources

ConstructorError = yaml.constructor.ConstructorError

_log = logging.getLogger(__name__)

def invocation_args(loader, node, deep=False):
    def _kwargs():
        return (), loader.construct_mapping(node, deep=deep)

    def _args():
        return loader.construct_sequence(node, deep=deep), {}

    def _singlearg():
        return (loader.construct_scalar(node),), {}

    casemap = {yaml.nodes.SequenceNode: _args,
               yaml.nodes.MappingNode: _kwargs,
               yaml.nodes.ScalarNode: _singlearg}

    return casemap[type(node)]()


def imported(loader, node, module='builtins', attribute=None, safe=False):
    try:
        if not safe:
            module = import_module(module)
        elif not module in sys.modules:
            raise ConstructorError(f'Unable to safely obtain {module} since it not yet imported')
        else:
            module = sys.modules[module]
    except:
        raise ConstructorError("while constructing a Python object", node.start_mark)
    if attribute:
        return attrgetter(attribute)(module)
    else:
        return module

def partial(loader, node, **kwargs):
    _callable = imported(loader, node, **kwargs)
    args, kwargs = invocation_args(loader, node)
    return _partial(_callable, *args, **kwargs)

def invoked(loader, node, **kwargs):
    _callable = imported(loader, node, **kwargs)
    args, kwargs = invocation_args(loader, node, deep=True)
    return _callable(*args, **kwargs)


UNDEFINED = object()
def envvar(loader, node, varname=UNDEFINED, default=UNDEFINED, converter=UNDEFINED):
    assert varname is not UNDEFINED
    getenv = _partial(os.environ.get, str(varname))
    if isinstance(node, yaml.nodes.MappingNode):
        declaration = loader.construct_mapping(node)
        converter = declaration.get('converter', converter)
        default = declaration.get('default', default)

    envvar = getenv() if default is UNDEFINED else getenv(default)
    if isinstance(envvar, str):
        envvar = yaml.load(envvar, Loader=yaml.Loader)
    return converter(envvar) if converter is not UNDEFINED else envvar


def yaml_file_finder(cls, extensions):
    current_loaders = importlib._bootstrap_external._get_supported_file_loaders()
    current_loaders.append((cls, extensions))
    sys.path_hooks[-1] = importlib.machinery.FileFinder.path_hook(*current_loaders)
    invalidate_caches()
    for name in [name for name in sys.path_importer_cache]:
        del sys.path_importer_cache[name]

IMPLICIT_RESOLVER = {}

def implicit_resolver(loader, node, name='_'):
    resolver = loader.construct_mapping(node, deep=True)
    if name == '_':
        loader.add_implicit_resolver(**resolver)
    else:
        IMPLICIT_RESOLVER_SETS[name] = resolver
    return resolver


KIND = {
    'mapping': dict,
    'sequence': list,
    'scalar': str,
    None: None,
    '': None
}

@attr.s
class PathObject:
    tag = attr.ib(converter=lambda value: value.lstrip('.'))
    kind = attr.ib(default=None)

@attr.s
class PathResolver:
    object = attr.ib(default=[])
    node = attr.ib(default=[])
    @classmethod
    def construct(cls, loader, _node):
        if _node.tag.startswith('!resolver:'):
            return loader.construct_object(_node)
        assert isinstance(_node, yaml.nodes.MappingNode), 'PathResolver configuration should be a mapping'
        object = []
        node = []
        merged = []
        for node_check_key_yaml_node, node_check_value_yaml_node in _node.value:
            node_check_key = loader.construct_scalar(node_check_key_yaml_node)
            if node_check_key.startswith('.'):
                node_check_value = loader.construct_scalar(node_check_value_yaml_node)
                object.append(PathObject(node_check_key, KIND[node_check_value]))
            elif node_check_key.startswith('~'):
                loader.construct_object(node_check_value_yaml_node)
            elif node_check_key in KIND:
                for index_check_key_yaml_node, index_check_value_yaml_node in node_check_value_yaml_node.value:
                    index_check_key = loader.construct_object(index_check_key_yaml_node)
                    node.append(((KIND[node_check_key], index_check_key), cls.construct(loader, index_check_value_yaml_node)))
            elif node_check_key == '<<':
                merged.append(loader.construct_object(node_check_value_yaml_node))
            else:
                raise ConstructorError(f'PathResolver keys should either start with ["." | "~" | "<<"] or be in range {KIND.keys()}')
        for merge in merged:
            object.extend(merge.object)
            node.extend(merge.node)
        return cls(object, node)

    def __call__(self):
        for path_object in self.object:
            yield (), path_object

        for subpath, subresolver in self.node:
            for suffix, path_object in subresolver():
                yield (subpath,) + suffix, path_object

PATH_RESOLVER = {}

def set_path_resolver(loader, node, name='_'):
    resolver = PathResolver.construct(loader, node)
    if name == '_':
        append_path_resolvers(loader, resolver)
    else:
        PATH_RESOLVER[name] = resolver

def append_path_resolvers(loader, resolver):
    for path, path_object in resolver():
        loader.add_path_resolver(path_object.tag, path, kind=path_object.kind)

def get_path_resolver(loader, node, name='_'):
    return PATH_RESOLVER[name]


STRJOIN_MAPPING_JOINER = {
    'values': lambda m, d: m.values(),
    'keys': lambda m, d: m.keys(),
    'items': lambda m, d: ( d.join(item) for item in d.items() )
}

def strjoin(loader, node, delimiter='', joining='values', subjoiner=''):
    assert joining in STRJOIN_MAPPING_JOINER
    args, kwargs = invocation_args(loader, node)
    mapjoiner = STRJOIN_MAPPING_JOINER(joining)
    return delimiter.join(args) + delimiter.join(mapjoiner(kwargs, subjoiner))


def path(loader, node, root=''):
    assert not isinstance(node, yaml.nodes.MappingNode)
    _path = Path(root)
    items, _ = invocation_args(loader, node, deep=True)
    for item in items:
        _path = _path / item
    return _path


def dir(loader, node, create=False, exist_ok=False, root=''):
    _path = path(loader, node, root=root)
    @contextmanager
    def _dir():
        _current = Path(root).resolve()
        if create:
            os.makedirs(_path, exist_ok=exist_ok)
        os.chdir(_path)
        try:
            yield _path
        finally:
            os.chdir(_current)
    return _dir


def asset(loader, node, package=UNDEFINED, abspath=True):
    if package is UNDEFINED:
        package = loader.module['package']

    _root = Path(pkg_resources.resource_filename(package, ''))
    if abspath:
        _root = _root.resolve()

    return path(loader, node, root=_root)


def file_contents(loader, node, root='', coding=locale.getpreferredencoding(False)):
    _path = path(loader, node, root=root)

    with io.open(_path, encoding=coding) as file_contents:
        return file_contents.read()