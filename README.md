# LAPD Crime Analytics & Distributed Predictive Pipeline

An end-to-end data engineering and predictive modeling project analyzing ~1 million LAPD crime records (2020-2025). This project spans initial exploratory data analysis and feature enrichment all the way to a distributed big data pipeline ready for enterprise cloud deployment.

## Project Phases

### Phase 1: Data Discovery & Feature Enrichment (Pandas, Matplotlib)
* Domain-Specific Cleaning: Identified and dropped ~102k non-physical/virtual crimes (e.g., identity theft) to eliminate artificial 12:00 PM logging spikes and restore spatial-temporal accuracy.
* Feature Engineering: Merged daily LAX weather data (NOAA API) and US federal holidays to capture environmental impacts on incident density.
* Target Encoding: Built leakage-free historical area baselines using strictly pre-2023 data.

### Phase 2: Distributed Cloud Scaling (PySpark)
* Big Data Architecture: Translated the analytical logic into a distributed PySpark pipeline for handling multi-terabyte scale.
* Model Training: Trained a distributed PySpark XGBoost Regressor (`xgboost.spark`) to forecast incident density across 6-hour patrol windows per LAPD division.
* Production Readiness: Exported the final engineered datasets as Parquet files, optimized for downstream BI tools (Power BI) and Databricks.

## Key Results
* Test MAE: 6.73 (~22.7% relative error) evaluated on a strictly out-of-time 2023 test set.
* Primary Drivers: Historical division baseline (`area_mean_crime`) and the 6-hour patrol window (`hour_bucket`) proved to be the strongest predictors.

## Repository Contents
* `01_eda_and_feature_engineering.ipynb` - Data cleaning, visualization, and baseline modeling.
* `02_pyspark_distributed_modeling.ipynb` - Distributed feature vectorization and PySpark XGBoost training.
