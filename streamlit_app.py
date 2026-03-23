import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os
import re

# ===== 상수 정의 =====
GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

LEAFLET_TEMPLATE_IDS = {
    "메가": "1N0Aq60bQnPjg7o4GFv19lbqv3pUc57H8",
    "토스": "1Xn_hB6Xl6fojhcgyF2zVlpYtyQst5ann",
    "지금융": "1b4BIQeFKooVdC-pt0z87gVZSuYTzpY8l",
    "엠금융": "1ukqgpfA4VwELcaybWN_8MGWc8ufbLwAC",
    "스카이블루에셋": "1xPOw05Kjk0hNIeIIJ1iJE4NFVv1_yvU5",
    "유퍼스트": "1X7jZLVwEYIScZqEp_9O-UHX1kK2rPhQ3",
    "케이지에이에셋": "1faWuhu3haJ3-bjkhK3Xwlp5x60Yj063W",
    "피플라이프": "1oShjwYdKsjUvVkAMUmxAbgrmTA_v9Wna",
    "더금융": "1DeUpP_czQzEpa2JTiWyvcg_42e0FT-_Y",
    "더좋은보험": "1OLsK7oilx3OacZSw8f1VZP3pKBvYsLRj",
    "프라임에셋": "1iZie57BZYUNguiiuympKd4wsg_kkZxVt",
    "에이플러스": "1EFc4RNsiKo1Rgv0M0tAXVvALY6lC74V0",
    "지에이코리아": "1xsc5JVGxyercM0553s2Cdx5vw8PbjccS",
    "메타리치": "13MXbTMcaq0E9ugf9V4Yh1wGfNcavQSvX",
    "글로벌금융": "1rLX4jeoFvzgQCEEBaMLYWp5eSs_XdNNE",
    "인카금융": "15l_dvr73h5RwdrEEi2GP4lbVReMyj8KJ",
    "아너스": "1DrMIR4hDRcXuI3l6Ue-l4aCfP0aEP0JS",
    "굿리치": "1vNoopxTYV5cK1zlOPlNvSGseK_dbXkXl",
    "신한금융": "1XAAncz-bWC4scblwtO7sLxsprqpcmu7_",
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "none": "19ZnaS2s4X8JKv27NW9FFuMUVh32i3hc0"
}

# ===== 페이지 설정 =====
st.set_page_config(page_title="메리츠 설계사 성과 조회", layout="wide")

# ===== CSS 스타일링 =====
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        letter-spacing: -0.3px;
    }
    
    body {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    
    /* 입력 필드 스타일 - 자동완성 완벽 제거 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }
    
    /* 자동완성 완벽 제거 */
    input {
        autocomplete: "off" !important;
    }
    
    input:-webkit-autofill {
        -webkit-box-shadow: 0 0 0 1000px #1a1a1a inset !important;
        -webkit-text-fill-color: #ffffff !important;
        -webkit-transition: background-color 5000s ease-in-out 0s !important;
        transition: background-color 5000s ease-in-out 0s !important;
    }
    
    input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px #1a1a1a inset !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* 버튼 스타일 - 어두운 색상 */
    .stButton > button {
        background: linear-gradient(135deg, #4a4a4a 0%, #2a2a2a 100%) !important;
        color: #ffffff !important;
        border: 1px solid #555555 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #555555 0%, #333333 100%) !important;
        border: 1px solid #666666 !important;
    }
    
    /* 정보 박스 스타일 */
    .info-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
        border-left: 5px solid #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .info-box p {
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* 누적 성과 박스 */
    .cumulative-box {
        background: linear-gradient(135deg, #2a2410 0%, #1a1410 100%);
        border-left: 5px solid #ffdc00;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* 주차 성과 박스 */
    .weekly-box {
        background: linear-gradient(135deg, #1a2a1a 0%, #131a13 100%);
        border-left: 5px solid #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .weekly-box p {
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .weekly-current {
        background: linear-gradient(135deg, #2a2410 0%, #1a1410 100%);
        border-left: 5px solid #ffa500;
    }
    
    /* 목표 박스 */
    .target-box {
        background: linear-gradient(135deg, #1a1a2a 0%, #131320 100%);
        border-left: 5px solid #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .target-box p {
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* 브릿지 박스 */
    .bridge-box {
        background: linear-gradient(135deg, #2a1a10 0%, #1a0f00 100%);
        border-left: 5px solid #ff9f6d;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* MC 박스 */
    .mc-box {
        background: linear-gradient(135deg, #1a2a2a 0%, #131a1a 100%);
        border-left: 5px solid #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* MC+ 박스 */
    .mcplus-box {
        background: linear-gradient(135deg, #1a2a3a 0%, #131a2a 100%);
        border-left: 5px solid #66ccff;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* 제목 스타일 */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    
    h1 {
        font-size: 32px;
        margin-bottom: 20px;
    }
    
    h3 {
        font-size: 20px;
        margin-bottom: 15px;
    }
    
    h4 {
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    p {
        color: #ffffff;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* 동명이인 선택 버튼 - 어둡게 */
    .duplicate-selector {
        background-color: #1a1a1a !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin: 8px 0 !important;
        color: #ffffff !important;
    }
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #555555;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #888888;
    }
</style>
""", unsafe_allow_html=True)

# ===== 헬퍼 함수 =====
def safe_float(value):
    """안전한 float 변환"""
    try:
        return float(value) if value else 0
    except (ValueError, TypeError):
        return 0

def format_display(value):
    """숫자 포맷팅"""
    value = safe_float(value)
    if value == int(value):
        return f"{int(value):,}"
    else:
        return f"{value:,.2f}"

def get_current_week():
    """현재 주차 반환 (3월 기준)"""
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).date()
    march_start = today.replace(day=1)
    days_into_march = (today - march_start).days + 1
    
    if days_into_march <= 7:
        return 1
    elif days_into_march <= 14:
        return 2
    elif days_into_march <= 21:
        return 3
    elif days_into_march <= 28:
        return 4
    else:
        return 5

def get_image_id_by_authentic_and_partner(authentic, partner):
    """인증여부와 파트너사 기준 이미지 ID 조회"""
    if pd.isna(authentic) or pd.isna(partner):
        return LEAFLET_TEMPLATE_IDS.get("none")
    
    authentic_str = str(authentic).strip()
    partner_str = str(partner).strip()
    
    if authentic_str == "1":
        return LEAFLET_TEMPLATE_IDS.get("어센틱", LEAFLET_TEMPLATE_IDS.get("none"))
    else:
        return LEAFLET_TEMPLATE_IDS.get(partner_str, LEAFLET_TEMPLATE_IDS.get("none"))

def extract_branch_number(branch_name):
    """지점명에서 숫자 추출"""
    match = re.search(r'-(\d+)', str(branch_name))
    if match:
        return int(match.group(1))
    return 999

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    """Google Sheets에서 데이터 로드"""
    csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 이미지 로드"""
    if not file_id or file_id == "none":
        return None
    
    try:
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "leaflet.png")
        gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
        
        if os.path.exists(temp_path):
            return Image.open(temp_path)
    except Exception as e:
        st.warning(f"이미지 로드 실패: {e}")
    
    return None

def load_logo():
    """로고 로드"""
    if os.path.exists("meritz.png"):
        return Image.open("meritz.png")
    return None

def render_mc_box(status, shortage, shortage_final):
    """MC 상태 박스 렌더링"""
    status_str = str(status).strip()
    
    if status_str == "달성":
        color = "#4a9d66"
        bg = "#1a2a1a"
    elif status_str == "부족":
        color = "#ff6b6b"
        bg = "#2a1a1a"
    else:
        color = "#ffffff"
        bg = "#1a1a1a"
    
    shortage_val = format_display(shortage)
    shortage_final_val = format_display(shortage_final)
    
    return f"""
    <div style='background: {bg}; border-left: 5px solid {color}; border-radius: 8px; padding: 12px; margin: 8px 0; font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif;'>
        <p style='color: {color}; font-weight: 600; margin: 5px 0; font-size: 14px;'>상태: {status_str}</p>
        <p style='color: #ffffff; margin: 5px 0; font-size: 14px;'>도전구간: {shortage_val}</p>
        <p style='color: #ffdc00; margin: 5px 0; font-size: 14px;'>부족최종: {shortage_final_val}</p>
    </div>
    """

def display_result(row):
    """조회 결과 표시"""
    # 팁 문구 - 조회 후에만 표시
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-radius: 10px; border-left: 5px solid #ffb366; margin-bottom: 20px; font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif;'>
    <p style='color: #ffb366; font-weight: 600; font-size: 15px; margin: 0;'>💡 아래 시상안을 보고 달성 시상금을 확인하세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # 기본 정보
        st.markdown(f"""
        <div class='info-box'>
            <p><strong>지사명:</strong> {row.get('지사명', 'N/A')}</p>
            <p><strong>지점명:</strong> {row.get('지점명', 'N/A')}</p>
            <p><strong>설계사명:</strong> {row.get('설계사명', 'N/A')} ({row.get('현재대리점설계사조직코드', 'N/A')})</p>
            <p><strong>매니저:</strong> {row.get('매니저', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3월 누계 실적
        cumulative = format_display(row.get('3월실적', 0))
        st.markdown(f"""
        <div class='cumulative-box'>
            <h4 style='color: #ffdc00; margin: 0; font-size: 16px;'>💰 3월 누계 실적</h4>
            <p style='font-size: 24px; font-weight: 700; color: #ffdc00; margin: 10px 0;'>{cumulative}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 주차별 성과
        st.markdown("<h4 style='color: #ffffff; font-size: 16px;'>📊 주차별 성과</h4>", unsafe_allow_html=True)
        current_week = get_current_week()
        
        for week in range(1, 6):
            col_name = f'{week}주차'
            value = format_display(row.get(col_name, 0))
            week_class = "weekly-current" if week == current_week else "weekly-box"
            week_emoji = "⭐" if week == current_week else "📈"
            
            st.markdown(f"""
            <div class='{week_class}'>
                <p style='color: #ffffff; margin: 5px 0; font-size: 14px;'>{week_emoji} {week}주차: <strong>{value}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # 당주 목표
        target = format_display(row.get('주차목표', 0))
        shortage = format_display(row.get('주차부족', 0))
        
        st.markdown(f"""
        <div class='target-box'>
            <h4 style='color: #ffffff; margin: 0; font-size: 16px;'>🎯 당주 목표</h4>
            <p style='color: #ffffff; margin: 5px 0; font-size: 14px;'>목표: <strong>{target}</strong></p>
            <p style='color: #ffdc00; margin: 5px 0; font-size: 14px;'>부족: <strong>{shortage}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # 브릿지 (인증 아닌 경우만)
        authentic = str(row.get('어센틱구분', '0')).strip()
        if authentic != "1":
            st.markdown("<h4 style='color: #ffffff; font-size: 16px;'>🌉 브릿지 성과</h4>", unsafe_allow_html=True)
            bridge_status = str(row.get('브릿지 달성구간', '')).strip()
            bridge_shortage = format_display(row.get('브릿지 도전구간', 0))
            bridge_shortage_final = format_display(row.get('브릿지 부족', 0))
            
            st.markdown(render_mc_box(bridge_status, bridge_shortage, bridge_shortage_final), unsafe_allow_html=True)
        
        # MC (인증인 경우만)
        if authentic == "1":
            st.markdown("<h4 style='color: #ffffff; font-size: 16px;'>💎 MC 성과</h4>", unsafe_allow_html=True)
            mc_status = str(row.get('MC도전구간', '')).strip()
            mc_shortage = format_display(row.get('MC부족', 0))
            mc_shortage_final = format_display(row.get('MC부족최종', 0))
            
            st.markdown(render_mc_box(mc_status, mc_shortage, mc_shortage_final), unsafe_allow_html=True)
        
        # MC+ (모두)
        st.markdown("<h4 style='color: #ffffff; font-size: 16px;'>🚀 MC PLUS + 성과</h4>", unsafe_allow_html=True)
        mcplus_status = str(row.get('MC+구간', '')).strip()
        mcplus_shortage = format_display(row.get('MC부족', 0))
        mcplus_shortage_final = format_display(row.get('MC부족최종', 0))
        
        st.markdown(render_mc_box(mcplus_status, mcplus_shortage, mcplus_shortage_final), unsafe_allow_html=True)
    
    with col_right:
        # 리플렛 이미지
        st.markdown("<h4 style='color: #ffffff; font-size: 16px;'>📄 대리점 리플렛</h4>", unsafe_allow_html=True)
        
        authentic = str(row.get('어센틱구분', '0')).strip()
        partner = row.get('대리점', 'none')
        image_id = get_image_id_by_authentic_and_partner(authentic, partner)
        
        leaflet_image = load_leaflet_template_from_drive(image_id)
        
        if leaflet_image:
            st.image(leaflet_image, use_container_width=True)
            
            # 다운로드 버튼
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                leaflet_image.save(tmp_file.name)
                with open(tmp_file.name, "rb") as f:
                    st.download_button(
                        label="📥 리플렛 다운로드",
                        data=f.read(),
                        file_name=f"leaflet_{row.get('설계사명', 'unknown')}.png",
                        mime="image/png"
                    )
        else:
            st.info("리플렛 이미지를 불러올 수 없습니다.")

# ===== 메인 UI =====
logo = load_logo()
if logo:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo, width=100)
    with col2:
        st.title("메리츠 설계사 성과 조회")
else:
    st.title("메리츠 설계사 성과 조회")

# 데이터 로드
df = load_data_from_google_sheets()

if df is None:
    st.error("데이터를 로드할 수 없습니다.")
else:
    # 세션 상태 초기화
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = None
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    
    # 입력 필드
    st.markdown("<h3 style='color: #ffffff; font-size: 20px;'>🔍 설계사 정보 조회</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<label style='color: #ffffff; font-weight: 600; font-size: 14px;'>1️⃣ 지점명</label>", unsafe_allow_html=True)
        branches = sorted(df["지점명"].dropna().unique(), key=extract_branch_number)
        default_branch = "GA4-2지점" if "GA4-2지점" in branches else (branches[0] if branches else "")
        selected_branch = st.selectbox("지점 선택", branches, index=list(branches).index(default_branch) if default_branch in branches else 0, label_visibility="collapsed")
    
    with col2:
        st.markdown("<label style='color: #ffffff; font-weight: 600; font-size: 14px;'>2️⃣ 매니저명</label>", unsafe_allow_html=True)
        manager_name = st.text_input("매니저명 입력", placeholder="박메리", label_visibility="collapsed", key="manager_input", autocomplete="off")
    
    with col3:
        st.markdown("<label style='color: #ffffff; font-weight: 600; font-size: 14px;'>3️⃣ 설계사명</label>", unsafe_allow_html=True)
        agent_name = st.text_input("설계사명 입력", placeholder="홍길동", label_visibility="collapsed", key="agent_input", autocomplete="off")
    
    # 검색 버튼
    search_col1, search_col2, search_col3 = st.columns([1, 1, 1])
    with search_col2:
        search_clicked = st.button("🔍 검색", use_container_width=True)
    
    # 엔터 키 감지 (검색 실행)
    if manager_name and agent_name:
        # 실제 엔터 감지는 어려우므로, 값 변경 감지로 처리
        pass
    
    # 검색 로직
    def perform_search():
        if not selected_branch or not manager_name or not agent_name:
            st.error("⚠️ 지점명, 매니저명, 설계사명을 모두 입력해주세요.")
            return
        
        filtered = df[
            (df['지점명'].astype(str).str.strip() == selected_branch.strip()) &
            (df['매니저'].astype(str).str.strip() == manager_name.strip()) &
            (df['설계사명'].astype(str).str.strip() == agent_name.strip())
        ]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {selected_branch} / {manager_name} / {agent_name}")
        elif len(filtered) == 1:
            st.session_state.selected_agent = filtered.iloc[0]
            st.session_state.show_result = True
        else:
            st.markdown("<p style='color: #ffffff; font-weight: 600; margin-top: 20px; font-size: 14px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
            
            for idx, (_, agent_row) in enumerate(filtered.iterrows()):
                agent_display = f"{agent_row.get('지사명', 'N/A')} - {agent_row.get('설계사명', 'N/A')} ({agent_row.get('현재대리점설계사조직코드', 'N/A')})"
                
                if st.button(agent_display, key=f"agent_{idx}", use_container_width=True):
                    st.session_state.selected_agent = agent_row
                    st.session_state.show_result = True
                    st.rerun()
    
    if search_clicked:
        perform_search()
    
    # 조회 결과 표시
    if st.session_state.show_result and st.session_state.selected_agent is not None:
        display_result(st.session_state.selected_agent)
    
    # 초기화 버튼
    col_reset1, col_reset2, col_reset3 = st.columns([1, 1, 1])
    with col_reset2:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.selected_agent = None
            st.session_state.show_result = False
            st.rerun()
