import streamlit as st
import pandas as pd
import gdown
import tempfile
import os

GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

st.set_page_config(page_title="데이터 구조 확인", layout="wide")

@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    """Google Drive에서 Excel 데이터 로드"""
    temp_path = os.path.join(tempfile.gettempdir(), "temp_data.xlsx")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
    return pd.read_excel(temp_path, sheet_name=0)

try:
    df = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)
    
    st.write("### 📊 Excel 파일 정보")
    st.write(f"**행 개수:** {len(df)}")
    st.write(f"**열 개수:** {len(df.columns)}")
    
    st.write("### 📋 전체 데이터 (처음 5행)")
    st.dataframe(df.head(), use_container_width=True)
    
    st.write("### 🔍 열 정보 (Column Names)")
    for idx, col in enumerate(df.columns):
        st.write(f"**{idx}열:** {col}")
    
    st.write("### 💾 Raw 데이터 (처음 3행)")
    st.write(df.iloc[:3].to_dict())
    
except Exception as e:
    st.error(f"오류: {e}")
