''' optionftxtest.py - FTXのオプションAPIをテストするアプリ '''

import os.path
from decimal import Decimal
# import json
from time import sleep

from termcolor import cprint

from bitIAI4.exchange.ftx import FTXAPIInfo, FTXAccount, FTXOptionClient, FTXOptionExpiry
from bitIAI4.trade import Direction, OptionType

__author__ = 'Takeyuki Watadani<twatadani@swan.ocn.ne.jp>'
__version__ = '0.1'
__date__ = '2021/11/10'
__status__ = 'dev'

msg = 'OptionFTXTest バージョン' + __version__ + 'を開始します。'
cprint(msg, 'green')

# APIInfoの準備
apipath = '~/.optionftxtest/FTXAPI.json'
apipath = os.path.expanduser(os.path.expandvars(apipath))
apiinfo = FTXAPIInfo(apipath)

# accountとclientの準備
account = FTXAccount(apiinfo)
client = account.client

assert isinstance(client, FTXOptionClient)

# list_public_quotesのテスト
msg = 'パブリックなオプションquoteの一覧を表示します。'
cprint(msg, 'yellow')
print(client.list_public_quotes())

# quote_requestのテスト

optyp = OptionType.Put
strike = Decimal('66600')
expiry = FTXOptionExpiry(2021, 11, 11)
print(expiry.unixtime())
side = Direction.Buy
size = Decimal('0.0002')

msg = 'オプションのquote requestを行います。'
cprint(msg, 'yellow')
result = client.quote_request(optyp, strike, expiry, side, size)
print(result)

resultdict = result # json.loads(result)
request_id = resultdict['result']['id']

# get_quoteのテスト
msg = 'get_quoteのテストを行います。'
cprint(msg, 'yellow')
for i in range(15):
    result = client.get_quote(request_id)
    print(result)
    resultdict = result # json.loads(result)
    quotes = resultdict['result']
    if len(quotes) == 0:
        cprint('提示されたquoteがありません。')
    else:
        for q in quotes:
            quoteid = q['id']
            price = Decimal(q['price'])
            cprint('提示されたquoteのidは' + str(quoteid) + ', priceは' + str(price) + 'です。', 'yellow')
    sleep(4)

# cancel quoteのテスト
msg = 'cancel quoteのテストを行います。'
cprint(msg, 'yellow')
result = client.cancel_quote(request_id)
print(result)

msg = 'OptionFTXTestを終了します。'
cprint(msg, 'yellow')
