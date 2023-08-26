import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from psycopg2 import sql
import altair as alt
import time
import os

def get_database_credentials():
    host = os.environ.get('DB_HOST')
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    return host, dbname, user, password

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

def write_time_to_db(time_to_write):
    host, dbname, user, password = get_database_credentials()
    connection =  psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        # Create a cursor
        cursor = connection.cursor()

        table_name = "example_table"
        id = 'temp_user' #to replace with txt input from user

        # Insert data into the table
        insert_query = sql.SQL("""
            INSERT INTO {} (column1, column2) VALUES (%s, %s);
        """).format(sql.Identifier(table_name))

        values = (id, time_to_write)
        cursor.execute(insert_query, values)
        connection.commit()

    except Exception as e:
        print("Error:", e)
        connection.rollback()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def get_all():
    host, dbname, user, password = get_database_credentials()
    connection =  psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    rows = []
    try:
        # Create a cursor
        cursor = connection.cursor()

        query = "SELECT * FROM example_table"
        cursor.execute(query)
        rows = cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        connection.rollback()

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
    return rows

def clear_table():
    host, dbname, user, password = get_database_credentials()
    connection =  psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    delete_query = f"DELETE FROM example_table;"
    reset_sequence_query = f"ALTER SEQUENCE example_table_id_seq RESTART WITH 1;"

    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        cursor.execute(reset_sequence_query)
        connection.commit()

def main():
    st.title('Simple Streamlit App')

    tabs = ['Simple Plotting', 'Speed Clicking']
    plot_tab, click_game_tab = st.tabs(tabs)

    with plot_tab:
        df = load_data()
        column_name = 'loan_amnt'
        column_data = load_column(df, column_name)
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
    with click_game_tab:
        is_clicked = st.button('Store Current Time')
        if is_clicked:
            current_time = int(time.time_ns())
            st.write(current_time)
            write_time_to_db(current_time)
        if st.button('display your clicks!'):
            rows = get_all()
            st.write(rows)
        if st.button('clear table'):
            clear_table()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    # function to check if db exists, if not exist terminate?
    main()
