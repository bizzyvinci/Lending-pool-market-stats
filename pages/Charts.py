import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils import get_aave_df, get_compound_df


st.set_page_config(page_title = "Charts", page_icon='😀')

aave_df = get_aave_df()
compound_df = get_compound_df()


metric = st.selectbox(
    'Metric',
    [
        'Supply APY', 'Borrow APY',
        'TVL', 'Total Supply',
        'Available USD Supply', 'Available Token Supply',
        'Borrowed USD', 'Borrowed Token',
        'Utilization Rate',
        'Borrowed USD (Stable)', 'Borrowed Token (Stable)',
        'Borrowed USD (Variable)', 'Borrowed Token (Variable)'
    ]
)

pools = st.multiselect(
    'Pools',
    np.append(
        'AAVE - ' + aave_df['Asset'].unique(),
        'Compound - ' + compound_df['Asset'].unique()
    ),
    ['AAVE - USDC']
)

# Create figure
fig = go.Figure()

# Add traces
for pool in pools:
    protocol, asset = pool.split(' - ')
    name = 'a' if protocol == 'AAVE' else 'c'
    name += asset + ' ' + metric
    df = aave_df if protocol == 'AAVE' else compound_df
    df = df[df['Asset'] == asset]
    fig.add_trace(
        go.Scatter(x=df['Day'], y=df.get(metric), name=name)
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

st.plotly_chart(fig)
