import streamlit as st
import numpy as np
import pandas as pd
from utils import get_compound_df


st.set_page_config(page_title = "Compound Pools", page_icon='😀')

@st.cache
def get_displayed_df():
    df = get_compound_df()
    latest_df = df.sort_values(['Day', 'TVL'], ascending=False).groupby('Asset').head(1)

    displayed_df = pd.DataFrame()
    displayed_df['Pool'] = latest_df['Asset']
    displayed_df['TVL'] = latest_df['TVL']
    displayed_df['Supply APY'] = np.round(latest_df['Supply APY'], 2)
    displayed_df['Borrow APY'] = np.round(latest_df['Borrow APY'], 2)
    displayed_df['Available Supply'] = latest_df['Available USD Supply']
    displayed_df['Utilization Rate'] = latest_df['Utilization Rate']
    displayed_df['Reserves'] = latest_df['Reserved USD']
    return displayed_df


st.header('Compound Pools')
st.dataframe(get_displayed_df(), use_container_width=True)
