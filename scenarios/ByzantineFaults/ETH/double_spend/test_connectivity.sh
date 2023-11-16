#!/bin/bash

# Array of validator container names
validators=("hyperledger-besu-priv-net-validator1-1" "hyperledger-besu-priv-net-validator2-1" "hyperledger-besu-priv-net-validator3-1" "hyperledger-besu-priv-net-validator4-1")

# Loop over all validators
for i in "${!validators[@]}"; do
  # Loop over all other validators
  for j in "${!validators[@]}"; do
    if [ $i -ne $j ]; then
      # Check if validator i can connect to validator j
      if docker exec -it ${validators[$i]} bash -c "echo > /dev/tcp/${validators[$j]}/8545"; then
        echo "Connection from ${validators[$i]} to ${validators[$j]} is open"
      else
        echo "Connection from ${validators[$i]} to ${validators[$j]} is closed"
      fi
    fi
  done
done