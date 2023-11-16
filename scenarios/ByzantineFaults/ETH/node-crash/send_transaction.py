import requests
import csv
import time
from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
import sys

# Connect to Ethereum node
w3 = Web3(HTTPProvider("http://18.203.164.164:8545"))

# Set private key
private_key = "0x6fe8890c925cc7061e4682162077291891610bb6845441a2f0d35cee8f5e0edc"

# Get the account's public address
account_address = w3.eth.account.from_key(private_key).address

# Set the recipient Ethereum address
to_address = "0xE43121e27407a0D6cD1d7966aD489C6fD18C4B3D"

# Get the number of transactions to send from the user
num_transactions = int(input("Enter the number of transactions: "))

# Open the CSV file and create a CSV writer
with open("transactions_time.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Transaction", "Timestamp", "Time", "Status"])

    # Send the specified number of transactions
    for i in range(1, num_transactions + 1):
        nonce = w3.eth.get_transaction_count(account_address)
        txn = {
            "to": to_address,
            "value": w3.toWei(1, 'ether'),  # sending 0.01 Ether
            "gas": 2000000,
            "gasPrice": Web3.toWei('100', 'gwei'),
            "nonce": nonce,
            "chainId": w3.eth.chain_id
        }

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(txn, private_key)

        # Attempt to send the transaction and handle potential Timeout error
        try:
            start_time = time.time()
            txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            w3.eth.wait_for_transaction_receipt(txn_hash)
            elapsed_time = time.time() - start_time
            status = "Successful"
        except (requests.exceptions.Timeout, TimeExhausted) as e:
            print(f"Transaction {i} error: {str(e)} after {time.time() - start_time} seconds.")
            elapsed_time = "Timeout"
            status = "Failed"
            continue

        # Write the transaction number, timestamp, elapsed time, and status to the CSV file
        writer.writerow([i, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), elapsed_time, status])

        print(f"Transaction {i} sent in {elapsed_time} seconds.")
        sys.stdout.flush()
        # Sleep for a while before sending the next transaction
        time.sleep(1)
