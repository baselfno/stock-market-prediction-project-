#fbprophetr liner
from fbprophet import Prophet
import csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
# csv_file = 'csv/Abdullah Al Othaim Markets Co.csv'

prediction_period = 365
Prediction_Class = 'Volume Traded'


def load_data(csv_path, isAdvanceModel):
    all_data = []
    with open(csv_path, 'r') as file:
        data = csv.reader(file)
        for row in data:
            all_data.append(row)

    dict_data = {}

    key_list = all_data[0]
    for i in key_list:
        dict_data[i] = []

    for i in all_data[1:]:
        for j in range(len(i)):
            dict_data[key_list[j]].append(i[j])

    stock_df = pd.DataFrame.from_dict(dict_data)

    dates = stock_df['date'].tolist()
    dates = [date for date in dates]
    trades = stock_df['close'].tolist()
    trades = [float(trade) for trade in trades]
    data_training = [[dates[i], trades[i]] for i in range(len(dates))]
    df = pd.DataFrame(data_training, columns=['ds', 'y'])
    if isAdvanceModel:
        df['cap'] = 8.5
    
    return df, dates, trades


# if __name__ == '__main__':
def m1_pred(text_vlue, csv_file, company_name, prophet_output_model, isAdvanceModel=False):
    # class_value = 'Close'
    m = Prophet(growth='logistic' if isAdvanceModel else 'linear')
    
    df_train, x, y = load_data(csv_file, isAdvanceModel)
    periods = text_vlue
    m.fit(df_train)
    future = m.make_future_dataframe(periods=periods)
    if isAdvanceModel:
        future['cap'] = 10
    forecast = m.predict(future)
    print(forecast.keys())
    predicted_values = forecast['yhat'].tolist()
    predicted_values = predicted_values[::-1]
    prediction = predicted_values[:len(y)]
    # predicted_values = reversed(predicted_values)
    # predicted_values = predicted_values[len(df_train):]
    plt.clf()
    plt.xlabel("No. of Days")
    plt.ylabel(f"Close")
    mse = round(mean_squared_error(y, prediction),2)
    mae = mean_absolute_error(y, prediction)
    plt.plot(y, color='green',  label="Original Closed Price")
    plt.plot(predicted_values, color='red',  label=f"Predicted Closed Price")
    plt.title(f"{prophet_output_model}_{text_vlue}")

    print(f'Mean Squared Error: {mse:.2f}')
    print(f'Mean Absolute Error: {mae:.2f}')
    plt.legend(loc=2, prop={'size': 10})
    img_path = f'img/{prophet_output_model}_{company_name}_{text_vlue}.png'
    plt.savefig(img_path)

    return img_path,mse
  