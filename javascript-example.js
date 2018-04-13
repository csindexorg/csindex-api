//getting current local comp time
var lastdate;

function update(name, values) {
    if (values.price) {
        document.getElementById(name).innerHTML = values.price.toFixed(2);
    }
    document.getElementById(name + "_tm").innerHTML = "     " + (new Date(values.ts + 'Z'));
}

function timer() {
    var date = new Date();
    var time = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
    document.getElementById("currenttime").innerHTML = date;
    lastdate = date;
};
setInterval(timer, 0);
//getting current index values
var socket = new WebSocket("wss://csindex.org/api/index");
socket.onopen = function () {
    login = '{"name":"login", "user_id":"anonymous", "token":"","ver":"1"}';
    socket.send(login);
};
var msg;
socket.onmessage = function (event) {
    msg = JSON.parse(event.data);
    console.log("Answer", event.data)
    if (msg.name == 'login_ack') {
        subscribe = '{"name":"subscribe", "channel":"indexstat","symbols":["csindex","csi_btc","csi_eth","csi_bch","csi_xrp","csi_ltc","csi_miota","csi_dash","csi_btg","csi_xmr","csi_eos"],"channel_mode":"SnapshotAndOnline"}';
        socket.send(subscribe);
    }
    if (msg.name == 'indexstat') {
        for (var i = 0; i < msg.data.length; i++) {
            var data = msg.data[i]
            update(data.symbol, data.values[0])
        }

    }
};
