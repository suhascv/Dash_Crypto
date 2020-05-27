import dash
import dash_core_components as dcc
import dash_html_components as html
import sys
import requests
import datetime as dt


def get_last_7_days():
    today=dt.date.today()
    seven_days=[]
    for i in range(6,-1,-1):
        seven_days.append(today-dt.timedelta(days=i))
    return seven_days


def get_live_data(data):
    crypto_data=[]
    for d in data:
        crypto={'name':d['name'],'y':[],'x':[],'type':'line'}
        last_7_days=get_last_7_days()
        j=24
        for day in last_7_days:
            crypto['x'].append(day)
            crypto['y'].append(((d['sparkline_in_7d']['price'][j]-d['sparkline_in_7d']['price'][j-23])/d['sparkline_in_7d']['price'][j])*100)
            j+=23
        crypto_data.append(crypto)
    return crypto_data

   

app =dash.Dash()
request_data=requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1&sparkline=true&price_change_percentage='1h'").json()
crypto_data=get_live_data(request_data)


app.layout = html.Div(children=[
    html.H1('Live Crypto Trends'),
    dcc.Graph(id='crypto',
              figure={
                  'data':crypto_data,
                  'layout':{
                      'title':'past week price trend in perecentage of top 5 crypto currencies'
                  }
              }
    )

])

if __name__=='__main__':
    app.run_server(debug=True)