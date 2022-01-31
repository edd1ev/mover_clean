from logging import exception
from time import sleep
import krakenex
from pykrakenapi import KrakenAPI
import datetime

api = krakenex.API()
k = KrakenAPI(api)

# #have file in same folder
api.load_key('KrakenPass.txt')

#loop
while True:
    
    # ct stores current time
    ct = datetime.datetime.now()

    print('---Order Processing--- ')
    print(ct)
    
    #percentage to increase by
    increase = .22/100
    
    #get open orders 
    try:
        open_orders = k.get_open_orders()
    except exception as e:
        print(f'Open Order Data Found: {e}')
        print(ct)
    
    print()
    
    #get USDT price
    try:
        USDT = float((k.get_ticker_information('USDTUSD'))['a'][0][0])
        print('USDT Price: ' + str(USDT) )
    except exception as e:
        print(f'Unable to obtain USDT data: {e}')
        print(ct)
    
    print()
    
    #get USD account balance
    try:
        fiat_balance = k.get_account_balance()
        USD = fiat_balance.loc["ZUSD"][0]
        print('USD Balance: ' + str(USD))
    except exception as e:
        print(f'Unable to obtain balance data: {e}')
        print(ct)
    
    print()  
    
    #check for open orders, if open orders restart loop triggered      
    if open_orders.empty == False:
        try:
            print('---You have orders, restarting in 5 min---')
            print(ct)
            sleep (300)
            print()
        except exception as e:
            print(f'Error viewing Open Orders: {e}')
            print(ct)
            print()
    
    elif USDT <= 1.0003:
        try:
            price_start = USDT
            
            response = k.add_standard_order( 
                                      pair = 'USDTUSD',
                                      type = 'buy',
                                      ordertype = 'limit',
                                      price = str(price_start),
                                      volume = USD * .75,
                                      oflags = 'fciq',
                                      validate = False,
                                      close_ordertype= 'limit',
                                      close_price= str(round( price_start + price_start * increase , 4))
                                     )
            print(response)
            print()
        except exception as e:
            print(f'Error placing order: {e}')
            print(ct)
            print()
    
        sleep(1)
    
        check_order = k.query_orders_info(response['txid'][0])
    
        if check_order['status'][0] == 'open' or 'closed':
            print('Order completed sucessfully')
            print(ct)
            print()
            #break
        else:
            print('Order rejected')
            print(ct)
            print()
            #break
    
    else:
        print('Since USDT is currently ' + str(USDT) + ', no order will be executed' )
        print()
        print('---Order End, restarting in 5 sec---')
        print(ct)
        print()
        sleep(5)
