'use strict';
const RippleAPI = require('ripple-lib').RippleAPI;

const api = new RippleAPI({
    server: 'ws://18.203.164.164:6006' // Public ripple server
});

var sourceAddress = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh"; 
var secret = "snoPBrXtMeMyMHUVTgbuqAfg1SUTb"; 
var destinationAddress1 = "rpd3Q9F3bpbi9Lxf2iMHgauXFyPrUfgmjX";
var destinationAddress2 = "rJYJPiWauDCG4UZjnxto8P29KTL4VLPAYc";

api.connect().then(() => {
    return api.getAccountInfo(sourceAddress).then(accountInfo => {
        const sequence = accountInfo.sequence;

        const transaction1 = {
            "TransactionType" : "Payment",
            "Account" : sourceAddress,
            "Amount" : "1000000",
            "Destination" : destinationAddress1,
            "Sequence": sequence
        };

        const transaction2 = {
            "TransactionType" : "Payment",
            "Account" : sourceAddress,
            "Amount" : "1000000",
            "Destination" : destinationAddress2,
            "Sequence": sequence
        };

        const {signedTransaction: signedTransaction1} = api.sign(JSON.stringify(transaction1), secret);
        api.submit(signedTransaction1);

        const {signedTransaction: signedTransaction2} = api.sign(JSON.stringify(transaction2), secret);
        api.submit(signedTransaction2);
    }).then(() => {
        return api.disconnect();
    }).then(() => {
        console.log('Done and Disconnected.');
    }).catch(console.error);
});

