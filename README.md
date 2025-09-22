# 📈 Saudi Stock Prediction 

## Overview
A desktop GUI (Tkinter) for **predicting Saudi stock prices** using multiple time-series models:
- **FB-Prophet (Linear)** and **FB-Prophet (Logistic)**, with plots and MSE, and export of forecast images. 
- **LSTM** sequence model that loads a pre-trained weight file and plots predicted vs. original prices with MSE. 

The app lets you **log in**, pick a **company CSV** from `csv/`, select a **model**, choose a **prediction period (days)**, and view/save result images in `img/`. 
The app plots **actual vs. predicted** prices, shows **MSE/MAE**, and saves images to `img/`.

Models available:
- **Prophet (Linear)**
- **Prophet (Logistic)** 
- **LSTM** (loads pre-trained weights)

---

## Repository (key files)
- `GUI.py` — main GUI (login, choose company/model/days, run, clear images)
- `model_predection.py` — Prophet forecasting + metrics + plot saving
- `model_3.py` — LSTM pipeline (scaling, sequence windows, load weights, metrics, plot)
- `model_2.py` — (optional) ARIMA helpers
- `requirements.txt` — dependencies
- `csv/` — **put your company CSVs here**
- `img/` — forecast images are saved here
- `weights/` — LSTM weights (e.g., `stock_prediction_Close.h5`)

---

## Data Description
**Input:** per-company CSV file under `csv/`.  
Minimum columns (names can be adapted inside the model scripts):
- `Date` (or datetime column) — trading date
- `Close` — closing price (target to forecast)

**Prophet expects** columns mapped to:
- `ds` (datetime)
- `y` (numeric target)

**LSTM expects** a single target series (e.g., `Close`), which it scales to `[0,1]` and windows (e.g., 50 steps).

> Tip: Ensure dates are parseable (e.g., `YYYY-MM-DD`) and there are no missing values in the target column.

---

## Setup
> Recommended: Python **3.8** (for `fbprophet==0.7.1` / `pystan==2.19.x`)

Install all dependencies:
```bash
pip install -r requirements.txt

---

# run the code using this command:
python GUI.py


For login Credentials:
	username = user
	password = password
