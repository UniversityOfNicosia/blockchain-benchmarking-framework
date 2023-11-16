#!/bin/bash

# Initialize csv file
echo "Timestamp,RunningValidators,StoppedValidators" > validators.csv

# Get list of validators dynamically, excluding "xrpl-validator-genesis"
validators=($(docker ps -a --format '{{.Names}}' | grep '^xrpl-validator-' | grep -v '^xrpl-validator-genesis$'))

# Array to keep track of stopped validators
stopped=()

while true; do
    # Select a random validator to stop
    validator=${validators[$RANDOM % ${#validators[@]}]}

    # Stop the validator
    echo "Stopping $validator"
    docker stop $validator

    # Add it to the stopped validators array
    stopped+=($validator)

    # Remove it from the validators array
    validators=(${validators[@]//$validator})

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
    echo "$timestamp, $((${#validators[@]} + 1)), ${#stopped[@]}" >> validators.csv

    # Wait for 30 seconds
    sleep 30
done
