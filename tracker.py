import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
import numpy as np
import pandas as pd

# Failsafe: Validate date format
def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print(f"Error: Incorrect date format for '{date_text}', should be YYYY-MM-DD.")
        return None

# Input custom tickers
while True:
    tickers_input = input("Enter two ticker symbols separated by a comma (e.g., AAPL, MSFT): ")
    tickers = [symbol.strip().upper() for symbol in tickers_input.split(',')]
    if len(tickers) == 2 and all(tickers):
        first_ticker, second_ticker = tickers
        break
    print("Error: Please enter exactly two ticker symbols separated by a comma.")

# Input timeframe start and end
date_start_str = None
while True:
    date_start_str = input("Enter the start timeframe in YYYY-MM-DD: ")
    date_start = validate_date(date_start_str)
    if date_start:
        break

date_end_str = None
while True:
    date_end_str = input("Enter the end timeframe in YYYY-MM-DD: ")
    date_end = validate_date(date_end_str)
    if date_end:
        break

if date_end < date_start:
    print("Error: End date must be after start date.")
    exit(1)

# Download data with failsafe
def download_data_for_ticker(ticker_symbol):
    try:
        return yf.download(ticker_symbol, start='2010-01-01', end=date_end_str)
    except Exception as download_error:
        print(f"Error downloading data for {ticker_symbol}: {download_error}")
        exit(1)

# Get historical price data
historical_data_first = download_data_for_ticker(first_ticker)
historical_data_second = download_data_for_ticker(second_ticker)

# Filter and check data
filtered_data_first = historical_data_first.loc[date_start_str:date_end_str].dropna()
filtered_data_second = historical_data_second.loc[date_start_str:date_end_str].dropna()
if filtered_data_first.empty or filtered_data_second.empty:
    print("Error: No data available for the given date range.")
    exit(1)

# Find common dates
common_trading_dates = filtered_data_first.index.intersection(filtered_data_second.index)
if common_trading_dates.empty:
    print("Error: No overlapping dates between data sets.")
    exit(1)

# Extract price series as numpy arrays
def extract_price_array(data_frame, dates, price_column):
    try:
        return data_frame.loc[dates, price_column].values
    except KeyError:
        print(f"Error: Column '{price_column}' not found in data.")
        exit(1)

close_prices_first = extract_price_array(filtered_data_first, common_trading_dates, 'Close')
close_prices_second = extract_price_array(filtered_data_second, common_trading_dates, 'Close')
open_prices_first = extract_price_array(filtered_data_first, common_trading_dates, 'Open')
open_prices_second = extract_price_array(filtered_data_second, common_trading_dates, 'Open')

# Standard deviation comparison
def safe_std(array):
    return np.std(array) if array.size else 0.0

std_first = safe_std(close_prices_first)
std_second = safe_std(close_prices_second)
print(f"{first_ticker} Close Standard Deviation: {std_first}")
print(f"{second_ticker} Close Standard Deviation: {std_second}")
print(f"{first_ticker} is more volatile." if std_first > std_second else f"{second_ticker} is more volatile.")

# User entry date selection
while True:
    entry_date_str = input(f"At what date would you like to assume entry (YYYY-MM-DD) between {date_start_str} and {date_end_str}: ")
    entry_date = validate_date(entry_date_str)
    if entry_date and date_start_str <= entry_date_str <= date_end_str:
        break
    print("Error: Entry date must be a valid date within the timeframe.")

# Filter for post-entry period
def filter_post_entry(data_frame, start_str, end_str):
    return data_frame.loc[start_str:end_str].dropna()

post_entry_first = filter_post_entry(historical_data_first, entry_date_str, date_end_str)
post_entry_second = filter_post_entry(historical_data_second, entry_date_str, date_end_str)
common_post_dates = post_entry_first.index.intersection(post_entry_second.index)
if common_post_dates.empty:
    print("Error: No overlapping data after entry date.")
    exit(1)

# Get open price at entry as float scalars
offer_open_price_entry_first = post_entry_first.loc[entry_date_str]['Open'].values
offer_open_price_entry_second = post_entry_second.loc[entry_date_str]['Open'].values
offer_close_price_end_first = post_entry_first.loc[common_post_dates[-1]]['Close'].values
offer_close_price_end_second = post_entry_second.loc[common_post_dates[-1]]['Close'].values

# Extract post-entry close arrays for deviation calc
post_close_array_first = post_entry_first.loc[common_post_dates, 'Close'].values
post_close_array_second = post_entry_second.loc[common_post_dates, 'Close'].values
post_open_array_first = post_entry_first.loc[common_post_dates, 'Open'].values
post_open_array_second = post_entry_second.loc[common_post_dates, 'Open'].values

# Deviation calculation via original formula
pct_changes_first = ((post_close_array_first - post_open_array_first) / post_open_array_first) * 100
pct_changes_second = ((post_close_array_second - post_open_array_second) / post_open_array_second) * 100
ngtv_changes_first = pct_changes_first[pct_changes_first < 0]
ngtv_changes_second = pct_changes_second[pct_changes_second < 0]
pstv_changes_first = pct_changes_first[pct_changes_first > 0]
pstv_changes_second = pct_changes_second[pct_changes_second > 0]
sqrd_neg_first = ngtv_changes_first ** 2
sqrd_neg_second = ngtv_changes_second ** 2
sqrd_pstv_first = pstv_changes_first ** 2
sqrd_pstv_second = pstv_changes_second ** 2
mean_sqrd_neg_first = sqrd_neg_first.mean()
mean_sqrd_neg_second = sqrd_neg_second.mean()
mean_sqrd_pstv_first = sqrd_pstv_first.mean()
mean_sqrd_pstv_second = sqrd_pstv_second.mean()
dd_first = np.sqrt(mean_sqrd_neg_first)
dd_second = np.sqrt(mean_sqrd_neg_second)
ud_first = np.sqrt(mean_sqrd_pstv_first)
ud_second = np.sqrt(mean_sqrd_pstv_second)
print (f"First Open at Entry: {offer_open_price_entry_first}")
print (f"Second Open at Entry: {offer_open_price_entry_second}")
print(f"Firste's Downward Deviation: {dd_first:.4f}%")
print(f"Microsoft's Downward Deviation: {dd_second:.4f}%")
print(f"Firste's Upward Deviation: {ud_first:.4f}%")
print(f"Microsoft's Upward Deviation: {ud_second:.4f}%")


# Determine total return from entry to end
if post_close_array_first.size:
    total_return_pct_first = ((post_close_array_first[-1] - offer_open_price_entry_first) / offer_open_price_entry_first) * 100
else:
    total_return_pct_first = 0.0
if post_close_array_second.size:
    total_return_pct_second = ((post_close_array_second[-1] - offer_open_price_entry_second) / offer_open_price_entry_second) * 100
else:
    total_return_pct_second = 0.0

best_profit_ticker = first_ticker if total_return_pct_first > total_return_pct_second else second_ticker
print(f"Best profit from entry to {date_end_str}: {best_profit_ticker} with {max(total_return_pct_first, total_return_pct_second)}%")

# Calculate daily returns manually to ensure correct length and avoid pandas alignment issues
daily_returns_first = ((post_close_array_first[1:] - post_close_array_first[:-1]) / post_close_array_first[:-1]) * 100
daily_returns_second = ((post_close_array_second[1:] - post_close_array_second[:-1]) / post_close_array_second[:-1]) * 100

# Prompt for investment amount
while True:
    amount_input = input("Enter an investment amount to simulate profit calculation: ")
    try:
        investment_amount = float(amount_input)
        if investment_amount > 0:
            break
    except ValueError:
        pass
    print("Error: Please enter a valid positive number.")

# Calculate profit amounts
profit_amount_first = investment_amount * total_return_pct_first / 100
profit_amount_second = investment_amount * total_return_pct_second / 100
print(f"If you invested {investment_amount} in {first_ticker}, profit would be {profit_amount_first}")
print(f"If you invested {investment_amount} in {second_ticker}, profit would be {profit_amount_second}")

#Calculate Correlation
if len(daily_returns_first.flatten()) > 1 and len(daily_returns_second.flatten()) > 1:
    correlation = np.corrcoef(daily_returns_first.flatten(), daily_returns_second.flatten())[0, 1]
    print(f"Correlation between {first_ticker} and {second_ticker}: {correlation:.4f}")
else:
    print(f"Insufficient data to calculate correlation between {first_ticker} and {second_ticker}")

# Interpretation
def interpret_correlation(corr_value):
    if np.isnan(corr_value):
        return "Correlation is undefined (possibly due to missing or constant data)."
    elif corr_value > 0.8:
        return "Strong positive correlation: they tend to move together."
    elif corr_value > 0.5:
        return "Moderate positive correlation: generally move in the same direction."
    elif corr_value > 0.2:
        return "Weak positive correlation: some tendency to move together."
    elif corr_value > -0.2:
        return "No meaningful correlation: their movements are largely independent."
    elif corr_value > -0.5:
        return "Weak negative correlation: slight tendency to move in opposite directions."
    elif corr_value > -0.8:
        return "Moderate negative correlation: generally move in opposite directions."
    else:
        return "Strong negative correlation: they tend to move in opposite directions."

# Show interpretation
print(f"Interpretation: {interpret_correlation(correlation)}")



# Plotting helper
def safe_plot(plot_function, *args, **kwargs):
    try:
        plot_function(*args, **kwargs)
    except Exception as plot_error:
        print(f"Plot error: {plot_error}")

# Plot indices
days_full = list(range(1, len(common_trading_dates) + 1))
days_since_entry = list(range(1, len(daily_returns_first) + 1))

# Plot: Stock Prices Over Time
plt.figure(figsize=(10, 5))
safe_plot(plt.plot, days_full, close_prices_first, marker='o', linestyle='-', label=first_ticker)
safe_plot(plt.plot, days_full, close_prices_second, marker='d', linestyle='--', label=second_ticker)
plt.title('Stock Prices Over Time')
plt.xlabel('Days')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)
plt.show()

# Plot: Daily Returns since entry
plt.figure(figsize=(10, 5))
safe_plot(plt.plot, days_since_entry, daily_returns_first, marker='o', linestyle='-', label=first_ticker)
safe_plot(plt.plot, days_since_entry, daily_returns_second, marker='d', linestyle='--', label=second_ticker)
plt.title('Daily Returns from Entry Date')
plt.xlabel('Days Since Entry')
plt.ylabel('Daily Return (%)')
plt.legend()
plt.grid(True)
plt.show()

# Convert to floats if they are NumPy arrays
def extract_scalar(val):
    if isinstance(val, np.ndarray):
        return float(val.item()) if val.size == 1 else float(val[0])
    return float(val)

return_first = extract_scalar(total_return_pct_first)
return_second = extract_scalar(total_return_pct_second)
profit_first = extract_scalar(profit_amount_first)
profit_second = extract_scalar(profit_amount_second)


# Plot: Total Return Percentage
plt.figure(figsize=(6, 5))
safe_plot(plt.bar, [first_ticker, second_ticker], [return_first, return_second])
plt.title('Total Return Percentage from Entry to End')
plt.ylabel('Return (%)')
plt.grid(axis='y')
plt.show()

# Plot: Profit Amounts
plt.figure(figsize=(6, 5))
safe_plot(plt.bar, [first_ticker, second_ticker], [profit_first, profit_second])
plt.title(f'Profit Amount on Investment of {investment_amount}')
plt.ylabel('Profit Amount ($)')
plt.grid(axis='y')
plt.show()

