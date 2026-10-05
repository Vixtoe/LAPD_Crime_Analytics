import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

@pytest.fixture(scope="module")
def spark():
    session = SparkSession.builder \
        .appName("ETL_Unit_Tests") \
        .master("local[1]") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
        .getOrCreate()
    yield session
    session.stop()

def test_non_physical_crime_filter(spark):
    schema = StructType([
        StructField("AREA NAME", StringType(), True),
        StructField("Crm Cd Desc", StringType(), True)
    ])
    data = [("Central", "ROBBERY"), ("Hollywood", "THEFT OF IDENTITY")]
    df = spark.createDataFrame(data, schema)
    filtered_df = df.filter(~F.col("Crm Cd Desc").isin(["THEFT OF IDENTITY"]))
    results = [row["Crm Cd Desc"] for row in filtered_df.collect()]
    assert "THEFT OF IDENTITY" not in results
    assert "ROBBERY" in results
