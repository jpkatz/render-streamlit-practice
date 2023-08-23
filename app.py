import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    file_path = './data/Anonymize_Loan_Default_data.csv'
    df = pd.read_csv(file_path,
                     encoding='latin1',
                     index_col=0)
    return df

def plot_bar(data, bins):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)

    st.pyplot(fig)          

def main():

    df = load_data()

    st.title('Simple Streamlit App')

    st.dataframe(df)

    loan_amnt_data = df.loan_amnt
    histo_bins = st.slider('Number of histogram bins', 
                           0, 
                           100, 
                           5)
    plot_bar(loan_amnt_data, bins=histo_bins)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    main()
