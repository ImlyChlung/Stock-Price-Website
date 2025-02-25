import pandas as pd
import yfinance as yf
import mplfinance as mpf
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ticker = 'AAPL'
    start_date = '2024-01-01'
    end_date = '2024-10-14'

    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

    # 下載股市數據
    data = yf.download(ticker, start=start_date, end=end_date)

    # 設置索引
    data.reset_index(inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # 畫陰陽燭圖表
    fig, ax = mpf.plot(data, type='candle', volume=True, style='charles', returnfig=True)

    # 將圖表保存到緩衝區
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')

    return render_template('index.html', img_data=img_base64)

if __name__ == '__main__':
    app.run(debug=True)




