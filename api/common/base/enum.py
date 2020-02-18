from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def all_key_value_str(self) -> str:
        return BaseEnum.key_value_str(list(self))

    @classmethod
    def key_value_str(cls, selected_enumlist) -> str:
        return "\n".join(['{} ￫ {}'.format(enum.value, enum.name) for enum in selected_enumlist])

    def list_of_values(self) -> list:
        return list(map(int, self))

    def __str__(self):
        return self.value
