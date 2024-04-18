import pandas as pd
import requests
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def get_active(active_item):
    url = f"http://iss.moex.com/iss/engines/stock/markets/shares/securities/{active_item}/candles.json?from=2023-05-25&till=2024-04-03&interval=24"
    response = requests.get(url)
    data = response.json()
    df2 = pd.DataFrame(data['candles']['data'], columns=data['candles']['columns'])

    result_active = df2[['begin', 'close']]
    return result_active

def get_currency(currency_item):
    start_date = datetime.strptime('12.07.2014', '%d.%m.%Y')
    end_date = datetime.strptime('05.04.2024', '%d.%m.%Y')

    data = []

    while start_date <= end_date:
        date_str = start_date.strftime('%d.%m.%Y')
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}&VAL_NM_RQ={currency_item}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            for valute in root.findall('Valute'):
                date = datetime.strptime(root.attrib['Date'], '%d.%m.%Y')
                value = float(valute.find('Value').text.replace(',', '.'))  # Convert value to float
                data.append({'Date': date, 'Value': value})
                            
        start_date += timedelta(days=1)

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime type
    df['Value'] = pd.to_numeric(df['Value'])
    return df

try:
    currency_item = 'JPY'  # Example valid currency code
    currency_df = get_currency(currency_item)
    print(currency_df)
except ValueError as e:
    print(e)


def get_cb():
    df2 = pd.read_json('нто\cb_js.json')

    df2['Date'] = df2[0]
    df3 = df2.drop(columns=[0, 2])

    slov = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08', 
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }

    def ivf(date_str):
        date_str = str(date_str)
        for k in slov.keys():
            if k in date_str:
                date_str = date_str.replace(k, str(slov[k]))
                date_str = str(date_str).split('-')[-1]
                date_str = date_str.split('г.')[0]
                date_str = date_str[-5:]
        return date_str

    df3['Date'] = df3['Date'].apply(ivf)
    df3['price'] = df3[1]
    df3 = df3.drop(columns=[1])
    df3['price'] = [k / 100 for k in df3['price']]
    result_currency = pd.DataF
    
def model_active(active_model_item):    
    url = f"http://iss.moex.com/iss/engines/stock/markets/shares/securities/{active_model_item}/candles.json?from=2023-05-25&till=2024-04-03&interval=24"
    response = requests.get(url)
    data = response.json()
    df2 = pd.DataFrame(data['candles']['data'], columns=data['candles']['columns'])

    result_active = df2[['begin', 'close']]

    model = SARIMAX(result_active['close'], order=(3, 1, 1), seasonal_order=(1, 1, 1, 12)) 
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=31) 

    start_date = '2024-04-04'
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    result_yandex1 = {'data': date_range, 'price': forecast}
    result_yandex = pd.DataFrame(result_yandex1)
    return result_yandex

# def model_currency(active_model_item):
#     url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/01/2020&date_req2=02/04/2024&VAL_NM_RQ={currency_item}"
#     df = pd.read_xml(url)
#     result_currency = pd.DataFrame(df, columns=['Date', 'Value'])

#     result_active = df2[['begin', 'close']]

#     model = SARIMAX(result_active['close'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)) 
#     model_fit = model.fit()

#     forecast = model_fit.forecast(steps=31) 

#     start_date = '2024-04-04'
#     end_date = pd.to_datetime(start_date) + pd.DateOffset(days=30)
#     date_range = pd.date_range(start=start_date, end=end_date, freq='D')
#     result_yandex1 = {'data': date_range, 'price': forecast}
#     result_yandex = pd.DataFrame(result_yandex1)
#     return result_yandex

# def model_cb():
#     df2 = pd.read_json('./data_cb.json')

#     df2['Date'] = df2[0]
#     df3 = df2.drop(columns=[0, 2])

#     slov = {
#         'января': '01',
#         'февраля': '02',
#         'марта': '03',
#         'апреля': '04',
#         'мая': '05',
#         'июня': '06',
#         'июля': '07',
#         'августа': '08', 
#         'сентября': '09',
#         'октября': '10',
#         'ноября': '11',
#         'декабря': '12'
#     }

#     def ivf(date_str):
#         date_str = str(date_str)
#         for k in slov.keys():
#             if k in date_str:
#                 date_str = date_str.replace(k, str(slov[k]))
#                 date_str = str(date_str).split('-')[-1]
#                 date_str = date_str.split('г.')[0]
#                 date_str = date_str[-5:]
#         return date_str

#     df3['Date'] = df3['Date'].apply(ivf)
#     df3['price'] = df3[1]
#     df3 = df3.drop(columns=[1])
#     df3['price'] = [k / 100 for k in df3['price']]
#     result_currency = pd.DataFrame(df3, columns=['Date', 'price'])

#     model = SARIMAX(result_currency['price'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)) 
#     model_fit = model.fit()

#     forecast = model_fit.forecast(steps=31) 

#     start_date = '2024-04-04'
#     end_date = pd.to_datetime(start_date) + pd.DateOffset(days=30)
#     date_range = pd.date_range(start=start_date, end=end_date, freq='D')
#     result_yandex1 = {'data': date_range, 'price': forecast}
#     result_yandex = pd.DataFrame(result_yandex1)
#     return result_yandex