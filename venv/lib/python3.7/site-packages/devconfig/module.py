from importlib.abc import FileLoader
from types import ModuleType
import weakref as weak
import logging
import sys
from functools import wraps
from importlib import import_module
from itertools import chain
import io
import devconfig

_log = logging.getLogger(__name__)

PREPEND = {}
def strip_spec(spec, fields=()):
    return dict(((k,(v if not hasattr(v, '__dict__') else weak.ref(v)))
                                            for (k,v) in vars(spec).items()
                                            if not k in fields
                                            and not isinstance(v, (bool, type(None)))))

class YAMLFileLoader(FileLoader):
    def create_module(self, spec):
        return  ModuleType(spec.name)

    def exec_module(self, module):
        origin = module.__spec__.origin
        with open(origin, 'r') as source:
            for document in chain(devconfig.documents(PREPEND.get(origin, io.StringIO())), devconfig.documents(source)):
                _log.debug(f'{module.__spec__.name}', extra=strip_spec(module.__spec__, fields=('name', )))
                document.loader.module = {
                    'package': module.__package__,
                    'spec': strip_spec(module.__spec__)
                }
                module.__dict__.update(document.loader.construct_document(document))

    def get_filename(self, fullname):
        return os.path.basename(fullname)

    def get_source(fullname):
        return 'notimplemented'
