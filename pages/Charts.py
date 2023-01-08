from datetime import date, timedelta

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils import get_aave_df, get_compound_df, get_aave_liquidity_index_df


st.set_page_config(page_title = "Charts", page_icon='😀')

aave_liquidity_index_df = get_aave_liquidity_index_df()
aave_df = get_aave_df()
compound_df = get_compound_df()


metric = st.selectbox(
    'Metric',
    [
        # General
        'Supply APY', 'Borrow APY',
        '1m ROI', '1y ROI',
        'Supply APR', 'Borrow APR',
        'TVL', 'Total Supply',
        'Available USD Supply', 'Available Token Supply',
        'Borrowed USD', 'Borrowed Token',
        'Utilization Rate',
        # Compound
        'Reserved Token', 'Reserved USD',
        # AAVE
        'Borrow APY (Stable)', 'Borrow APR (Stable)',
        'Borrowed USD (Stable)', 'Borrowed Token (Stable)',
        'Borrowed USD (Variable)', 'Borrowed Token (Variable)'
    ]
)

pools = st.multiselect(
    'Pools',
    np.sort(np.append(
        'AAVE - ' + aave_df['Asset'].unique(),
        'Compound - ' + compound_df['Asset'].unique()
    )),
    ['AAVE - USDC']
)

# Create figure
fig = go.Figure()


def add_lines():
    # Add traces
    for pool in pools:
        protocol, asset = pool.split(' - ')
        name = 'a' if protocol == 'AAVE' else 'c'
        name += asset + ' ' + metric
        df = aave_df if protocol == 'AAVE' else compound_df
        df = df[df['Asset'] == asset]
        fig.add_trace(
            go.Scatter(x=df['Day'], y=df.get(metric, []), name=name)
        )


    fig.update_layout(
        hovermode = 'x unified',
        yaxis = dict(
            autorange=True,
            fixedrange=False,
            title=metric,
        ),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date",
            title="Date"
        )
    )

def add_bar():
    current_date = date.today() - timedelta(days=1)
    old_date = current_date - timedelta(days=30) if metric == '1m ROI' else current_date - timedelta(days=365)
    x, y = [], []
    for pool in pools:
        protocol, asset = pool.split(' - ')
        if protocol == 'AAVE':
            name = 'a'
            df = aave_liquidity_index_df[['Day', 'Asset', 'Exchange Rate']]
            default = 1
        else:
            name = 'c'
            df = compound_df[['Day', 'Asset', 'Exchange Rate']]
            default = 2

        current_exchange_rate = df[(df['Day'] == current_date.isoformat()) & (df['Asset'] == asset)]['Exchange Rate'].values
        old_exchange_rate = df[(df['Day'] == old_date.isoformat()) & (df['Asset'] == asset)]['Exchange Rate'].values
        # Convert the array above to first item or default
        current_exchange_rate = current_exchange_rate[0] if len(current_exchange_rate) else default
        old_exchange_rate = old_exchange_rate[0] if len(old_exchange_rate) else default
        roi = 100 * (current_exchange_rate - old_exchange_rate) / old_exchange_rate
        x.append(name + asset)
        y.append(roi)
    fig.add_trace(
        go.Bar(x=x, y=y)
    )
    fig.update_layout(
        yaxis = dict(title=metric),
        xaxis = dict(title='Pool')
    )

if metric == '1m ROI' or metric == '1y ROI':
    add_bar()
else:
    add_lines()

st.plotly_chart(fig)
