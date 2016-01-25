'''
Python 2.7 version needed.

To make this file work, following lib should be installed:
- websocket (https://pypi.python.org/pypi/websocket-client/)

'''

import websocket
import thread
import time
import json


def on_message(ws, message):
    ''' Function, that creates file and writes proper message on it '''

    file_to_write = open('data.txt', 'a')
    try:
        edited = json.loads(json.loads(message)['data'])
        file_to_write.write('Roll is {} \n'.format(edited['roll']))
        print 'Roll is {}'.format(edited['roll'])
    except:
        print "OOOPS! Wrong JSON"
        pass


def on_error(ws, error):
    print 'Something went wrong: {}'.format(error)


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    ''' Function that authorizes to WS and creates thread '''

    def run(*args):
        ws.send('{"event":"pusher:subscribe","data":{"channel":"chat_ru"}}')
        ws.send('{"event":"pusher:subscribe","data":{"channel":"dice"}}')
        while True:
            time.sleep(1)
        print "thread terminating..."
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    appId = "wss://ws.pusherapp.com/app/7e8fd1da535c087cc7f0"
    ws = websocket.WebSocketApp(appId,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
