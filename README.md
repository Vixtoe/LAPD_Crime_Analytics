# LAPD Crime Analytics & Distributed Predictive Pipeline

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-Launch_App-brightgreen?style=for-the-badge&logo=dash)](https://lapd-crime-dashboard.onrender.com/)

![PySpark](https://img.shields.io/badge/PySpark-Distributed-orange?style=flat-square&logo=apachespark)
![Model](https://img.shields.io/badge/Model-XGBoost%20Regressor-blue?style=flat-square)
![Dashboard](https://img.shields.io/badge/Dashboard-Dash%20%2F%20Plotly-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python)

An end-to-end data engineering and predictive modeling project analyzing **~1 million LAPD crime records (2020–2024)**. This project spans initial data cleaning and feature enrichment with PySpark all the way to an XGBoost regression model and an interactive Dash visualization web application deployed on Render.

> **Note**: This web application is hosted on Render's free tier. If the app has been inactive, the server may spin down into sleep mode. The initial load may take up to **50–60 seconds** to boot up. Subsequent interactions will be instantaneous.

---

## 📌 Executive Summary

* **Data Volume Processed**: Ingested **1,004,847** raw incident records from Kaggle via `kagglehub`.
* **Data Cleaning & Filtering**: Removed **102,792** non-physical crime entries (e.g., identity theft, fraud) to retain **902,055** physical crime events.
* **Feature Engineering**: Created temporal features including `year`, `month`, `day_of_week`, `is_weekend`, and 6-hour discrete `hour_bucket` intervals.
* **Model Performance**: The XGBoost Regressor achieved a **6.40 MAE** (crimes per slice) on 2023 test data, outperforming Baseline 1 by **36.89%** and Baseline 2 by **17.21%**.
* **Deployment**: Permanently hosted as a production **Dash & Plotly** web service on **Render**, served via Gunicorn.

---

## 📊 Model Evaluation Results

Evaluation performed on 2023 test data (7,056 spatio-temporal slices, mean actual crime count: **29.63**):

| Model / Baseline | MAE | MAE (% of Mean Actual) | Improvement vs. Baseline 1 | Improvement vs. Baseline 2 |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline 1 (Area Mean)** | 10.13 | 34.20% | Benchmark | — |
| **Baseline 2 (Previous Year)** | 7.73 | 26.07% | +23.77% | Benchmark |
| **XGBoost Regressor** | **6.40** | **21.59%** | **+36.89%** | **+17.21%** |

---

## 📂 Project Structure

```text
.
├── tests/
│   └── test_etl.py                    # PySpark transformations & parsing unit tests
├── .gitignore                         # Excludes raw data, parquet outputs & pickles
├── 01_eda_and_feature_engineering.ipynb # Jupyter/Colab exploratory analysis notebook
├── 02_pyspark_distributed_modeling.ipynb# Jupyter/Colab PySpark modeling notebook
├── app.py                             # Production Dash web application (Flask server)
├── Cn340_LAPD_compressed.pdf          # Compressed project report PDF
├── etl.py                             # PySpark ETL & spatial-temporal aggregation
├── model.py                           # XGBoost regressor, baseline evaluation & CSV export
├── predictions_2023.csv               # Pre-computed model outputs for dashboard rendering
├── README.md                          # Project documentation
└── requirements.txt                   # Production Python dependencies
