from distutils.core import setup


setup(
    name="pandasserializer",
    packages=["pandas_serializer"],
    version="0.0.1",
    license="MIT",
    description="Pandas Serializer is a powerful and flexible toolkit for building JSON structures based on data represented in a two-dimensional data structure.",
    author="Eduardo Ventura Izquierdo Nuñez",
    author_email="in.eduardo.v@outlook.com",
    url="https://github.com/dot-tostring/pandas_serializer",
    keywords=["pandas", "serializer"],
    install_requires=[
        "pandas",
    ],
)
