"""Optional Spark version of the daily aggregation.

Run with PySpark installed:
    spark-submit scripts/spark_etl.py
The core API does not require Spark, so the repository remains easy to run on a student laptop.
"""
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as _sum

ROOT = Path(__file__).resolve().parents[1]
spark = SparkSession.builder.appName("DecisionOS-ETL").getOrCreate()
df = spark.read.option("header", True).option("inferSchema", True).csv(str(ROOT / "data" / "retail_daily.csv"))
out = df.groupBy("date").agg(_sum("revenue").alias("revenue"), _sum("units_sold").alias("units_sold"))
out.write.mode("overwrite").option("header", True).csv(str(ROOT / "data" / "spark_daily"))
spark.stop()
