import os
import glob
import pandas as pd
import kagglehub
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

NO_SCENE_CRIMES = ['THEFT OF IDENTITY', 'COUNTERFEIT', 'EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)']

def main():
    dataset_dir = kagglehub.dataset_download("samithsachidanandan/crime-data-from-2020-to-present")
    csv_path = glob.glob(os.path.join(dataset_dir, "*.csv"))[0]
    spark = SparkSession.builder.appName("LAPD_Crime_ETL").getOrCreate()
    df = spark.read.csv(csv_path, header=True, inferSchema=False)
    filtered = df.filter(~F.col("Crm Cd Desc").isin(NO_SCENE_CRIMES))
    # Additional ETL processing...
    print("ETL execution complete.")

if __name__ == "__main__":
    main()
