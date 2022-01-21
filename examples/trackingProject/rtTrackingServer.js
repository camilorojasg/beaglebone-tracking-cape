//For non-commercial use!

//Load NET and Socket.io libraries
var io = require('socket.io')(1909);
var net = require('net');
 
//Start a TCP Server
net.createServer(function (socket) {
 
        //Identify this client
        socket.name = socket.remoteAddress + ":" + socket.remotePort
 
        console.log("Tracking Cape connected (" + socket.name + ")\n");

        //Handle incoming messages from clients.
        socket.on('data', function (data) {
                console.log("TrackingCape says: " + data + "\n");
                //Emit new received coordinates.
                io.emit('newCoord', { coord: data});
        });
 
        socket.on('end', function () {
                console.log("TrackingCape disconnected.\n");
        });
 
}).listen(5000);
 
console.log("Waiting for BeagleBone Tracking Cape. Port 5000\n");