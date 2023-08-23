import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import time

@st.cache_data
def load_data():
    file_path = './data/Anonymize_Loan_Default_data.csv'
    df = pd.read_csv(file_path,
                     encoding='latin1',
                     index_col=0)
    return df

@st.cache_data
def load_column(df, name):
    return df[name].copy().dropna()

@st.cache_data
def plot_histogram_pyplot(data, bins):
    start = time.time()
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)

    st.pyplot(fig)
    st.write('The time to load pyplot', time.time() - start)

@st.cache_data
def plot_histogram_altair(data, bins):
    start = time.time()
    fig=alt.Chart(data.reset_index()).mark_bar().encode(
        alt.X("loan_amnt").bin(maxbins=bins),
        y='count()'
    )

    st.altair_chart(fig)
    st.write('The time to load altair', time.time() - start) 

def main():

    df = load_data()
    column_name = 'loan_amnt'
    column_data = load_column(df, column_name)

    st.title('Simple Streamlit App')
    st.dataframe(df)

    histo_bins_pyplot = st.slider('Number of histogram bins', 
                           0, 
                           100, 
                           5,
                           key='pyplot_bins')
    plot_histogram_pyplot(column_data, bins=histo_bins_pyplot)

    histo_bins_altair = st.slider('Number of histogram bins', 
                           0, 
                           100, 
                           5,
                           key='altair_bins')
    plot_histogram_altair(column_data, bins=histo_bins_altair)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    main()
