import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
from flask import Flask
from data_parser import get_active  
from data_parser import get_currency
from data_parser import get_cb
from data_parser import model_active
slov_active = {
    'яндекс': 'YNDX',
    'сбер': 'SBER',
    'роснефть': 'ROSN',
    'лукойл': 'LKOH',
    'газпром': 'GAZP',
    'озон': 'OZON',
    'мос_биржа': 'MOEX',
    'тинькофф': 'TCSG',
    'газпромнефть': 'SIBN'
}

slov_currency = {
    'EUR': 'R01239',
    'USD': 'R01239',
    'JPY': 'R01820',
    'GBP': 'R01035',
    'CHF': 'R01775'
}

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

# Пустой DataFrame для начала
df = pd.DataFrame()

dash_app.layout = html.Div([
    html.H1('Курсы акций'),

    dcc.Dropdown(
        id='dropdown-menu',
        options=[{'label': key, 'value': slov_active[key]} for key in slov_active.keys()],
        value='YNDX'
    ),

    dcc.Graph(id='example-graph'),

    html.Div(id='example-table')
])

@dash_app.callback(
    Output('example-graph', 'figure'),
    Output('example-table', 'children'),
    Input('dropdown-menu', 'value')
)
def update_data(selected_item):
    global df
    df = get_active(selected_item)
    print(selected_item)
    graph_figure = {
        'data': [
            {'x': df['begin'], 'y': df['close'], 'type': 'line', 'name': 'Value'},
        ],
        'layout': {
            'title': 'График значений по дате'
        }
    }

    table_rows = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), 10))  # Показываем только первые 10 строк
        ])
    ])

    return graph_figure, table_rows

dash_app2 = dash.Dash(__name__, server=app, url_base_pathname='/dash2/')

# Пустой DataFrame для начала
df2 = pd.DataFrame()

dash_app2.layout = html.Div([
    html.H1('Курсы Валют'),

    dcc.Dropdown(
        id='dropdown-menu',
        options=[{'label': key, 'value': slov_currency[key]} for key in slov_currency.keys()],
        value='CHF'
    ),

    dcc.Graph(id='example-graph'),

    html.Div(id='example-table')
])

@dash_app2.callback(
    Output('example-graph', 'figure'),
    Output('example-table', 'children'),
    Input('dropdown-menu', 'value')
)
def update_data(selected_item):
    global df2
    df2 = get_currency(selected_item)
    graph_figure = {
        'data': [
            {'x': df2['Date'], 'y': df2['Value'], 'type': 'line', 'name': 'Value'},
        ],
        'layout': {
            'title': 'График значений по дате'
        }
    }

    table_rows = html.Table([   
        html.Thead(html.Tr([html.Th(col) for col in df2.columns])),
        html.Tbody([
            html.Tr([
                html.Td(df2.iloc[i][col]) for col in df2.columns
            ]) for i in range(min(len(df2), 10))  # Показываем только первые 10 строк
        ])
    ])

    return graph_figure, table_rows


dash_app3 = dash.Dash(__name__, server=app, url_base_pathname='/dash3/')

# Пустой DataFrame для начала
df3 = pd.DataFrame()
df3 = get_cb()
print(df3)
dash_app3.layout = html.Div([
    html.H1('Ставка ЦБ'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df3['Date'], 'y': df3['price'], 'type': 'line', 'name': 'Value'},
            ],
            'layout': {
                'title': 'График значений по дате'
            }
        }
    ),

    html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df3.columns])),
        html.Tbody([
            html.Tr([
                html.Td(df3.iloc[i][col]) for col in df3.columns
            ]) for i in range(min(len(df3), 10))  # Показываем только первые 10 строк
        ])
    ])
])

df4 = pd.DataFrame()
dash_app4 = dash.Dash(__name__, server=app, url_base_pathname='/dash4/')
dash_app4.layout = html.Div([
    html.H1('Предсказание Акций с помощью ИИ'),

    dcc.Dropdown(
        id='dropdown-menu',
        options=[{'label': key, 'value': slov_active[key]} for key in slov_active.keys()],
        value='EUR'
    ),

    dcc.Graph(id='example-graph'),

    html.Div(id='example-table')
])

@dash_app4.callback(
    Output('example-graph', 'figure'),
    Output('example-table', 'children'),
    Input('dropdown-menu', 'value')
)
def update_data(selected_item):
    global df4
    df4 = model_active(selected_item)
    print(selected_item)
    graph_figure = {
        'data': [
            {'x': df4['data'], 'y': df4['price'], 'type': 'line', 'name': 'Value'},
        ],
        'layout': {
            'title': 'График значений по дате'
        }
    }

    table_rows = html.Table([   
        html.Thead(html.Tr([html.Th(col) for col in df4.columns])),
        html.Tbody([
            html.Tr([
                html.Td(df4.iloc[i][col]) for col in df4.columns
            ]) for i in range(min(len(df4), 10)) 
        ])
    ])
    return graph_figure, table_rows


# dash_app5 = dash.Dash(__name__, server=app, url_base_pathname='/dash5/')

# # Пустой DataFrame для начала
# df5 = pd.DataFrame()
# df5 = model_cb()
# dash_app5.layout = html.Div([
#     html.H1('Ставка ЦБ'),

#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': df5['Date'], 'y': df5['price'], 'type': 'line', 'name': 'Value'},
#             ],
#             'layout': {
#                 'title': 'График значений по дате'
#             }
#         }
#     ),

#     html.Table([
#         html.Thead(html.Tr([html.Th(col) for col in df3.columns])),
#         html.Tbody([
#             html.Tr([
#                 html.Td(df5.iloc[i][col]) for col in df5.columns
#             ]) for i in range(min(len(df5), 10))  # Показываем только первые 10 строк
#         ])
#     ])
# ])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=2456)