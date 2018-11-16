## Version
On April 1, 2018 protocol version 1.0 was published

## WebSocket URL
wss://csindex.org/api/index

## WebSocket standard
WebSocket is offered according to RFC 6455 standard (https://tools.ietf.org/html/rfc6455).

## Messages
All messages have JSON format.

### Subscribe
Client opens channel using “subscribe” message in which the set of indices is specified:

| Parameter    | Format          | Description                                                          |
|--------------|-----------------|----------------------------------------------------------------------|
| channel      | string          | Unique channel name. Currently there is just one channel “indexstat” |
| channel_mode | string          | Channel mode. Possible values:,“Snapshot” or “SnapshotAndOnline”     |
| symbols      | List of strings | List of index tickers                                                |

Example:
```json
{
  "name": "subscribe", 
  "channel": "indexstat", 
  "symbols": ["csindex","csi_btc"], 
  "channel_mode": "SnapshotAndOnline"
}
```

### Subscribe report
The result of subscription comes in the form of “subscribe_report” message:

| Parameter     | Format          | Description                                                          |
|---------------|-----------------|----------------------------------------------------------------------|
| state         | integer         | Message processing status                                            |
| time          | t               | Server time                                                          |
| channel       | string          | Channel name. See “subscribe” message description                    |
| channel_state | string          | Subscription status: “Closed”, “Snapshot” or “Online”                |
| message       | string          | Text message                                                         |
| topic_id      | string          | Unique subscription code for subscription management                 |
| channel_mode  | string          | Optional. Mode of channel opening: “Snapshot” or “SnapshotAndOnline” |

Example:
```json
{
  "name": "subscribe_report",
  "time": "2018-01-17T13:06:40.449790436",
  "channel": "indexstat",
  "state": 0,
  "message": "Ok",
  "topic_id": "1",
  "channel_state": "Snapshot"
}
```

### Index, snapshot
Then current values of all index parameters come in an “index” snapshot message:

| Parameter     | Format             | Description                                            |
|---------------|--------------------|--------------------------------------------------------|
| time          | t                  | Server time of message generation                      |
| channel       | string             | Channel name. See “subscribe” message description      |
| topic_id      | string             | Unique subscription code                               |
| data          | List of index_data | Index parameters                                       |

Type “index_data” has structure:

| Parameter     | Format             | Description             |
|---------------|--------------------|-------------------------|
| symbol        | string             | Index ticker            |
| values        | List of value      | Index parameters array  |

Type “value” has structure:

| Parameter | Format    | Description                                                     |
|-----------|-----------|-----------------------------------------------------------------|
| price     | decimal   | Last index value                                                |
| ts        | t         | Time of last index calculation                                  |
| fixing    | decimal   | Optional. Last fixing value. Usually generated daily            |
| dt        | decimal   | Change of last inged value to the fixing value, in index points |
| high      | decimal   | Optional. Maximal index value since the time of last fixing     |
| low       | decimal   | Optional. Minimal index value since the time of last fixing     |

Example:
```json
{
  "name": "index",
  "time": "2018-01-17T13:06:40.449762062",
  "channel": "indexstat",
  "topic_id": "1",
  "data": [{
    "symbol": "csi_",
    "values": [{
      "price": 1.04308519,
      "ts": "2018-01-17T12:53:05",
      "dt": 0.001,
      "high": 1.09,
      "low": 1.01,
      "fixing": 1.04
    }]
  }]
}
```

After “index” snapshot messages transmission, comes “subscribe_report” with “channel_state”:
“Online”.

Example:
```json
{
  "name": "subscribe_report",
  "time": "2018-01-17T13:06:40.449790436",
  "channel": "indexstat",
  "state": 0,
  "message": "Ok",
  "topic_id": "1",
  "channel_state": "Online"
}
```

### Index, online
After the latter “subscribe_report” message, online stream of “index” messages with partial set of
parameters starts.

Example:
```json
{
  "name": "index",
  "time": "2018-01-17T13:06:40.449762062",
  "channel": "indexstat",
  "topic_id": "1",
  "data": [{
    "symbol": "csi_",
    "values": [{
      "price": 1.04308519,
      "ts": "2018-01-17T12:53:05",
      "dt": -0.0001
    }]
  }]
}
```

### Subscribe_modify
Subscription can be modified using “subscribe_modify” message:

| Parameter    | Format         | Description                                 |
|--------------|----------------|---------------------------------------------|
| topic_id     | string         | Unique subscription code                    |
| modify_mode  | string         | Mode of change: “Add”, “Remove”, “Replace”  |
| symbols      | List of string | List of tickers                             |

### Subscribe_modify_report
The result of modification comes in “subscribe_modify_report” message:

| Parameter | Format    | Description                       |
|-----------|-----------|-----------------------------------|
| time      | t         | Server time of message generation |
| state     | integer   | Message processing status         |
| message   | string    | Text message                      |
| topic_id  | string    | Unique subscription code          |

### Unsubscribe
Subscription can be closed with “unsubscribe” message:

| Parameter | Format    | Description              |
|-----------|-----------|--------------------------|
| topic_id  | string    | Unique subscription code |

After “unsubscribe” command user gets “subscribe_report” message with “channel_state”:
“Closed”.
After that user does not get any further messages in the channel with given topic_id.

## Response state codes

| Value | Code                   |
|-------|------------------------|
| 0     | Ok                     |
| 1     | UserBlocked            |
| 2     | InvalidToken           |
| 3     | UserDisconnected       |
| 4     | TopicNotSubscribed     |
| 5     | SpecifySymbols         |
| 6     | BadChannel             |
| 7     | InvalidMode            |
| 8     | LoginTimeout           |
| 9     | InvalidSymbol          |
| 10    | RateExceeded           |
| 11    | AnonymousDisallowed    |
| 12    | Partial                |
| 13    | HeartbeatTimeout       |
| 14    | TopicAlreadySubscribed |
| 15    | InvalidModifyMode      |
| 16    | UnsupportedVersion     |








