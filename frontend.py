import streamlit as st 
from main import get_data_from_database # Importing main to use its functions
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon=":bar_chart:",
    layout="centered"
)

st.title("AI Data Analyst")
st.subheader("Generate SQL queries from natural language and visualize data effortlessly!")
st.markdown("""
This application allows you to input natural language queries, which are then converted into SQL queries to fetch data from a sample database. The results are displayed in an easy-to-understand format.
""")
user_query = st.text_input("Enter your query about the Amazon database:", "List the name of all customers")

if st.button("Generate SQL and Fetch Data"):
      
    try:
        result = get_data_from_database(user_query)
        st.subheader("Query Result:")
        if result:
            for row in result:
                st.write(row)
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"An error occurred while executing the SQL query: {e}")
    