import pandas as pd
import matplotlib.pyplot as plt

# Load the validator status data
validator_data = pd.read_csv('C:\\Users\\touloups.m\\Desktop\\ByzantineFaults\\XRPL\\node-crashing\\data\\validator_status.csv')

# Load the transaction time data
transaction_data = pd.read_csv('C:\\Users\\touloups.m\\Desktop\\ByzantineFaults\\XRPL\\node-crashing\\data\\transactions_time.csv')

# Convert the 'Timestamp' column in validator data to datetime format
validator_data['Timestamp'] = pd.to_datetime(validator_data['Timestamp'])

# Convert the 'Timestamp' column in transaction data to datetime format
transaction_data['Timestamp'] = pd.to_datetime(transaction_data['Timestamp'])

# Set the window size for the rolling average
window_size = 10

# Calculate the rolling average for the number of running validators
running_avg = validator_data['RunningValidators'].rolling(window=window_size, min_periods=1).mean()

# Calculate the rolling average for the number of stopped validators
stopped_avg = validator_data['StoppedValidators'].rolling(window=window_size, min_periods=1).mean()

# Preprocess transaction time data
transaction_data['Real'] = transaction_data['Real'].str.extract(r'(\d+\.\d+)').astype(float)

# Aggregate the transaction time data into 30-second intervals
transaction_data.set_index('Timestamp', inplace=True)
transaction_data_agg = transaction_data['Real'].resample('30S').mean().reset_index()

# Get the x-axis range from the validator status data
x_min = validator_data['Timestamp'].min()
x_max = validator_data['Timestamp'].max()

# Get the y-axis range for transaction time
y_min = 0
y_max = transaction_data['Real'].max() + 10  # Add some margin for better visualization

# Create a figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

# Plot the smoothed number of running validators
ax1.plot(validator_data['Timestamp'], running_avg)
ax1.set_title('Number of Running Validators Over Time')
ax1.set_ylabel('Number of Running Validators')
ax1.set_xlim(x_min, x_max)  # Set x-axis range

# Plot the smoothed number of stopped validators
ax2.plot(validator_data['Timestamp'], stopped_avg, color='red')
ax2.set_title('Number of Stopped Validators Over Time')
ax2.set_ylabel('Number of Stopped Validators')
ax2.set_xlim(x_min, x_max)  # Set x-axis range

# Plot the aggregated transaction time with markers
ax3.plot(transaction_data_agg['Timestamp'], transaction_data_agg['Real'], marker='o', linestyle='-')
ax3.set_title('Aggregated Transaction Time Over Time (30-second intervals)')
ax3.set_xlabel('Time')
ax3.set_ylabel('Transaction Time')
ax3.set_xlim(x_min, x_max)  # Set x-axis range
ax3.set_ylim(y_min, y_max)  # Set y-axis range

# Adjust the spacing between subplots
plt.tight_layout()

# Display the combined plot
plt.show()
