import streamlit as st
import requests
import pandas as pd


@st.cache
def get_aave_df():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/b6d97815-b855-4596-b192-7813ce437e31/data/latest'
    res = requests.get(url).json()
    df = pd.DataFrame(res)
    df['day'] = pd.to_datetime(df.day)
    # Standardize columns
    df.rename(columns={
        'day': 'Day',
        'RESERVE_NAME': 'Asset',
        'SUPPLY_RATE': 'Supply Rate',
        'BORROW_RATE_VARIABLE': 'Borrow Rate',
        'BORROW_RATE_STABLE': 'Borrow Rate (Stable)',
        'SUPPLY_APY': 'Supply APY',
        'BORROW_APY_VARIABLE': 'Borrow APY',
        'BORROW_APY_STABLE': 'Borrow APY (Stable)',
        'TOTAL_LIQUIDITY_TOKEN': 'Total Supply',
        'TOTAL_LIQUIDITY_USD': 'TVL',
        'TOTAL_VARIABLE_DEBT_TOKEN': 'Borrowed Token (Variable)',
        'TOTAL_VARIABLE_DEBT_USD': 'Borrowed USD (Variable)',
        'TOTAL_STABLE_DEBT_TOKEN': 'Borrowed Token (Stable)',
        'TOTAL_STABLE_DEBT_USD': 'Borrowed USD (Stable)',
        'TOTAL_DEBT_TOKEN': 'Borrowed Token',
        'TOTAL_DEBT_USD': 'Borrowed USD',
        'AVAILABLE_SUPPLY_TOKEN': 'Available Token Supply',
        'AVAILABLE_SUPPLY_USD': 'Available USD Supply',
        'UTILIZATION_RATE': 'Utilization Rate'
    }, inplace=True)

    # Process
    for x in ['Supply Rate', 'Borrow Rate', 'Borrow Rate (Stable)', 'Supply APY', 'Borrow APY', 'Borrow APY (Stable)', 'Utilization Rate']:
        df[x] = df[x] * 100
    return df


@st.cache
def get_compound_df():
    return get_aave_df()
