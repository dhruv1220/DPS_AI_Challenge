import pandas as pd
import numpy as np
from xgboost import XGBRegressor

# Changing month to number
def preprocess_df(input_df):
    df_year = input_df[input_df['MONAT'] == 'Summe']

    df_month = input_df[input_df['MONAT'] != 'Summe']
    df_month['MONAT'] = df_month['MONAT'].apply(lambda x: int(str(x)[-2:]))
    
    return df_year, df_month


# Data Transformation
def transform_df(input_df):
    df_new = pd.DataFrame()
    temp = input_df.copy()
    temp['MONAT'] = temp['MONAT'].apply(lambda x: '0'+str(x) if x<10 else str(x))
    temp['Date'] = temp.apply(lambda x: str(x['JAHR']) + str(x['MONAT']) + '01', axis = 1)
    temp['Date'] = pd.to_datetime(temp['Date'])

    for cat in input_df['MONATSZAHL'].unique():
        for acc in temp[temp['MONATSZAHL'] == cat]['AUSPRAEGUNG'].unique():
    #         print(cat, 'and', acc)
            temp2=temp[(temp['MONATSZAHL'] == cat) & (temp['AUSPRAEGUNG'] == acc)]
            temp2 = temp2.dropna()
            col = cat + ' and ' + acc
            temp_df = pd.DataFrame()
            temp_df['Date'] = temp2['Date']
            temp_df[col] = temp2['WERT']

            if len(df_new.columns) == 0:
                df_new = temp_df.copy()
            else:
                df_new = pd.merge(df_new,temp_df, on='Date')

    df_new = df_new.set_index('Date')
    df_new.index = df_new.index.to_period('M')
    df_new = df_new.sort_index()
    return df_new


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols = list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    agg = pd.concat(cols, axis=1)
    if dropnan:
        agg.dropna(inplace=True)
    return agg.values
    
def xgboost_forecast(train, testX):
    train = np.asarray(train)
    trainX, trainy = train[:, :-1], train[:, -1]
    model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
    model.fit(trainX, trainy)
    yhat = model.predict(np.asarray([testX]))
    return yhat[0]

def walk_forward_validation(data, n_out, count):
    predictions = list()
    history = [x for x in data]
    predX = history[-1][-count:]
    for i in range(n_out):
#         print(len(predX))
        yhat = xgboost_forecast(history, predX)
        predictions.append(yhat)
        pred = np.append(predX, [yhat], axis=0)
        history.append(pred)
        predX = pred[-count:]
        
    return predictions


def model_output(year):
    # Return value if year is between 2000 and 2020 (included)
    if year>=2000 and year<=2020:
        df_month = pd.read_csv('preprocessed_df.csv')
        df_month = df_month.rename(columns = {
                'MONATSZAHL': 'category', 
                'AUSPRAEGUNG': 'type',
                'JAHR': 'year',
                'MONAT': 'month',
                'WERT': 'prediction'
                })
        return df_month[df_month['year'] == year]
    
    df_new = pd.read_csv('transformed_df.csv')

    temp = df_new.copy()
    inp_len = [180,60,120,120,180,180,60]
    count = 0
    final_df = pd.DataFrame(columns = ['category', 'type', 'date', 'prediction'])

    for col in df_new.columns:
        series = temp[[col]]
        values = series.values
        data = series_to_supervised(values, n_in=inp_len[count])
        yhat = walk_forward_validation(data, (year-2020)*12, inp_len[count])
        # print(yhat)
    #     plt.plot(yhat, label='predictions')
    #     plt.plot(test_df_new[[col]].values, label='expected')
    #     plt.legend()
    #     plt.show()

        # Convert yhat to df
        category = col.split(' and ')[0]
        typ = col.split(' and ')[1]
        col_df = pd.DataFrame()
        col_df['prediction'] = yhat
        col_df['category'] = category
        col_df['type'] = typ
        col_df['date'] = col_df.index
        col_df['date'] = col_df['date'].apply(lambda x: pd.to_datetime('2020-12-01') + pd.DateOffset(months=(int(x) + 1)))
    #     display(col_df)
        final_df = pd.concat([final_df, col_df])
        count = count + 1

    final_df['year'] = final_df['date'].dt.year
    final_df['month'] = final_df['date'].dt.month
    
    return final_df


# print(model_output(2022))

