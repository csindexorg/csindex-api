#!/usr/bin/python

import websocket
import thread
import time
import json
import logging
import signal
import datetime

logging.basicConfig(filename='ticks.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def unsubscribe(*agrs):
    print "unsubcribe"
    unsubscribe = '{"name": "unsubscribe", \
                   "topic_id": "1" }'
    ws.send(unsubscribe)


def on_message(ws, message):
    print '%s: %s' % (datetime.datetime.now(), message)
    data = json.loads(message)
    if data['name'] == 'login_ack':
        subscribe = '{"name": "subscribe", \
                   "channel": "indexstat", \
                   "symbols": ["csi_btg"], \
                   "channel_mode": "SnapshotAndOnline"}'
        ws.send(subscribe)

        subscribe = '{"name": "subscribe", \
                   "channel": "index", \
                   "symbols": ["csi_btg"], \
                   "channel_mode": "SnapshotAndOnline"}'
        ws.send(subscribe)

        signal.signal(signal.SIGINT, unsubscribe)


def on_error(ws, error):
    print error


def on_close(ws):
    unsubscribe = '{"name": "unsubscribe", \
                   "topic_id": "1" }'
    ws.send(unsubscribe)
    print "closed"


def on_open(ws):
    login = '{"name": "login", \
            "user_id": "anonymous", \
            "token": "", \
            "ver": "1"}'
    ws.send(login)


if name == "main":
    host = "wss://csindex.org/api/index"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
