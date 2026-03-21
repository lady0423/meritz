import streamlit as st
import pandas as pd
import gdown
import tempfile
import os

GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

st.set_page_config(page_title="열 이름 확인", layout="wide")

@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    temp_path = os.path.join(tempfile.gettempdir(), "temp_data.xlsx")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
    return pd.read_excel(temp_path, sheet_name=0, header=0)

try:
    df = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)
    
    st.write("### 📊 모든 열 이름")
    for idx, col in enumerate(df.columns):
        st.write(f"**{idx}번째:** `{col}`")
    
    st.write("### 📋 처음 2행 데이터")
    st.dataframe(df.head(2), use_container_width=True)
    
except Exception as e:
    st.error(f"오류: {e}")
