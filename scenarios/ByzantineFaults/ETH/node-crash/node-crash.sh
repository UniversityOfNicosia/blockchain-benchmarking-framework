#!/bin/bash

# Initialize csv file
echo "Timestamp,RunningValidators,StoppedValidators" > validators.csv

# List of validators
validators=("hyperledger-besu-priv-net-validator1-1" "hyperledger-besu-priv-net-validator2-1" "hyperledger-besu-priv-net-validator3-1" "hyperledger-besu-priv-net-validator4-1")

# Array to keep track of stopped validators
stopped=()

while true; do
    # Only stop a validator if there's more than one running
    if [ ${#validators[@]} -gt 3 ]; then
        # Select a random validator to stop
        validator=${validators[$RANDOM % ${#validators[@]}]}

        # Stop the validator
        echo "Stopping $validator"
        docker stop $validator

        # Add it to the stopped validators array
        stopped+=($validator)

        # Remove it from the validators array
        validators=(${validators[@]//$validator})
    fi

    # Randomly select whether to restart a validator or not, only if there's at least one stopped validator
    if (( RANDOM % 2 )) && [ ${#stopped[@]} -gt 0 ]; then
        # Select a random number of validators to start
        num_to_start=$(shuf -i 1-${#stopped[@]} -n 1)
        echo "Starting $num_to_start validators"
        for i in $(seq $num_to_start); do
            # Select a random stopped validator to start
            restartValidator=${stopped[$RANDOM % ${#stopped[@]}]}

            # Start the validator
            echo "Starting $restartValidator"
            docker start $restartValidator

            # Check if the validator was successfully started
            if [ $? -eq 0 ]; then
                # Add it back to the validators array
                validators+=($restartValidator)

                # Remove it from the stopped validators array
                stopped=(${stopped[@]//$restartValidator})
            fi
        done
    fi

    # Get timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")

    # Print out the number of running and stopped validators
    echo "$timestamp, ${#validators[@]}, ${#stopped[@]}" >> validators.csv

    # Wait for 30 seconds
    sleep 30
done