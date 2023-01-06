import streamlit as st
import numpy as np
import pandas as pd
from utils import get_aave_df


@st.cache
def get_displayed_df():
    df = get_aave_df()
    latest_df = df.groupby('Asset').head(1)

    displayed_df = pd.DataFrame()
    displayed_df['Pool'] = latest_df['Asset']
    displayed_df['TVL'] = latest_df['TVL']
    displayed_df['Supply APY'] = np.round(latest_df['Supply APY'], 2)
    displayed_df['Borrow APY Variable'] = np.round(latest_df['Borrow APY'], 2)
    displayed_df['Borrow APY Stable'] = np.round(latest_df['Borrow APY (Stable)'], 2)
    displayed_df['Available Supply'] = latest_df['Available USD Supply']
    displayed_df['Utilization Rate'] = latest_df['Utilization Rate']
    return displayed_df


st.header('AAVE Pools')
st.dataframe(get_displayed_df(), use_container_width=True)
