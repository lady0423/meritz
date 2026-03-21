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
    "토스": "1YOUR_TOSS_IMAGE_ID",  # ← 토스 이미지 ID 입력
    "지금융": "1YOUR_JIGEUM_IMAGE_ID",
    "브릿지": "1YOUR_BRIDGE_IMAGE_ID",
    # ... 다른 대리점 추가
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

.main {
    background-color: #0e1117;
}

.info-card {
    background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.week-card {
    background: #161b22;
    border: 2px solid #30363d;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    margin: 8px 0;
    transition: all 0.3s ease;
}

.week-card:hover {
    background: #0d1117;
    border-color: #58a6ff;
}

.week-card-current {
    background: linear-gradient(135deg, #da3633 0%, #f85149 100%);
    border: 3px solid #f85149;
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(248, 81, 73, 0.4);
}

.week-number {
    font-size: 16px;
    font-weight: 700;
    color: #79c0ff;
    margin-bottom: 8px;
}

.week-card-current .week-number {
    color: #ffffff;
    font-size: 20px;
}

.week-amount {
    font-size: 24px;
    font-weight: 900;
    color: #79c0ff;
}

.week-card-current .week-amount {
    color: #ffffff;
    font-size: 28px;
}

.target-card {
    background: #161b22;
    border-left: 4px solid #1f6feb;
    padding: 15px;
    border-radius: 6px;
    margin: 10px 0;
}

.bridge-card {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.mc-status {
    background: #161b22;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #79c0ff;
    margin: 10px 0;
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

def safe_int(value):
    """안전한 int 변환"""
    try:
        if pd.isna(value) or value == "":
            return 0
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return int(float(value))
    except:
        return 0

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
    """현재 주차 반환 (3월=1주차, 4월=2주차, ...)"""
    now = datetime.now()
    month = now.month
    if month == 3:
        return 1
    elif month == 4:
        return 2
    elif month == 5:
        return 3
    elif month == 6:
        return 4
    elif month == 7:
        return 5
    else:
        return 0

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
    """Google Drive에서 이미지 로드 (캐시 없음 - 항상 새로 로드)"""
    if not file_id or file_id.startswith("1YOUR_"):
        return None
    
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"leaflet_{file_id}.jpg")
    
    # 기존 파일 삭제
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except:
        pass
    
    download_url = f"https://drive.google.com/uc?id={file_id}"
    try:
        gdown.download(download_url, temp_file, quiet=True)
        if os.path.exists(temp_file):
            img = Image.open(temp_file)
            return img
    except:
        pass
    
    return None

# ============ 헤더 ============

col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("meritz.png"):
        logo = Image.open("meritz.png")
        st.image(logo, width=100)
    else:
        st.write("📌 로고 없음")

with col2:
    st.title("📊 실적 안내장 조회")

# 마지막 업데이트 시간
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
    manager_input = st.text_input(
        "👤 매니저명",
        autocomplete="off",
        key="manager_key"
    )

with col2:
    agent_code_input = st.text_input(
        "🔍 설계사 코드",
        autocomplete="off",
        key="agent_code_key"
    )

with col3:
    search_button = st.button("🔍 검색", key="search_btn", use_container_width=True)

# ============ 검색 로직 ============

if search_button:
    if not manager_input or not agent_code_input:
        st.warning("⚠️ 매니저명과 설계사 코드를 입력하세요.")
    else:
        # 필터링
        filtered = df_data[
            (df_data.iloc[:, 0].astype(str).str.strip() == agent_code_input.strip()) &
            (df_data.iloc[:, 3].astype(str).str.contains(manager_input.strip(), case=False, na=False))
        ]
        
        if filtered.empty:
            st.error("❌ 데이터를 찾을 수 없습니다.")
        else:
            row = filtered.iloc[0]
            
            # 데이터 추출 (열 인덱스 확인 필요)
            agent_code = safe_get_value(row, 0)  # A열
            agent_name = safe_get_value(row, 6)  # G열
            branch = safe_get_value(row, 5)  # F열
            manager_name = safe_get_value(row, 3)  # D열
            agency_name = safe_get_value(row, 22)  # W열 (대리점명)
            
            # 실적 데이터 (열 인덱스 확인 필수)
            cumulative = safe_float(safe_get_value(row, 11))  # L열 (누계)
            week1 = safe_float(safe_get_value(row, 12))  # M열
            week2 = safe_float(safe_get_value(row, 13))  # N열
            week3 = safe_float(safe_get_value(row, 14))  # O열
            week4 = safe_float(safe_get_value(row, 15))  # P열
            week5 = safe_float(safe_get_value(row, 16))  # Q열
            
            # 목표 및 부족액
            current_week = get_current_week()
            target = safe_float(safe_get_value(row, 8))  # I열 (목표)
            shortage = safe_float(safe_get_value(row, 9))  # J열 (부족액)
            
            # 브릿지 실적
            bridge_performance = safe_float(safe_get_value(row, 17))  # R열
            
            # MC+ 상태 (T열: MC+도전구간, V열: MC+부족금액)
            mc_challenge = safe_get_value(row, 19)  # T열
            mc_shortage = safe_float(safe_get_value(row, 21))  # V열
            
            # MC+ 상태 텍스트
            if pd.isna(mc_challenge) or mc_challenge == "":
                mc_status_text = "미달성"
                mc_status_color = "🔴"
            else:
                mc_status_text = str(mc_challenge)
                mc_status_color = "🟢"
            
            # ============ 결과 표시 ============
            
            st.write("---")
            st.success("✅ 검색 완료!")
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.markdown("### 📋 기본 정보")
                st.markdown(f"""
                <div class="info-card">
                    <strong>설계사 코드:</strong> {agent_code}<br>
                    <strong>설계사명:</strong> {agent_name}<br>
                    <strong>지점:</strong> {branch}<br>
                    <strong>매니저:</strong> {manager_name}<br>
                    <strong>대리점:</strong> {agency_name}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 💰 누계 실적")
                st.markdown(f"""
                <div class="info-card">
                    <div style="font-size: 32px; font-weight: 900; color: #79c0ff;">
                        {format_currency(cumulative)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📈 주차별 실적")
                weeks = [week1, week2, week3, week4, week5]
                for i, week in enumerate(weeks, 1):
                    is_current = (i == current_week)
                    card_class = "week-card-current" if is_current else "week-card"
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="week-number">{i}주차</div>
                        <div class="week-amount">{format_currency(week)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### 🎯 현재 주차 목표")
                st.markdown(f"""
                <div class="target-card">
                    <strong>목표:</strong> {format_currency(target)}<br>
                    <strong>부족액:</strong> {format_currency(shortage)}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 🌉 브릿지 실적")
                st.markdown(f"""
                <div class="bridge-card">
                    <div style="font-size: 28px; font-weight: 900;">
                        {format_currency(bridge_performance)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📊 MC+ 상태")
                st.markdown(f"""
                <div class="mc-status">
                    <strong>{mc_status_color} 상태:</strong> {mc_status_text}<br>
                    <strong>부족금액:</strong> {format_currency(mc_shortage)}
                </div>
                """, unsafe_allow_html=True)
            
            with col_right:
                st.markdown("### 📄 안내장 템플릿")
                
                # 대리점명으로 이미지 ID 조회
                image_id = LEAFLET_TEMPLATE_IDS.get(str(agency_name).strip(), None)
                
                if image_id and not image_id.startswith("1YOUR_"):
                    leaflet_img = load_leaflet_template_from_drive(image_id)
                    if leaflet_img:
                        st.image(leaflet_img, use_container_width=True)
                        
                        # JPG 다운로드 버튼
                        img_byte_arr = io.BytesIO()
                        leaflet_img.save(img_byte_arr, format='JPEG')
                        img_byte_arr.seek(0)
                        
                        st.download_button(
                            label="📥 안내장 다운로드 (JPG)",
                            data=img_byte_arr,
                            file_name=f"{agent_code}_{agency_name}_안내장.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    else:
                        st.warning(f"⚠️ 이미지를 로드할 수 없습니다. (ID: {image_id})")
                else:
                    st.info(f"📌 대리점명: {agency_name}\n이미지 ID가 설정되지 않았습니다.")
            
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
