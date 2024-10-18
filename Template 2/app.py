import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from flask import Flask, render_template, request
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ticker = 'AAPL'  # default ticker
    start_date = '2024-01-01'  # default start date
    end_date = '2024-10-10'  # default end date

    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

    # 確保日期是字符串格式
    start_date = str(start_date)
    end_date = str(end_date)

    # 下載股市數據
    data = yf.download(ticker, start=start_date, end=end_date)

    # 設置索引
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # 使用Plotly生成陰陽燭圖表
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])

    # 將圖表轉換為HTML
    fig_html = fig.to_html(full_html=False)

    return render_template('index.html', fig_html=fig_html)

if __name__ == '__main__':
    app.run(debug=True)
