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

def plot_histogram_pyplot(data, bins):
    start = time.time()
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)

    st.pyplot(fig)
    st.write('The time to load pyplot', time.time() - start)    

def plot_histogram_altair(data, bins):
    start = time.time()
    fig=alt.Chart(data).mark_bar().encode(
        alt.X("loan_amnt").bin(maxbins=bins),
        y='count()'
    )

    st.altair_chart(fig)
    st.write('The time to load altair', time.time() - start)  

def main():

    df = load_data()

    st.title('Simple Streamlit App')

    st.dataframe(df)

    loan_amnt_data = df.loan_amnt.copy()
    histo_bins_pyplot = st.slider('Number of histogram bins', 
                           0, 
                           100, 
                           5,
                           key=1)
    plot_histogram_pyplot(loan_amnt_data, bins=histo_bins_pyplot)

    histo_bins_altair = st.slider('Number of histogram bins', 
                           0, 
                           100, 
                           5,
                           key=2)
    plot_histogram_altair(loan_amnt_data.dropna().reset_index(), bins=histo_bins_altair)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    main()
