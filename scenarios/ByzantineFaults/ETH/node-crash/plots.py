import pandas as pd
import matplotlib.pyplot as plt

# Read the validator status dataset
validator_data = pd.read_csv('crash_nodes.csv')

# Read the transaction times dataset
transaction_data = pd.read_csv('transactions_time_final.csv')

# Extract validator status columns
timestamps_validator = pd.to_datetime(validator_data['Timestamp'])
running_validators = validator_data['RunningValidators']
stopped_validators = validator_data['StoppedValidators']

# Extract transaction times columns
timestamps_transaction = pd.to_datetime(transaction_data['Timestamp'])
transaction_times = transaction_data['Time']
transaction_status = transaction_data['Status']

# Calculate rolling averages for validator status
running_validators_smooth = running_validators.rolling(window=3, min_periods=1).mean()
stopped_validators_smooth = stopped_validators.rolling(window=3, min_periods=1).mean()

# Create subplots for the combined visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Plotting the smoothed number of running and stopped validators
ax1.plot(timestamps_validator, running_validators_smooth, label='Running Validators')
ax1.plot(timestamps_validator, stopped_validators_smooth, label='Stopped Validators')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Number of Validators')
ax1.set_title('Number of Running and Stopped Validators Over Time')
ax1.legend()
ax1.grid(True)

# Plotting the transaction times
scatter = ax2.scatter(timestamps_transaction, transaction_times, c=transaction_status.map({'Successful': 'green', 'Failed': 'red', 'Timeout': 'orange'}))
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Time (seconds)')
ax2.set_title('Transaction Times Over Time')
fig.colorbar(scatter, ax=ax2, label='Status')
ax2.grid(True)

plt.tight_layout()
plt.show()
