## Version
On April 1, 2018 protocol version 1.0 was published.

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
`	{name: "subscribe", 
channel: "indexstat", 
symbols: ["csindex","csi_btc"], 
channel_mode: "SnapshotAndOnline"}.`
