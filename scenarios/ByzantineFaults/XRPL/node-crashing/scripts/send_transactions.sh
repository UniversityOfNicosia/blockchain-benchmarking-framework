#!/bin/bash

# Check if a command line argument is provided
if [ -z "$1" ]
then
    echo "Please provide the number of transactions as a command line argument."
    exit 1
fi

# Get the number of transactions from the command line argument
num_transactions=$1

# Name of the CSV file
csv_file="transactions_time.csv"

# Write the header to the CSV file
echo "Transaction,Timestamp,Real,User,Sys" > $csv_file

# Loop to send the specified number of transactions
for i in $(seq 1 $num_transactions)
do
    # Get the current timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Measure the execution time and parse it using awk
    (time node make_tx.js 1000:rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh:rsZBEzto16D6AvVVnuVm6pipH2J9uQeLgj:1000) 2>&1 | awk -v trans=$i -v time=$timestamp '/real/{real=$2} /user/{user=$2} /sys/{sys=$2} END{print trans","time","real","user","sys}' >> $csv_file
done
