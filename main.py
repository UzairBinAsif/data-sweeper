import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title='Data Sweeper 💿', layout='wide')
st.title('Data Sweeper 💿 and type converter 🔄')
st.write('Convert your files to CSV or excel formats with built-in Data cleaning, Compression and Visualization')

upload_files = st.file_uploader('Upload files', type=['csv', 'xlsx'], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        x = file.name
        extension = os.path.splitext(file.name)[-1]
        
        if extension == '.csv':
            df = pd.read_csv(file)
        elif extension == '.xlsx':
            df = pd.read_excel(file)
            break
        else:
            st.error(f'Unsupported file format {extension}, must ba a csv or xlsx file < 200 MB')
            continue
    
    st.write(f'**File Name:** {file.name}')
    st.write(f'**File Size:** {round(file.size/1024, 2)} MB')

    st.write('🔍 Preview of the Dataframe:')
    st.dataframe(df, use_container_width = True)

    st.subheader('🛠 Data cleaning Options')

    if st.checkbox(f'🔧 Clean data inside {x}'):
        col1, col2 = st.columns(2)
        
        with col1:
            j = st.button(f'🚮 Remove duplicates from {x}')
            
            if j:
                df.drop_duplicates(inplace=True)
                st.write('Duplicates Removed')
        
        with col2:
            k = st.button(f'💽 Fill missing values inside {x}')
            
            if k:
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                
                st.write('Filled missing values')
    st.subheader('Select columns to convert')
    columns = st.multiselect(f'Choose columns for {x}', df.columns, default=df.columns)
    df = df[columns]
    
    st.subheader('Data Visualization 📊')
    if st.checkbox(f'Show Visulaization for data inside {x}'):
        try:
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        except:
            st.error('Only Select columns with numerical values')
        
    st.subheader('Conversion 🔁')
    convert_type = st.radio('convert file to: ', ['CSV', 'EXCEL'], key=x)
    
    if st.button('CONVERT 📀'):
        buffer = BytesIO()
        
        if convert_type == 'CSV':
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(extension,'.csv')
            mime_type = 'text/csv'
        elif convert_type == 'EXCEL':
            df.to_excel(buffer, index=False)
            file_name = x.replace(extension, '.xlsx')
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        buffer.seek(0)
        st.download_button(
            label=f' Download {x} as {convert_type} 💾',
            data=buffer,
            file_name=file_name,
            mime=mime_type,
        )
        
        st.success('File converted successfully ✅')