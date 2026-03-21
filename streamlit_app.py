import streamlit as st
import pandas as pd
import gdown
import io
import tempfile
import os
from datetime import datetime
import pytz

# ============ 설정 ============
GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

LEAFLET_TEMPLATE_IDS = {
    "메가": "16l4rB2dRYkmEARfP7shI_N5L_HKio9wO",
    "토스": "17b27Cq0sN52ifJ5NvCsnr87KbaUcsqsr",
    "지금융": "19lR3nBPV6guyEIAk9xw_6GwDPO1N_wbw",
    "엠금융": "1BBJvzGqHrDWw-lFewIsBdEgk0WTVsfKq",
    "스카이블루": "1DEFjI5-pnUJM1d7uJUzmoBZLHZ4z7YPf",
    "유퍼스트": "1DPUTq6hU_M21dpliYkwSa5HQdY2J9fB3",
    "케이지에이에셋": "1E24X08TpagWpuU0AeiQK1uh57Pf7hV9G",
    "피플라이프": "1LNJw-eB_fRXLGTm7F5N7ndXx8S_wMISP",
    "더금융": "1Nj05DgH3oatnEiCGbGHQU2K1dRsVEQHh",
    "더좋은보험금융": "1Px8WawPHjME-oYAXd4TTkhIjQCFVDISc",
    "프라임에셋": "1UniyB7NEUEPhRHuqormlWrS3v_rFaYy1",
    "에이플러스": "1Z_7FNhOQJngRPiuICIwdmvJqJQw1qFwc",
    "지에이코리아": "1aH3tXtWQHCeNUitXkMua9D7sAl6x8SLz",
    "메타리치": "1kL-z0xn8vQBh5aEGkZiV3X_zYp-dYYni",
    "글로벌금융": "1oDR5WfrM1XLOca13olvpx8AwZHYRqIVF",
    "인카금융": "1r1ukWIJf3EG_pf6nhQuxwkab2CVeQdDG",
    "아너스": "1rJ7SoZJyno5b6tAurjTpkkEmissGKntj",
    "굿리치": "1vNoopxTYV5cK1zlOPlNvSGseK_dbXkXl",
    "신한금융": "1z3Ayg6mJsUeeHdebaOrWyOK4lz1-ROB_",
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf"
}

# ============ 페이지 설정 ============
st.set_page_config(page_title="실적 안내장 조회", layout="wide", initial_sidebar_state="collapsed")

# 다크 테마 CSS
st.markdown("""
    <style>
    body {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff5252;
    }
    .info-card {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============ 헤더 ============
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("metiz.png"):
        st.image("metiz.png", width=80)

with col2:
    st.title("📊 실적 안내장 조회")

# 마지막 업데이트 시간 표시
seoul_tz = pytz.timezone('Asia/Seoul')
now = datetime.now(seoul_tz)
st.caption(f"⏰ 마지막 업데이트: {now.strftime('%Y년 %m월 %d일 %H:%M:%S')}")

# ============ 안전 변환 함수 ============
def safe_float(value, default=0):
    try:
        return float(value)
    except:
        return default

def safe_int(value, default=0):
    try:
        return int(float(value))
    except:
        return default

def safe_get_value(row, index, default=0):
    try:
        return row.iloc[index] if len(row) > index else default
    except:
        return default

# ============ 데이터 로드 함수 ============
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

@st.cache_data(ttl=3600)
def load_leaflet_template_from_drive(file_id):
    try:
        from PIL import Image
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"leaflet_{file_id[:8]}.jpg")
        
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass
        
        download_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(download_url, temp_file, quiet=True)
        
        if os.path.exists(temp_file):
            with open(temp_file, 'rb') as f:
                img = Image.open(io.BytesIO(f.read()))
            try:
                os.remove(temp_file)
            except:
                pass
            return img
    except:
        pass
    return None

# ============ 데이터 로드 ============
with st.spinner("📥 데이터 로드 중..."):
    df_data = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)

if df_data is None:
    st.error("❌ 데이터를 로드할 수 없습니다.")
    st.stop()

st.success("✅ 데이터 로드 완료!")

# ============ 검색 입력 ============
st.write("---")
st.subheader("🔍 검색")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    manager_input = st.text_input("📝 매니저명", autocomplete="off")
with col2:
    agent_code_input = st.text_input("🔍 설계사 코드", autocomplete="off")
with col3:
    search_button = st.button("검색", key="search_btn")

# ============ 검색 로직 ============
if search_button:
    if not manager_input or not agent_code_input:
        st.warning("⚠️ 매니저명과 설계사 코드를 모두 입력하세요.")
    else:
        # 데이터 필터링
        filtered_data = df_data[
            (df_data.iloc[:, 0].astype(str).str.strip() == agent_code_input.strip()) &
            (df_data.iloc[:, 3].astype(str).str.contains(manager_input.strip(), case=False, na=False))
        ]
        
        if filtered_data.empty:
            st.error("❌ 해당하는 데이터를 찾을 수 없습니다.")
        else:
            agent_row = filtered_data.iloc[0]
            
            # 데이터 추출
            agent_code = safe_get_value(agent_row, 0, "")
            manager_name = safe_get_value(agent_row, 3, "")
            agent_name = safe_get_value(agent_row, 6, "")
            branch = safe_get_value(agent_row, 5, "")
            agency_name = str(safe_get_value(agent_row, 22, "")).strip()
            
            # 실적 데이터
            cumulative = safe_int(safe_get_value(agent_row, 11, 0))
            week1 = safe_int(safe_get_value(agent_row, 12, 0))
            week2 = safe_int(safe_get_value(agent_row, 13, 0))
            week3 = safe_int(safe_get_value(agent_row, 14, 0))
            week4 = safe_int(safe_get_value(agent_row, 15, 0))
            week5 = safe_int(safe_get_value(agent_row, 16, 0))
            
            week_target = safe_int(safe_get_value(agent_row, 17, 0))
            week_shortage = safe_int(safe_get_value(agent_row, 18, 0))
            
            bridge_result = safe_int(safe_get_value(agent_row, 7, 0))
            bridge_target = safe_int(safe_get_value(agent_row, 8, 0))
            bridge_shortage = safe_int(safe_get_value(agent_row, 9, 0))
            
            mc_target = safe_int(safe_get_value(agent_row, 19, 0))
            mc_shortage = safe_int(safe_get_value(agent_row, 21, 0))
            
            # ============ 결과 표시 ============
            st.write("---")
            st.success("✅ 검색 완료!")
            
            left_col, right_col = st.columns([1, 1])
            
            # ============ 왼쪽: 정보 카드 ============
            with left_col:
                st.subheader("📋 기본 정보")
                
                st.markdown(f"""
                <div class="info-card">
                <strong>설계사 코드:</strong> {agent_code}<br>
                <strong>설계사명:</strong> {agent_name}<br>
                <strong>매니저:</strong> {manager_name}<br>
                <strong>지점:</strong> {branch}<br>
                <strong>대리점:</strong> {agency_name}
                </div>
                """, unsafe_allow_html=True)
                
                # 누계 실적
                st.subheader("📊 누계 실적")
                st.markdown(f"""
                <div class="info-card">
                <h3 style="color: #ffeb3b; margin: 0;">₩ {cumulative:,}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # 주차별 실적
                st.subheader("📈 주차별 실적")
                cols = st.columns(5)
                weeks = [week1, week2, week3, week4, week5]
                for i, (col, week) in enumerate(zip(cols, weeks)):
                    with col:
                        st.metric(f"주차 {i+1}", f"₩{week:,}")
                
                # 목표/부족
                st.subheader("🎯 주차 목표 / 부족")
                col_target, col_shortage = st.columns(2)
                with col_target:
                    st.metric("목표", f"₩{week_target:,}", delta=None)
                with col_shortage:
                    st.metric("부족", f"₩{week_shortage:,}", delta=None)
                
                # 브릿지
                st.subheader("🌉 브릿지 실적")
                st.markdown(f"""
                <div class="info-card">
                <strong>실적:</strong> {bridge_result} | 
                <strong>목표:</strong> {bridge_target} | 
                <strong>부족:</strong> {bridge_shortage}
                </div>
                """, unsafe_allow_html=True)
                
                # MC+
                st.subheader("⭐ MC+ 상태")
                st.markdown(f"""
                <div class="info-card">
                <strong>목표:</strong> {mc_target} | 
                <strong>부족:</strong> {mc_shortage}
                </div>
                """, unsafe_allow_html=True)
            
            # ============ 오른쪽: 리플렛 이미지 ============
            with right_col:
                st.subheader("📄 실적 안내장")
                
                # 템플릿 선택
                template_id = LEAFLET_TEMPLATE_IDS.get(agency_name, LEAFLET_TEMPLATE_IDS["none"])
                
                with st.spinner(f"🖼️ {agency_name} 템플릿 로드 중..."):
                    template_img = load_leaflet_template_from_drive(template_id)
                
                if template_img:
                    st.image(template_img, width=400)
                    
                    # 다운로드 버튼
                    img_byte_arr = io.BytesIO()
                    template_img.save(img_byte_arr, format='JPEG', quality=100)
                    img_byte_arr.seek(0)
                    
                    st.download_button(
                        label="📥 JPG 다운로드",
                        data=img_byte_arr,
                        file_name=f"{agent_name}_{agent_code}_실적.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.warning("⚠️ 리플렛 템플릿을 로드할 수 없습니다.")
            
            # ============ 하단 기능 ============
            st.write("---")
            st.write("### 💡 기능")
            
            col_print, col_reset = st.columns([1, 1])
            
            with col_print:
                if st.button("🖨️ 인쇄"):
                    st.info("💻 브라우저의 Ctrl+P (또는 Cmd+P)를 눌러 인쇄하세요.")
            
            with col_reset:
                if st.button("🔄 초기화"):
                    st.rerun()

# ============ 푸터 ============
st.write("---")
st.caption("📌 Meritz 실적 안내장 조회 시스템 | 개인 정보 보호 중심 설계")
