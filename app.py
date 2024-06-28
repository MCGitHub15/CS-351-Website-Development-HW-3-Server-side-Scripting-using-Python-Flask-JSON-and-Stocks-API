from flask import Flask, render_template, request, jsonify
import requests
import logging, json
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    print("DEBUG: The / route has been called!")
    #testvar = 'THIS IS A TEST' 
    #return render_template('index.html', testvar=testvar)
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def main():
    API_KEY = 'TIINGO_API_KEY'
    print("DEBUG: The /search route has been called!")

    ticker = request.args.get('search')
    testvar = 'THIS IS A TEST' 
    
    if not ticker:
        return jsonify({'error': 'Ticker symbol is required'}), 400
    
    urlDaily = requests.get(f'https://api.tiingo.com/tiingo/daily/{ticker}?token={API_KEY}')
    dailyJ = urlDaily.json()
    print(dailyJ)

    #Error handling
    error_code = 200
    if 'detail' in dailyJ:
        print("DEBUG: Recieved a 500 Internal Server Error, create an error message to return this properly!")
        error_msg = "Error: No record has been found, please enter a valid symbol"
        error_code = 500

        urlIex = requests.get(f'https://api.tiingo.com/iex/{ticker}?token={API_KEY}')
        iexJ = urlIex.json()

        tingodata = {'daily': dailyJ, 'iex': iexJ, 'err': error_code}

        return jsonify(tingodata)
        return dailyJ

    #name = dailyJ['name']
    #ticker = dailyJ['ticker']
    #exchangeCode = dailyJ['exchangeCode']
    #startDate = dailyJ['startDate']
    description = dailyJ['description']
    description = description[:260]
    description += "..."

    #Modify the data before it returns in daily
    dailyJ['description'] = description

    #print("DEBUG: The name of the company is " + name)
    #print("DEBUG: The description is " + description)

    urlIex = requests.get(f'https://api.tiingo.com/iex/{ticker}?token={API_KEY}')
    iexJ = urlIex.json()
    print(iexJ)

    timestamp = iexJ[0]['timestamp']
    timestamp = timestamp[:10] #Truncate just the time
    prevClose = iexJ[0]['prevClose']
    high = iexJ[0]['high']
    low = iexJ[0]['low']
    last = iexJ[0]['low']
    #print("DEBUG: Last is " + str(last))
    #print("DEBUG: prevClose is " + str(prevClose))
    change = round((last - prevClose), 2) #Round the percentage based on percentage 0.00%
    change = str(change) + "% " #Change this into a string variable
    #print("DEBUG: change in percent is " + change)
    volume = iexJ[0]['volume']

    #Modify the data before it returns in daily
    iexJ[0]['timestamp'] = timestamp

    tingodata = {'daily': dailyJ, 'iex': iexJ, 'err': error_code}

    return jsonify(tingodata)

    #I can't get this to rerender with new data for whatever reason
    return render_template('index.html', name=name, ticker=ticker, exchangeCode=exchangeCode, startDate=startDate, description=description, testvar=testvar,
                           timestamp=timestamp, prevClose=prevClose, high=high, low=low, last=last, change=change, volume=volume)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)