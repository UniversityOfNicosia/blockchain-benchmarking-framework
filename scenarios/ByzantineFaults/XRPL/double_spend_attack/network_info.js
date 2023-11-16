'use strict';
const RippleAPI = require('ripple-lib').RippleAPI;

const api = new RippleAPI({
server: 'ws://18.203.164.164:6006' // Public ripple server
});
api.connect().then(() => {

return api.getServerInfo().then(info => {
	console.log(info)
});

}).then(() => {
return api.disconnect();
}).then(() => {
console.log('Done and Disconnected.');
}).catch(console.error);