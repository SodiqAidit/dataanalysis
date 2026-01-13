import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title='Analyze Your Data',page_icon='📊',layout='wide')

st.title('Analyze Your Data📊📊')
st.write('Upload A **CSV** or An **Excel Files** To Explore Your Data Interactively')

st.title("Upload CSV or Excel File")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xls", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Get file extension
        file_name = uploaded_file.name
        file_extension = file_name.split(".")[-1].lower()

        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)

        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(uploaded_file)

        else:
            st.error("Unsupported file type")
            st.stop()

        st.success("File uploaded successfully!🛫")
        st.write("Preview of data:")
        st.dataframe(df)

    except Exception as e:
        st.error('Could Not Read Excel / CSV File. Please Check The File Format')
        st.exception(e)
        st.stop()

    st.dataframe(df.head())
    st.write('### Data Overview🚥')
    st.write('Number of Row:',df.shape[0])
    st.write('Number of column:',df.shape[1])
    st.write('Number of Missing Value:',df.isnull().sum().sum())   # for another of .sum() is to show total of value in streamlit
    st.write('Number of Duplicate Record:',df.duplicated().sum())

    st.write('### 🫰Complete Summary of Dataset🫰')
    # st.dataframe(data.info()) # info() method only provide plain text summary
    # we can use StringIO able to catch plain text inside the data
    buffer = io.StringIO()
    df.info(buf = buffer)
    i = buffer.getvalue()
    st.text(i)

    st.write('### 🫰Statistical Summary of Dataset🫰')
    st.dataframe(df.describe())

    st.write('### 🫰Statistical Summary For Non Numerical Features of Dataset🫰')
    non_numeric_cols = df.select_dtypes(include=['object', 'bool'])

    if not non_numeric_cols.empty:
        st.dataframe(non_numeric_cols.describe())
    else:
        st.info("No non-numerical (object/bool) features found in this dataset.")

    st.write('### ✍️Select the desire column for Analysis✍️')
    selected_columns = st.multiselect('Choose Column',df.columns.tolist())

    if selected_columns:
        st.dataframe(df[selected_columns].head())
    else:
        st.info("No Columns Selected. Showing Full Dataset")
        st.dataframe(df.head())
    
    
    st.write('📉Data visualization📉')
    st.write('Select **Column** for data visualization')
    column = df.columns.tolist()
    x_axis = st.selectbox('Select Column for X-Axis',options=column)
    y_axis = st.selectbox('Select Column for Y-Axis',options=column)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        line_btn = st.button('Line Graph')
    with col2:
        scatter_btn = st.button('Scatter Graph')
    with col3:
        bar_btn = st.button('Bar Graph')
    with col4:
        pie_btn = st.button('Pie Graph')

    if line_btn:
        st.write('### Showing a Line Graph')
        fig,ax = plt.subplots()
        ax.plot(df[x_axis],df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Line  Graph of {x_axis} vs {y_axis}')
        st.pyplot(fig) # show the graph
    
    if scatter_btn:
        st.write('### Showing a Scatter Graph')
        fig,ax = plt.subplots()
        ax.scatter(df[x_axis],df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Scatter Graph of {x_axis} vs {y_axis}')
        st.pyplot(fig) # show the graph

    if bar_btn:
        st.write('### Showing a Bar Graph')

        fig, ax = plt.subplots()
        ax.bar(df[x_axis], df[y_axis])
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f'Bar Graph of {x_axis} vs {y_axis}')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    if pie_btn:
    
        if df[x_axis].dtype not in ['object', 'bool']:
            st.warning("Pie chart works best with categorical columns.")
        else:
            st.write('### Showing a Pie Graph')

            pie_data = df[x_axis].value_counts()

            fig, ax = plt.subplots()
            ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct='%1.1f%%',
            startangle=180)
            ax.set_title(f'Pie Chart of {x_axis}')
            ax.axis('equal')
            st.pyplot(fig)
else:
    st.info('Please Upload A CSV or An Excelfile to get Started')
