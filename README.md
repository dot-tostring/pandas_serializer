# Pandas Serializer

Pandas Serializer is a powerful and flexible toolkit for building JSON structures based on data represented in a two-dimensional data structure such as Pandas DataFrame.

Structures are defined by using **serializers** to represent objects and **fields** to represent data.

## Installation

Install using `pip`.
```
pip install pandasserializer
```

## Serializers

Serializers are responsible for transforming a dataset into a JSON structure based on the fields declared.

###### DataFrameSerializer

Pandas DataFrame serializer.

> Required

* __dataframe__: Source.

## Fields

Fields are responsible for representing the data according to the defined configuration.

###### Field

It represents the data as is.

> Opcional

* __source__: Identifies the column name.
* __unique__: It is considered unique for the representation.
* __hidden__: It is not displayed in the representation.

###### GroupField

It represents the data performing aggregation operations based on unique fields.

> Required

* __function__: Aggregation function.

> Opcional

* __source__: Identifies the column name.
* __drop_duplicates__: It drops duplicates in the aggregation.

###### NestField

It nests a representation based on the same data source.

> Required

* __serializer__: Serializer class.

###### NestGroupField

It is a combination of **GroupField** and **NestField**.

> Required

* __serializer__: Serializer class.

> Opcional

* __drop_duplicates__: It drops duplicates in the aggregation.

## Example

Let's take a look at a quick example of using DataFrameSerializer.

In these examples, the data represented are based on the following data source:

|produt_id|product_name|store_id|store_name|stock|
|:---|:---|:---|:---|:---|
|1|product_1|1|store_1|5|
|1|product_1|2|store_2|10|
|2|product_2|1|store_1|5|
|2|product_2|2|store_2|15|
|3|product_3|1|store_1|5|

###### Example: List products per store

```python
from pandas_serializer.serializers import DataFrameSerializer
from pandas_serializer.fields import Field, GroupField, NestGroupField

class ProductSerializer(DataFrameSerializer):
	name = Field(source="product_name")
	stock = Field()
	
class StoreSerializer(DataFrameSerializer):
	id = Field(source="store_id", unique=True, hidden=True)
	name = Field(source="store_name")
	products_total = GroupField(sum, source="stock")
	products = NestGroupField(ProductSerializer)

StoreSerializer(dataframe).represent()

"""Expected
[
	{
        "name": "store_1",
        "products_total": 15,
        "products": [
            {"name": "product_1", "stock": 5},
            {"name": "product_2", "stock": 5},
            {"name": "product_3", "stock": 5},
        ],
    },
    {
        "name": "store_2",
        "products_total": 25,
        "products": [
            {"name": "product_1", "stock": 10},
            {"name": "product_2", "stock": 15},
        ],
    },
]
"""
```
