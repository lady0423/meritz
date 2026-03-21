import streamlit as st
import pandas as pd
import gdown
import tempfile
import os

# Google Drive 파일 ID
GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

# 페이지 설정
st.set_page_config(page_title="실적 안내장 조회", layout="wide")
st.title("📊 실적 안내장 조회")

# 캐시 함수
@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_data.xlsx")
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except:
        pass
    download_url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(download_url, temp_file, quiet=True)
    if os.path.exists(temp_file):
        df = pd.read_excel(temp_file)
        try:
            os.remove(temp_file)
        except:
            pass
        return df
    return None

# 데이터 로드
with st.spinner("데이터 로드 중..."):
    df_data = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)

if df_data is None:
    st.error("❌ 데이터를 로드할 수 없습니다.")
    st.stop()

st.success("✅ 데이터 로드 완료!")

# UI 입력
st.write("---")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    manager_input = st.text_input("📝 매니저명")
with col2:
    agent_code_input = st.text_input("🔍 설계사 코드")
with col3:
    search_button = st.button("검색", key="search_btn")

# 검색 로직
if search_button:
    if not manager_input or not agent_code_input:
        st.warning("⚠️ 매니저명과 설계사 코드를 입력하세요.")
    else:
        filtered_data = df_data[
            (df_data.iloc[:, 0].astype(str).str.strip() == agent_code_input.strip()) &
            (df_data.iloc[:, 3].astype(str).str.contains(manager_input.strip(), case=False, na=False))
        ]
        
        if filtered_data.empty:
            st.error("❌ 데이터를 찾을 수 없습니다.")
        else:
            agent_row = filtered_data.iloc[0]
            
            st.write("### 📋 검색 결과")
            st.write(f"**설계사 코드:** {agent_row.iloc[0]}")
            st.write(f"**설계사명:** {agent_row.iloc[6]}")
            st.write(f"**지점:** {agent_row.iloc[5]}")
            st.write(f"**대리점:** {agent_row.iloc[22]}")
            st.write(f"**누계 실적:** {agent_row.iloc[11]}")
            
            st.success("✅ 검색 완료!")

st.write("---")
if st.button("🔄 초기화"):
    st.rerun()
