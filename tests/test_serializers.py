from pytest import fixture, raises
from pandas import DataFrame

from pandas_serializer.serializers import DataFrameSerializer
from pandas_serializer.fields import Field, NestField, GroupField, NestGroupField
from pandas_serializer.exceptions import (
    GroupFieldUniqueException,
    DataFrameSourceException,
)


class TestDataFrameSerializer:
    @fixture
    def catalogue(self):
        return DataFrame(
            {
                "a": [1, 1, 2, 2, 3],
                "b": [4, 4, 5, 5, 6],
                "c": [1, 2, 1, 2, 2],
                "d": [1, 1, 1, 2, 3],
            }
        )

    def test_dataframe_other_than_dataframe_must_raise_exception(self):
        with raises(DataFrameSourceException):
            DataFrameSerializer(dataframe=None)

    def test_end_to_end_field_must_represent_it(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field()

        assert Serializer(catalogue).represent() == [
            {"a": 1},
            {"a": 1},
            {"a": 2},
            {"a": 2},
            {"a": 3},
        ]

    def test_end_to_end_field_source_must_rename_it(self, catalogue):
        class Serializer(DataFrameSerializer):
            A = Field(source="a")

        assert Serializer(catalogue).represent() == [
            {"A": 1},
            {"A": 1},
            {"A": 2},
            {"A": 2},
            {"A": 3},
        ]

    def test_end_to_end_field_unique_must_drop_duplicates(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field(unique=True)

        assert Serializer(catalogue).represent() == [
            {"a": 1},
            {"a": 2},
            {"a": 3},
        ]

    def test_end_to_end_field_multiple_unique_must_check_them_together(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field(unique=True)
            c = Field(unique=True)

        assert Serializer(catalogue).represent() == [
            {"a": 1, "c": 1},
            {"a": 1, "c": 2},
            {"a": 2, "c": 1},
            {"a": 2, "c": 2},
            {"a": 3, "c": 2},
        ]

    def test_end_to_end_field_hidden_must_hide_it(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field(hidden=True)
            b = Field()

        assert Serializer(catalogue).represent() == [
            {"b": 4},
            {"b": 4},
            {"b": 5},
            {"b": 5},
            {"b": 6},
        ]

    def test_end_to_end_nestfield_must_represent_it(self, catalogue):
        class SerializerB(DataFrameSerializer):
            b = Field()

        class SerializerA(DataFrameSerializer):
            a = Field()
            n = NestField(SerializerB)

        assert SerializerA(catalogue).represent() == [
            {"a": 1, "n": {"b": 4}},
            {"a": 1, "n": {"b": 4}},
            {"a": 2, "n": {"b": 5}},
            {"a": 2, "n": {"b": 5}},
            {"a": 3, "n": {"b": 6}},
        ]

    def test_end_to_end_groupfield_must_represent_it(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field(unique=True)
            c = GroupField(function=list)

        assert Serializer(catalogue).represent() == [
            {"a": 1, "c": [1, 2]},
            {"a": 2, "c": [1, 2]},
            {"a": 3, "c": [2]},
        ]

    def test_end_to_end_groupfield_drop_duplicates_must_drop_duplicates(
        self, catalogue
    ):
        class Serializer(DataFrameSerializer):
            a = Field(unique=True)
            d = GroupField(function=list, drop_duplicates=True)

        assert Serializer(catalogue).represent() == [
            {"a": 1, "d": [1]},
            {"a": 2, "d": [1, 2]},
            {"a": 3, "d": [3]},
        ]

    def test_end_to_end_groupfield_without_unique_must_raise_exception(self, catalogue):
        class Serializer(DataFrameSerializer):
            a = Field()
            d = GroupField(function=list)

        with raises(GroupFieldUniqueException):
            Serializer(catalogue).represent()

    def test_end_to_end_nestgroupfield_must_represente_it(self, catalogue):
        class SerializerB(DataFrameSerializer):
            c = Field()

        class SerializerA(DataFrameSerializer):
            a = Field(unique=True)
            ng = NestGroupField(serializer=SerializerB)

        assert SerializerA(catalogue).represent() == [
            {"a": 1, "ng": [{"c": 1}, {"c": 2}]},
            {"a": 2, "ng": [{"c": 1}, {"c": 2}]},
            {"a": 3, "ng": [{"c": 2}]},
        ]

    def test_end_to_end_nestgroupfield_drop_duplicates_must_drop_duplicates(
        self, catalogue
    ):
        class SerializerB(DataFrameSerializer):
            d = Field()

        class SerializerA(DataFrameSerializer):
            a = Field(unique=True)
            ng = NestGroupField(serializer=SerializerB, drop_duplicates=True)

        assert SerializerA(catalogue).represent() == [
            {"a": 1, "ng": [{"d": 1}]},
            {"a": 2, "ng": [{"d": 1}, {"d": 2}]},
            {"a": 3, "ng": [{"d": 3}]},
        ]

    def test_end_to_end_nestgroupfield_without_unique_must_raise_exception(
        self, catalogue
    ):
        class SerializerB(DataFrameSerializer):
            d = Field()

        class SerializerA(DataFrameSerializer):
            a = Field()
            ng = NestGroupField(serializer=SerializerB)

        with raises(GroupFieldUniqueException):
            SerializerA(catalogue).represent()
