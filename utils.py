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
        'SUPPLY_RATE': 'Supply APR',
        'BORROW_RATE_VARIABLE': 'Borrow APR',
        'BORROW_RATE_STABLE': 'Borrow APR (Stable)',
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
    for x in ['Supply APR', 'Borrow APR', 'Borrow APR (Stable)', 'Supply APY', 'Borrow APY', 'Borrow APY (Stable)', 'Utilization Rate']:
        df[x] = df[x] * 100
    return df


@st.cache
def get_compound_df():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/95cbebc7-17e7-4881-b2db-42c73dc55226/data/latest'
    res = requests.get(url).json()
    df = pd.DataFrame(res)
    df['DATE_DAY'] = pd.to_datetime(df['DATE_DAY'])
    df['SYMBOL'] = df['SYMBOL'].str.slice(1)
    df['SUPPLY_RATE_PER_BLOCK'] = df['SUPPLY_RATE']
    df['BORROW_RATE_PER_BLOCK'] = df['BORROW_RATE']
    df['SUPPLY_RATE'] = ((df['SUPPLY_APY'] + 1) ** (1 / 31536000) - 1) * 31536000
    df['BORROW_RATE'] = ((df['BORROW_APY'] + 1) ** (1 / 31536000) - 1) * 31536000
    
    # Standardize columns
    df.rename(columns={
        'DATE_DAY': 'Day',
        'SYMBOL': 'Asset',
        'SUPPLY_RATE': 'Supply APR',
        'BORROW_RATE': 'Borrow APR',
        'SUPPLY_APY': 'Supply APY',
        'BORROW_APY': 'Borrow APY',
        'TOTAL_SUPPLY_TOKEN': 'Total Supply',
        'TOTAL_SUPPLY_USD': 'TVL',
        'TOTAL_BORROW_TOKEN': 'Borrowed Token',
        'TOTAL_BORROW_USD': 'Borrowed USD',
        'TOTAL_ACTIVE_TOKEN': 'Available Token Supply',
        'TOTAL_ACTIVE_USD': 'Available USD Supply',
        'TOTAL_RESERVE_TOKEN': 'Reserved Token',
        'TOTAL_RESERVE_USD': 'Reserved USD',
        'UTILIZATION_RATE': 'Utilization Rate'
    }, inplace=True)

    return df
