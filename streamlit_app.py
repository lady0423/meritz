import streamlit as st
import pandas as pd
import gdown
import tempfile
import os
from datetime import datetime
import pytz
from PIL import Image
import io

# ============ 설정 ============
GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

# 대리점명 → Google Drive 이미지 ID 매핑
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
    "더좋은보험": "1Px8WawPHjME-oYAXd4TTkhIjQCFVDISc",
    "프라임에셋": "1UniyB7NEUEPhRHuqormlWrS3v_rFaYy1",
    "에이플러스": "1Z_7FNhOQJngRPiuICIwdmvJqJQw1qFwc",
    "지에이코리아": "1aH3tXtWQHCeNUitXkMua9D7sAl6x8SLz",
    "메타리치": "1kL-z0xn8vQBh5aEGkZiV3X_zYp-dYYni",
    "글로벌금융": "1oDR5WfrM1XLOca13olvpx8AwZHYRqIVF",
    "인카금융": "1r1ukWIJf3EG_pf6nhQuxwkab2CVeQdDG",
    "아너스": "1rJ7SoZJyno5b6tAurjTpkkEmissGKntj",
    "굿리치": "1vNoopxTYV5cK1zlOPlNvSGseK_dbXkXl",
    "신한금융": "1z3Ayg6mJsUeeHdebaOrWyOK4lz1-ROB_",
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
}

# 페이지 설정
st.set_page_config(page_title="실적 안내장 조회", layout="wide", initial_sidebar_state="collapsed")

# CSS 스타일링
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

* {
    font-family: 'Noto Sans KR', sans-serif;
}

body {
    background-color: #0e1117;
    color: #c9d1d9;
}

.header-title {
    font-size: 28px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 20px;
}

.section-header {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 20px;
    margin-bottom: 10px;
}

.basic-info-box {
    background: #161b22;
    border: 1px solid #30363d;
    padding: 12px 15px;
    border-radius: 6px;
    margin: 5px 0;
    font-size: 14px;
    line-height: 1.8;
}

.cumulative-box {
    background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
    padding: 12px 15px;
    border-radius: 8px;
    color: white;
    margin: 10px 0;
    text-align: center;
}

.cumulative-value {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
}

.week-row {
    background: #161b22;
    border: 1px solid #30363d;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 6px 0;
    border-radius: 6px;
    padding: 12px 15px;
}

.week-row-current {
    background: linear-gradient(135deg, #da3633 0%, #f85149 100%);
    border: 2px solid #f85149;
    box-shadow: 0 4px 12px rgba(248, 81, 73, 0.3);
}

.week-label {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}

.week-amount {
    font-size: 20px;
    font-weight: 900;
    color: #79c0ff;
}

.week-row-current .week-amount {
    color: #ffffff;
    font-size: 24px;
}

.bridge-box {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
    padding: 15px;
    border-radius: 8px;
    color: white;
    margin: 10px 0;
}

.bridge-label {
    font-size: 14px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 8px;
    font-weight: 600;
}

.bridge-value {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 12px;
}

.bridge-section {
    background: rgba(0,0,0,0.2);
    padding: 12px;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    gap: 15px;
}

.bridge-info-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.bridge-section-label {
    font-size: 13px;
    color: rgba(255,255,255,0.7);
}

.bridge-section-value {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
}

.mc-box {
    background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
    padding: 15px;
    border-radius: 8px;
    color: white;
    margin: 10px 0;
}

.mc-label {
    font-size: 14px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 8px;
    font-weight: 600;
}

.mc-value {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 12px;
}

.mc-info {
    background: rgba(0,0,0,0.15);
    padding: 12px;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
}

.mc-info-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.mc-info-label {
    color: rgba(255,255,255,0.7);
    font-size: 13px;
}

.mc-info-value {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
}

.leaflet-placeholder {
    background: #161b22;
    border: 2px dashed #30363d;
    padding: 40px;
    border-radius: 8px;
    text-align: center;
    color: #8b949e;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ============ 유틸 함수 ============

def safe_float(value):
    """안전한 float 변환"""
    try:
        if pd.isna(value) or value == "":
            return 0.0
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value)
    except:
        return 0.0

def safe_get_value(row, col_index):
    """행에서 값 추출 (안전)"""
    try:
        if col_index < len(row):
            return row.iloc[col_index]
        return ""
    except:
        return ""

def format_currency(value):
    """통화 형식 (₩1,000)"""
    try:
        value = safe_float(value)
        return f"₩{value:,.0f}"
    except:
        return "₩0"

def get_current_week():
    """현재 주차 반환 (월별 자동 계산)"""
    now = datetime.now()
    month = now.month
    day = now.day
    
    # 월별 주차 매핑 (첫 주는 1-7일, 두 번째 주는 8-14일 등)
    week = (day - 1) // 7 + 1
    
    # 월별 시작 주차
    if month == 3:
        return week  # 3월 1-7일 = 1주차
    elif month == 4:
        return week  # 4월 1-7일 = 1주차
    elif month == 5:
        return week  # 5월 1-7일 = 1주차
    elif month == 6:
        return week  # 6월 1-7일 = 1주차
    elif month == 7:
        return week  # 7월 1-7일 = 1주차
    else:
        return 0

def get_image_id_by_agency_name(agency_name_full):
    """
    대리점명에서 키워드를 찾아서 이미지 ID 반환
    예: "토스인슈어런스 주식회사" → "토스" 포함 → 토스 이미지 ID 반환
    """
    agency_name_full = str(agency_name_full).strip().lower()
    
    # LEAFLET_TEMPLATE_IDS의 키들을 확인
    for keyword, image_id in LEAFLET_TEMPLATE_IDS.items():
        keyword_lower = keyword.lower()
        # 대리점명에 키워드가 포함되어 있는지 확인
        if keyword_lower in agency_name_full:
            return image_id
    
    # 일치하는 키워드가 없으면 None 반환
    return None

# ============ 데이터 로드 ============

@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    """Google Drive에서 Excel 데이터 로드"""
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

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 이미지 로드"""
    if not file_id:
        return None
    
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"leaflet_{file_id}.jpg")
    
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except:
        pass
    
    download_url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(download_url, temp_file, quiet=True, timeout=15)
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
            img = Image.open(temp_file)
            return img
    except Exception as e:
        pass
    
    return None

# ============ 헤더 ============

col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("meritz.png"):
        logo = Image.open("meritz.png")
        st.image(logo, width=100)

with col2:
    st.markdown('<div class="header-title">📊 실적 안내장 조회</div>', unsafe_allow_html=True)

kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"⏰ 마지막 업데이트: {now_kst}")

# ============ 데이터 로드 ============

st.write("---")
with st.spinner("📥 데이터 로드 중..."):
    df_data = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)

if df_data is None:
    st.error("❌ 데이터를 로드할 수 없습니다.")
    st.stop()

st.success("✅ 데이터 로드 완료!")

# ============ 검색 UI ============

st.write("---")
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    manager_input = st.text_input("👤 매니저명", autocomplete="off", key="manager_key")

with col2:
    agent_code_input = st.text_input("🔍 설계사 코드", autocomplete="off", key="agent_code_key")

with col3:
    search_button = st.button("🔍 검색", key="search_btn", use_container_width=True)

# ============ 검색 로직 ============

if search_button:
    if not manager_input or not agent_code_input:
        st.warning("⚠️ 매니저명과 설계사 코드를 입력하세요.")
    else:
        filtered = df_data[
            (df_data.iloc[:, 0].astype(str).str.strip() == agent_code_input.strip()) &
            (df_data.iloc[:, 3].astype(str).str.contains(manager_input.strip(), case=False, na=False))
        ]
        
        if filtered.empty:
            st.error("❌ 데이터를 찾을 수 없습니다.")
        else:
            row = filtered.iloc[0]
            
            # 데이터 추출
            agent_code = safe_get_value(row, 0)
            agent_name = safe_get_value(row, 6)
            branch = safe_get_value(row, 5)
            manager_name = safe_get_value(row, 3)
            agency_name = safe_get_value(row, 22)
            
            cumulative = safe_float(safe_get_value(row, 11))
            week1 = safe_float(safe_get_value(row, 12))
            week2 = safe_float(safe_get_value(row, 13))
            week3 = safe_float(safe_get_value(row, 14))
            week4 = safe_float(safe_get_value(row, 15))
            week5 = safe_float(safe_get_value(row, 16))
            
            # 브릿지: H열(실적), I열(목표), J열(부족금액)
            bridge_progress = safe_float(safe_get_value(row, 7))
            bridge_target = safe_float(safe_get_value(row, 8))
            bridge_shortage = safe_float(safe_get_value(row, 9))
            
            mc_challenge = safe_get_value(row, 19)
            mc_shortage = safe_float(safe_get_value(row, 21))
            
            current_week = get_current_week()
            
            st.write("---")
            st.success("✅ 검색 완료!")
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                # 기본 정보
                st.markdown('<div class="section-header">📋 기본 정보</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="basic-info-box">
                <strong>설계사 코드:</strong> {agent_code}<br>
                <strong>설계사명:</strong> {agent_name}<br>
                <strong>지사:</strong> {branch}<br>
                <strong>매니저:</strong> {manager_name}
                </div>
                """, unsafe_allow_html=True)
                
                # 누계 실적
                st.markdown('<div class="section-header">💰 누계 실적</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="cumulative-box">
                    <div class="cumulative-value">{format_currency(cumulative)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 주차별 실적
                st.markdown('<div class="section-header">📈 주차별 실적</div>', unsafe_allow_html=True)
                weeks = [week1, week2, week3, week4, week5]
                for i, week in enumerate(weeks, 1):
                    is_current = (i == current_week)
                    row_class = "week-row week-row-current" if is_current else "week-row"
                    st.markdown(f"""
                    <div class="{row_class}">
                        <div class="week-label">{i}주차</div>
                        <div class="week-amount">{format_currency(week)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 브릿지 실적
                st.markdown('<div class="section-header">🌉 브릿지 실적</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="bridge-box">
                    <div class="bridge-label">목표</div>
                    <div class="bridge-value">{format_currency(bridge_target)}</div>
                    <div class="bridge-section">
                        <div class="bridge-info-item">
                            <div class="bridge-section-label">진척</div>
                            <div class="bridge-section-value">{format_currency(bridge_progress)}</div>
                        </div>
                        <div class="bridge-info-item">
                            <div class="bridge-section-label">부족</div>
                            <div class="bridge-section-value">{format_currency(bridge_shortage)}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # MC+ 상태
                st.markdown('<div class="section-header">📊 MC+ 상태</div>', unsafe_allow_html=True)
                mc_status_text = str(mc_challenge) if (mc_challenge and str(mc_challenge).strip() != "") else "미달성"
                st.markdown(f"""
                <div class="mc-box">
                    <div class="mc-label">도전구간</div>
                    <div class="mc-value">{mc_status_text}</div>
                    <div class="mc-info">
                        <div class="mc-info-item">
                            <div class="mc-info-label">부족금액</div>
                            <div class="mc-info-value">{format_currency(mc_shortage)}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_right:
                st.markdown('<div class="section-header">📄 안내장 템플릿</div>', unsafe_allow_html=True)
                
                agency_name_str = str(agency_name).strip()
                # 자동 매칭 함수 사용 (대리점명에 포함된 키워드로 검색)
                image_id = get_image_id_by_agency_name(agency_name_str)
                
                if image_id:
                    with st.spinner(f"🔄 {agency_name_str} 안내장 로드 중..."):
                        leaflet_img = load_leaflet_template_from_drive(image_id)
                    
                    if leaflet_img:
                        st.image(leaflet_img, use_container_width=True)
                        
                        img_byte_arr = io.BytesIO()
                        leaflet_img.save(img_byte_arr, format='JPEG')
                        img_byte_arr.seek(0)
                        
                        st.download_button(
                            label="📥 안내장 다운로드 (JPG)",
                            data=img_byte_arr,
                            file_name=f"{agent_code}_{agency_name_str}_안내장.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    else:
                        st.markdown(f"""
                        <div class="leaflet-placeholder">
                            ⚠️ 이미지를 로드할 수 없습니다.<br><br>
                            <strong>대리점:</strong> {agency_name_str}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="leaflet-placeholder">
                        📌 대리점명: {agency_name_str}<br><br>
                        이 대리점의 이미지가 설정되지 않았습니다.
                    </div>
                    """, unsafe_allow_html=True)
            
            st.write("---")
            col_print, col_reset = st.columns([1, 1])
            with col_print:
                st.button("🖨️ 인쇄", key="print_btn", use_container_width=True)
            with col_reset:
                if st.button("🔄 초기화", key="reset_btn", use_container_width=True):
                    st.rerun()

st.markdown("""
---
<div style="text-align: center; color: #8b949e; font-size: 12px;">
💡 설계사 코드와 매니저명을 입력하고 검색 버튼을 클릭하세요.
</div>
""", unsafe_allow_html=True)
