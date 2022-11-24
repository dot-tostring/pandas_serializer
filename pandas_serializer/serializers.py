from pandas import DataFrame
from pandas import merge

from pandas_serializer.exceptions import (
    FieldSourceException,
    GroupFieldUniqueException,
    DataFrameSourceException,
)
from pandas_serializer.fields import NestField, GroupField, NestGroupField


class DataFrameSerializer:
    def __init__(self, dataframe: DataFrame):
        if not isinstance(dataframe, DataFrame):
            raise DataFrameSourceException(
                "It seems that the data source is not Pandas DataFrame."
            )

        self.__dataframe = dataframe

    def __fields_mapping(self) -> tuple:
        dataframe = self.__dataframe.copy()
        fields, nested_fields, grouped_fields, unique_fields, hidden_fields = (
            dict(),
            dict(),
            list(),
            list(),
            list(),
        )

        for name in self.__dir__():
            if (
                not name.startswith("_")
                and name not in NestField.__dict__.keys()
                and not callable(getattr(self, name))
            ):
                instance = getattr(self, name)

                if isinstance(instance, GroupField):
                    grouped_fields.append({"name": name, **instance.group})

                if isinstance(instance, NestField) or isinstance(
                    instance, NestGroupField
                ):
                    nested_fields[name] = instance.serializer(dataframe)

                else:
                    fields[name] = instance

                if instance.source:
                    if name in self.__dataframe.columns:
                        raise FieldSourceException(
                            f'Field "{name}" already exists in the data source.'
                        )

                    self.__dataframe[name] = self.__dataframe[instance.source]

                if instance.unique:
                    unique_fields.append(name)

                if instance.hidden:
                    hidden_fields.append(name)

        return fields, nested_fields, grouped_fields, unique_fields, hidden_fields

    def __fields_grouping(self, groups: list, uniques: list = []) -> None:
        if groups and not uniques:
            raise GroupFieldUniqueException(
                "At least one field defined as unique is required for grouping."
            )

        for group in groups:
            name = group["name"]
            function = group["function"]

            self.__dataframe = merge(
                self.__dataframe.drop(name, axis=1),
                (
                    self.__dataframe.loc[
                        self.__dataframe[[*uniques, name]]
                        .astype("string")
                        .drop_duplicates()
                        .index
                    ]
                    if group["drop_duplicates"]
                    else self.__dataframe
                )
                .groupby(uniques)[name]
                .agg(
                    lambda x: function["callable"](
                        x[x.notna()], **function["arguments"]
                    )
                ),
                on=uniques,
            )

    def __fields_review(self, items: list) -> list:
        for item in items:
            if any(item.values()):
                return items

        return None

    def represent(self, master: bool = True):
        (
            fields,
            nested_fields,
            grouped_fields,
            unique_fields,
            hidden_fields,
        ) = self.__fields_mapping()

        for name, instance in nested_fields.items():
            self.__dataframe[name] = instance.represent(master=False)

        self.__fields_grouping(grouped_fields, unique_fields)

        if master:
            self.__dataframe = self.__dataframe.loc[
                (self.__dataframe[unique_fields] if unique_fields else self.__dataframe)
                .astype("string")
                .drop_duplicates()
                .index
            ]

        self.__dataframe = self.__dataframe[
            [*list(set(fields.keys()) - set(hidden_fields)), *nested_fields.keys()]
        ]

        return self.__fields_review(self.__dataframe.to_dict(orient="records"))
