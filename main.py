import requests
import time
import threading


symbolPriceList = {}


def get_symbol_price(symbol):
    res = requests.get("https://api1.binance.com/api/v3/ticker/price?symbol=" + symbol)
    if res.status_code == 200:
        y = res.json()['price']
        return float(y)
    else:
        print("Get Symbol Price Error")
        print("Status Code:" + res.status_code)
        print("Error\n\n" + res.json())
        return -10001


def calculate_dif(symbol):
    if symbol in symbolPriceList:
        list_tmp = symbolPriceList[symbol]
        count = len(list_tmp)
        if count > 2:
            first = list_tmp[0]
            last = list_tmp[count - 1]
            before_last = list_tmp[count - 2]

            change_first = (last - first) / last
            change_last = (last - before_last) / last
            print(symbol + " Change Check with First: " + str(change_first) +
                  " Check with Last:" + str(change_last))


def add_to_dictionary(symbol, price):
    if symbol in symbolPriceList:
        symbolPriceList[symbol].append(price)
    else:
        symbolPriceList[symbol] = [price]
    print(symbol + " Price: " + str(price))


def get_price_with_time_based(symbol, second):
    while True:
        price = get_symbol_price(symbol)
        add_to_dictionary(symbol, price)
        calculate_dif(symbol)
        time.sleep(second)


t1 = threading.Thread(target=get_price_with_time_based, args=("BTCUSDT", 10, ))
t2 = threading.Thread(target=get_price_with_time_based, args=("ETHUSDT", 10, ))


t1.start()
t2.start()
