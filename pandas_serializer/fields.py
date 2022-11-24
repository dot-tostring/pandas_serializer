from pandas_serializer.exceptions import GroupFieldActionException


class Field:
    def __init__(self, source: str = None, unique: bool = False, hidden: bool = False):
        self.__source = source
        self.__unique = unique
        self.__hidden = hidden

    @property
    def source(self):
        return self.__source

    @property
    def unique(self):
        return self.__unique

    @property
    def hidden(self):
        return self.__hidden


class NestField(Field):
    def __init__(self, serializer):
        Field.__init__(self)
        self.__serializer = serializer

    @property
    def serializer(self):
        return self.__serializer


class GroupField(Field):
    def __init__(
        self,
        function,
        drop_duplicates: bool = False,
        source: str = None,
    ):
        super().__init__(source)

        if function not in [sum, max, min, list]:
            raise GroupFieldActionException(
                "Invalid grouping action. Please use: sum, max, min or list."
            )

        self.__group = {
            "function": {
                "callable": function,
                "arguments": {"default": None} if function in [max, min] else {},
            },
            "drop_duplicates": drop_duplicates,
        }

    @property
    def group(self):
        return self.__group


class NestGroupField(NestField, GroupField):
    def __init__(self, serializer, drop_duplicates: bool = False):
        super().__init__(serializer)
        super(NestField, self).__init__(list, drop_duplicates)
