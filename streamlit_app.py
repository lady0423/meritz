import streamlit as st
import pandas as pd
import gdown
import tempfile
import os

GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

st.set_page_config(page_title="데이터 구조 확인", layout="wide")

@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    temp_path = os.path.join(tempfile.gettempdir(), "temp_data.xlsx")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
    return pd.read_excel(temp_path, sheet_name=0)

try:
    df = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)
    
    st.write("### 📊 첫 번째 행 (헤더 확인)")
    st.write(df.iloc[0].to_dict())
    
    st.write("### 📋 특정 열 데이터 확인")
    st.write(f"**0열 (A, 처음 3행):** {df.iloc[:3, 0].tolist()}")
    st.write(f"**2열 (C, 처음 3행):** {df.iloc[:3, 2].tolist()}")
    st.write(f"**3열 (D, 처음 3행):** {df.iloc[:3, 3].tolist()}")
    st.write(f"**6열 (G, 처음 3행):** {df.iloc[:3, 6].tolist()}")
    st.write(f"**11열 (L, 처음 3행):** {df.iloc[:3, 11].tolist()}")
    st.write(f"**22열 (W, 처음 3행):** {df.iloc[:3, 22].tolist()}")
    
except Exception as e:
    st.error(f"오류: {e}")
