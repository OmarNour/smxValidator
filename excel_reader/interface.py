import streamlit as st
from excel_reader.data_loader import load_excel_to_duckdb
from excel_reader.query_executor import execute_query


def main():
    print("#####1234")
    st.title("Excel to SQL Interface")

    uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        con, sheet_info = load_excel_to_duckdb(uploaded_file)
        if sheet_info:
            st.sidebar.success("Excel file loaded successfully!")

            st.sidebar.title("Sheets and Columns")
            for sheet, columns in sheet_info.items():
                st.sidebar.subheader(sheet)
                for column in columns:
                    st.sidebar.write(column)

            query = st.text_area("Enter your SQL query here")

            if st.button("Execute Query"):
                result = execute_query(con, query)
                st.write(result)
        else:
            st.error("Failed to load the Excel file. Please check the file format and try again.")


if __name__ == "__main__":
    main()
