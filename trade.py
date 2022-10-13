import ftx


#FTX
api_key = '<ftx-api-key>'
api_secret = '<ftx-api-secret>'
already_traded = False
client = ftx.FtxClient(api_key=api_key, api_secret=api_secret)

def get_market_price(market: str):
    res = client.get_market(market)
    return res['price']
   
def do_quick_trade(market: str, long: bool, size_usd: float, sl_percent: float = -1):
    usd_price = get_market_price(market)
    order_size = size_usd / usd_price
    if(long):
        order_side = 'buy'
    else:
        order_side = 'sell'
    order_res = client.place_order(market=market, side=order_side, price=None, size=order_size, type='market')
    print('placed an order', order_res)
    if sl_percent > 0:
        if(long):
            stop_loss_trigger_price = ((100 - sl_percent) / 100) * usd_price
            sl_order_side = 'sell'
        else:
            stop_loss_trigger_price = ((100 + sl_percent) / 100) * usd_price
            sl_order_side = 'buy'
        sl_order_res = client.place_conditional_order(market=market, side=sl_order_side, size=order_size, type='stop', trigger_price=stop_loss_trigger_price)
        print('placed a stop loss order', sl_order_res)

    return order_res

def long(market: str, size_usd: float, stop_loss_percentual_movement: float = -1):
   do_quick_trade(market, True, size_usd, stop_loss_percentual_movement)

def short(market: str, size_usd: float, stop_loss_percentual_movement: float = -1):
   do_quick_trade(market, False, size_usd, stop_loss_percentual_movement)


def strategy(headline: float, core: float):
    global already_traded
# -long <= 7.9% headline && 6.3% core
# -short >= 8.3% headline && 6.6% core
    if already_traded:
        return
    elif headline <= 7.92 and core <= 6.31:
        long('BTC-PERP', 6000, 5)
        long('ETH-PERP', 3000, 6.5)
        already_traded=True
    elif headline >= 8.28 and core >= 6.55:
        short('BTC-PERP', 6000, 5)
        short('ETH-PERP', 3000, 6.5)
        already_traded=True

