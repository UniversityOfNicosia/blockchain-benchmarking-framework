#!/bin/bash

# Docker container names
VALIDATOR1="hyperledger-besu-priv-net-validator1-1"
VALIDATOR2="hyperledger-besu-priv-net-validator2-1"

split_network() {
    # Disconnect validators 1 and 2 from the existing network
    docker network disconnect quorum-dev-quickstart $VALIDATOR1
    docker network disconnect quorum-dev-quickstart $VALIDATOR2
}

reconnect_network() {
    # Reconnect validators 1 and 2 back to the existing network
    docker network connect --ip 172.16.239.11 quorum-dev-quickstart $VALIDATOR1
    docker network connect --ip 172.16.239.12 quorum-dev-quickstart $VALIDATOR2
}

if [[ $1 == "split" ]]; then
    split_network
elif [[ $1 == "reconnect" ]]; then
    reconnect_network
else
    echo "Usage: $0 {split|reconnect}"
fi