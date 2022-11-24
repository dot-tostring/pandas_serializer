class FieldException(Exception):
    ...


class FieldSourceException(FieldException):
    ...


class GroupFieldActionException(FieldException):
    ...


class GroupFieldUniqueException(FieldException):
    ...


class SerializerException(Exception):
    ...


class DataFrameSourceException(SerializerException):
    ...
