from web3 import Web3, HTTPProvider

# Initialize the web3 instances for each half of the network
web3_1 = Web3(HTTPProvider('http://18.203.164.164:21001'))  # adjust the URLs as needed
web3_2 = Web3(HTTPProvider('http://18.203.164.164:21003'))

# The account that will be doing the double spend
account = "0x21b0c2bEfdd3599fC69431b14fF45D0df9F03c23"

# The private key of the account doing the double spend
private_key = "0x6fe8890c925cc7061e4682162077291891610bb6845441a2f0d35cee8f5e0edc"

# The addresses that the funds will be sent to
address_1 = "0x603Fb8848aFF62f3955DEc4940C9976776Beb171"
address_2 = "0xE493C595574c6B55cebbcbd6EfdC72842e8234CC"

# The amount to send
amount = Web3.toWei(1, 'ether')

# Get the current nonce
nonce = web3_1.eth.getTransactionCount(account)

# Create the transactions
transaction_1 = {
    'to': address_1,
    'value': amount,
    'gas': 2000000,
    'gasPrice': Web3.toWei('50', 'gwei'),
    'nonce': nonce,
    'chainId': 1338  # replace with your chain ID
}

transaction_2 = {
    'to': address_2,
    'value': amount,
    'gas': 200000,
    'gasPrice': Web3.toWei('100', 'gwei'),
    'nonce': nonce,
    'chainId': 1338  # replace with your chain ID
}

# Sign the transactions
signed_transaction_1 = web3_1.eth.account.signTransaction(transaction_1, private_key)
signed_transaction_2 = web3_2.eth.account.signTransaction(transaction_2, private_key)

# Broadcast the transactions and handle any errors
try:
    tx_hash_1 = web3_1.eth.sendRawTransaction(signed_transaction_1.rawTransaction)
    print(f"Transaction 1 hash: {tx_hash_1.hex()}")
except Exception as e:
    print(f"Error sending transaction 1: {e}")

try:
    tx_hash_2 = web3_2.eth.sendRawTransaction(signed_transaction_2.rawTransaction)
    print(f"Transaction 2 hash: {tx_hash_2.hex()}")
except Exception as e:
    print(f"Error sending transaction 2: {e}")
