import os
import streamlit as st

def main():
    st.title('Simple Streamlit App')

    st.write("Hello, world!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    main()
