# FBPROFET LOGistic
from models.preprocess import load_data
from models.arima_model import arima_predictor
import matplotlib.pyplot as plt
import pandas as pd




# plt.savefig(f'results_Volume Traded.png')

def fun_main(text_value,Prediction_Class,prophet_output_model):
    days =text_value
    # days =text_value
    csv_path = 'csv/Abdullah Al Othaim Markets Co.csv'
    print('en')
    df, dates, trades = load_data(csv_path,Prediction_Class)
    genrated_date = pd.date_range(dates[-1], periods=days+1).to_pydatetime()

    future = pd.to_datetime(genrated_date).tolist()
    del future[0]
    pred = arima_predictor(df,text_value)
    print(pred)

    # df = {'future': future, 'Prediction': pred}
    # future_df = pd.DataFrame(df)
    plt.clf()

    plt.xlabel("Time Series")
    plt.ylabel(f"{Prediction_Class}")
    predicted_values = pred.tolist()

    plt.plot(trades + predicted_values, color='red', label=f"Predicted {Prediction_Class}")
    plt.plot(trades, color='green', label="Original Volumes Traded")

    plt.title(f"{prophet_output_model}_{Prediction_Class}_{text_value}")
    plt.legend(loc=2, prop={'size': 10})
    img_path = f'img/{prophet_output_model}_{Prediction_Class}_{text_value}.png'

    plt.savefig(f'{img_path}')
    return img_path
