
# LSTM MODEL
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from models.preprocess import load_data
from sklearn.metrics import mean_squared_error, mean_absolute_error

def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i - 50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x, y


# plt.savefig(f'results_Volume Traded.png')

def lstm_pre(nums_year, csv_file, company_name, prophet_output_model):
    # csv_path = 'csv/Abdullah Al Othaim Markets Co.csv'
    days = nums_year
    df, dates, trades = load_data(csv_file)
    df_val = df['y'].values
    df2 = df_val.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset_train = np.array(df2[:int(df.shape[0] * 0.8)])
    dataset_test = np.array(df2[int(df.shape[0] * 0.8):])
    dataset_train = scaler.fit_transform(dataset_train)
    dataset_test = scaler.transform(dataset_test)
    # print(dataset_train)
    x_train, y_train = create_dataset(dataset_train)
    x_test, y_test = create_dataset(dataset_test)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    model = Sequential()
    model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=96))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    # x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    # model.compile(loss='mean_squared_error', optimizer='adam')
    # model.fit(x_train, y_train, epochs=20, batch_size=1)
    # model.save(f'weights/stock_prediction_{Prediction_Class}.h5')
    model = load_model(f'weights/stock_prediction_Close.h5')
    predictions = model.predict(x_test)
    # print(predictions)
    predictions = scaler.inverse_transform(predictions)
    y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
    plt.clf()
    plt.xlabel("No. of Days")
    plt.ylabel(f"Close")
    # fig, ax = plt.subplots(figsize=(16, 8))
    plt.plot(y_test_scaled, color='green', label='Original price')
    # pred = predictions[:days]
    mse = round(mean_squared_error(y_test_scaled, predictions),2)
    mae = mean_absolute_error(y_test_scaled, predictions)

    print(f'Mean Squared Error: {mse:.2f}')
    print(f'Mean Absolute Error: {mae:.2f}')
    plt.plot(predictions, color='red', label='Predicted price')
    plt.legend()

    # predictions = model.predict(x_test)
    # predictions = scaler.inverse_transform(predictions)
    # y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
    # plt.clf()
    # fig, ax = plt.subplots(figsize=(16, 8))
    #
    # ax.plot(y_test_scaled, color='red', label='Original price')
    # plt.plot(predictions, color='cyan', label='Predicted price')
    # plt.title(f"{Prediction_Class}")
    # plt.legend(loc=2, prop={'size': 20})
    img_path = f'img/{prophet_output_model}_{company_name}_{nums_year}.png'
    plt.savefig(img_path)

    return img_path,mse
# if __name__ == '__main__':
#     csv_path= 'csv/Abdullah Al Othaim Markets Co.csv'
#     lstm_pre(1,'Volume Traded','lstn')
