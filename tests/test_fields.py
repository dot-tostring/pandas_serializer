from pytest import raises

from pandas_serializer.fields import Field, NestField, GroupField, NestGroupField
from pandas_serializer.exceptions import GroupFieldActionException


class TestField:
    def test_default(self):
        field = Field()

        assert field.source is None
        assert not field.unique
        assert not field.hidden

    def test_source_must_return_it(self):
        source = "source"
        assert Field(source=source).source == source

    def test_unique_must_return_it(self):
        assert Field(unique=True).unique

    def test_hidden_must_return_it(self):
        assert Field(hidden=True).hidden


class TestNestField:
    def test_serializer_must_return_it(self):
        assert not NestField(serializer=None).serializer


class TestGroupField:
    def test_group_must_return_it(self):
        function = list
        field = GroupField(function=function)
        assert field.group["function"]["callable"] == function
        assert not len(field.group["function"]["arguments"])
        assert not field.group["drop_duplicates"]

    def test_group_max_must_set_arguments(self):
        assert "default" in GroupField(function=max).group["function"]["arguments"]

    def test_group_min_must_set_arguments(self):
        assert "default" in GroupField(function=min).group["function"]["arguments"]

    def test_group_invalid_function_must_raise_exception(self):
        with raises(GroupFieldActionException):
            GroupField(function=None)

    def test_group_drop_duplicates_must_set_it(self):
        assert GroupField(function=list, drop_duplicates=True).group["drop_duplicates"]


class TestNestGroupField:
    def test_default(self):
        field = NestGroupField(serializer=None)
        assert not field.serializer
        assert field.group["function"]["callable"] == list
        assert not len(field.group["function"]["arguments"])
        assert not field.group["drop_duplicates"]
