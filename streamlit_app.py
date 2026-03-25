undefinedimport streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os

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

PASSWORD = "2603"

st.set_page_config(page_title="메리츠 실적현황", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
* {
    font-family: 'Noto Sans KR', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stDecoration"] {
    background: #f8f9fa !important;
    color: #2c3e50;
}

[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0.95) !important;
}

h1, h2, h3 {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #2c3e50;
}

input::-webkit-autofill,
input::-webkit-autofill:hover,
input::-webkit-autofill:focus,
input::-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #ffffff inset !important;
    box-shadow: 0 0 0 30px #ffffff inset !important;
}

input::-webkit-autofill {
    -webkit-text-fill-color: #2c3e50 !important;
}

.stButton > button {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(74, 85, 104, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    box-shadow: 0 4px 15px rgba(74, 85, 104, 0.4);
    transform: translateY(-2px);
}

.info-box {
    background: white;
    border-left: 4px solid #4a5568;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 500;
    color: #2c3e50;
}

.contact-box {
    background: white;
    border-left: 4px solid #48bb78;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 500;
    color: #2c3e50;
}

.cumulative-box {
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    padding: 16px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 22px;
    font-weight: 700;
    color: white;
    text-align: center;
    box-shadow: 0 2px 12px rgba(74, 85, 104, 0.25);
    letter-spacing: 0.5px;
}

.weekly-row {
    background: white;
    border-left: 4px solid #48bb78;
    padding: 10px 12px;
    border-radius: 8px;
    margin: 6px 0;
    font-size: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 600;
    color: #2c3e50;
}

.weekly-row.current {
    background: linear-gradient(135deg, #ffd93d 0%, #ffb93d 100%);
    border-left: 4px solid #f59e0b;
    box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
    color: #92400e;
}

.bridge-box {
    background: white;
    border-left: 4px solid #ed64a6;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 600;
    color: #2c3e50;
}

.mc-box {
    background: white;
    border-left: 4px solid #fc8181;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 600;
    color: #2c3e50;
}

.mc-plus-box {
    background: white;
    border-left: 4px solid #805ad5;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 600;
    color: #2c3e50;
}

.target-box {
    background: white;
    border-left: 4px solid #ed8936;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    font-weight: 600;
    color: #2c3e50;
}

.search-label {
    font-weight: 600;
    font-size: 13px;
    color: #4a5568;
    margin-bottom: 6px;
    display: block;
}

input, select {
    background-color: #ffffff !important;
    color: #2c3e50 !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s ease;
}

input:focus, select:focus {
    border-color: #4a5568 !important;
    box-shadow: 0 0 0 3px rgba(74, 85, 104, 0.1) !important;
    outline: none !important;
}

input::placeholder {
    color: #a0aec0 !important;
}

.stTextInput > label, .stSelectbox > label {
    font-weight: 600;
    color: #4a5568;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 14px;
}

[data-baseweb="select"] {
    width: 100%;
}

[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    min-height: 40px;
}

[data-baseweb="select"] > div > div {
    color: #2c3e50 !important;
    font-weight: 500 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    padding: 10px 20px;
    border-radius: 8px 8px 0 0;
    background-color: #e2e8f0;
    color: #4a5568;
}

.stTabs [aria-selected="true"] {
    background-color: #4a5568;
    color: white;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

.login-box {
    max-width: 320px;
    margin: 30px auto;
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.login-box h2 {
    font-size: 18px;
    margin-bottom: 15px;
}

.login-box input {
    font-size: 14px !important;
    padding: 8px !important;
}

h3 {
    font-size: 16px !important;
    margin-top: 12px !important;
    margin-bottom: 8px !important;
}

</style>
""", unsafe_allow_html=True)

def safe_float(value):
    if pd.isna(value):
        return 0.0
    if value == "" or value is None:
        return 0.0
    try:
        v = str(value).strip()
        if v == "":
            return 0.0
        if "만원" in v:
            num_part = v.replace("만원", "").strip()
            return float(num_part) * 10000
        return float(v.replace(",", ""))
    except:
        return 0.0

def format_display(value):
    v = str(value).strip()
    if v == "" or v == "nan":
        return "₩ 0"
    try:
        if "만원" in v:
            num_part = v.replace("만원", "").strip()
            num = float(num_part) * 10000
            return f"₩ {num:,.0f}"
        num = float(v.replace(",", ""))
        return f"₩ {num:,.0f}"
    except:
        return v

def get_current_week():
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst).date()
    day = today.day
    
    if today.month == 3:
        if day <= 1:
            return 0
        elif day <= 8:
            return 1
        elif day <= 15:
            return 2
        elif day <= 22:
            return 3
        elif day <= 29:
            return 4
        else:
            return 5
    return 4

def get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel, agency_name):
    if is_authentic:
        if is_partner_channel:
            return LEAFLET_TEMPLATE_IDS.get("none")
        else:
            return LEAFLET_TEMPLATE_IDS.get("어센틱")
    else:
        agency_name_lower = str(agency_name).strip().lower()
        for keyword, image_id in LEAFLET_TEMPLATE_IDS.items():
            if keyword.lower() in agency_name_lower:
                return image_id
        return LEAFLET_TEMPLATE_IDS.get("none")

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

@st.cache_data(ttl=300)
def load_contact_data_from_google_sheets():
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=1995676008"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"전화번호 데이터 로드 실패: {e}")
        return None

def create_vcard(name, phone, company, title, department):
    """vCard 파일 생성"""
    phone_clean = phone.replace("-", "").replace(" ", "")
    
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone_clean}
ORG:{company}
TITLE:{title}
NOTE:부서: {department}
END:VCARD"""
    
    return vcard

def load_leaflet_template_from_drive(file_id):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "template.jpg")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=True)
            if os.path.exists(output_path):
                return Image.open(output_path)
    except:
        pass
    return None

def load_logo():
    if os.path.exists("meritz.png"):
        return Image.open("meritz.png")
    return None

def render_mc_box(mc_challenge, mc_shortage, is_authentic=False, is_mc_plus=False):
    mc_challenge_display = format_display(mc_challenge)
    mc_shortage_display = format_display(mc_shortage)
    
    mc_shortage_val = safe_float(mc_shortage)
    shortage_str = str(mc_shortage).strip()
    
    if "최종달성" in shortage_str:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#48bb78"
    elif "다음기회에" in shortage_str or "재도전" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#718096"
    elif "대상아님" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#718096"
    elif "미달성" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#718096"
    elif is_authentic and not is_mc_plus and "전월" in str(mc_challenge):
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#718096"
    elif mc_shortage_val < 0:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#48bb78"
    elif mc_shortage_val == 0:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#48bb78"
    else:
        mc_display_status = "🟡 도전중"
        mc_shortage_color = "#ed8936"
    
    box_class = "mc-plus-box" if is_mc_plus else "mc-box"
    status_color = "#805ad5" if is_mc_plus else "#ed8936"
    
    st.markdown(f"""
    <div class='{box_class}'>
    <strong>도전구간 →</strong> {mc_challenge_display}<br>
    <strong>부족금액 →</strong> <span style='color: {mc_shortage_color}; font-weight: 700;'>{mc_shortage_display}</span><br>
    <strong>상태 →</strong> <span style='color: {status_color}; font-weight: 700;'>{mc_display_status}</span>
    </div>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'show_duplicates' not in st.session_state:
    st.session_state.show_duplicates = False
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'last_search_params' not in st.session_state:
    st.session_state.last_search_params = {'branch': '', 'agent': ''}
if 'contact_search_performed' not in st.session_state:
    st.session_state.contact_search_performed = False
if 'contact_selected_row' not in st.session_state:
    st.session_state.contact_selected_row = None

# 로그인 화면
if not st.session_state.authenticated:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        logo = load_logo()
        if logo:
            st.image(logo, width=60)
    
    with col_title:
        st.markdown("<h1 style='color: #2c3e50; font-size: 24px; margin-top: 5px;'>메리츠 설계사 성과 조회</h1>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 10px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='login-box'>
    <h2 style='text-align: center; color: #4a5568;'>🔐 로그인</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        password_input = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력", label_visibility="collapsed")
        
        if st.button("로그인", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")
    
    st.stop()

# 로그인 후 메인 화면
col_logo, col_title = st.columns([1, 4])
with col_logo:
    logo = load_logo()
    if logo:
        st.image(logo, width=60)
    else:
        st.write("📊")

with col_title:
    st.markdown("<h1 style='color: #2c3e50; font-size: 24px; margin-top: 5px;'>메리츠 설계사 성과 조회</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 8px 0;'>", unsafe_allow_html=True)

# 탭 생성
tab1, tab2 = st.tabs(["📊 실적조회", "📞 전화번호 조회"])

# ==================== 탭1: 실적조회 ====================
with tab1:
    df = load_data_from_google_sheets()
    if df is None:
        st.stop()

    current_week = get_current_week()

    st.markdown("<h3 style='color: #4a5568; margin-top: 12px; margin-bottom: 12px; font-size: 16px;'>🔍 검색 정보 입력</h3>", unsafe_allow_html=True)

    ga4_branches = [f"GA4-{i}지점" for i in range(1, 14)]
    default_idx = 1

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown("<div class='search-label'>📍 지점명</div>", unsafe_allow_html=True)
        selected_branch = st.selectbox("지점명", ga4_branches, index=default_idx, label_visibility="collapsed", key="branch")

    with col2:
        st.markdown("<div class='search-label'>👔 설계사명</div>", unsafe_allow_html=True)
        agent_name = st.text_input("설계사명", placeholder="예: 홍길동", label_visibility="collapsed", key="agent", autocomplete="off")

    with col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        search_clicked = st.button("🔍 검색", use_container_width=True)

    current_params = {
        'branch': selected_branch,
        'agent': agent_name
    }

    if current_params != st.session_state.last_search_params:
        st.session_state.search_performed = False
        st.session_state.selected_row = None
        st.session_state.show_duplicates = False
        st.session_state.filtered_data = None
        st.session_state.last_search_params = current_params.copy()

    if search_clicked:
        if not agent_name:
            st.error("⚠️ 설계사명을 입력해주세요.")
            st.session_state.search_performed = False
            st.session_state.show_duplicates = False
        else:
            filtered = df[(df["지점명"].astype(str).str.strip() == selected_branch.strip()) &
                          (df["설계사명"].astype(str).str.strip() == agent_name.strip())]
            
            if len(filtered) == 0:
                st.error(f"❌ 데이터를 찾을 수 없습니다")
                st.session_state.search_performed = False
                st.session_state.show_duplicates = False
            elif len(filtered) == 1:
                st.session_state.search_performed = True
                st.session_state.selected_row = filtered.iloc[0]
                st.session_state.show_duplicates = False
            else:
                st.session_state.show_duplicates = True
                st.session_state.filtered_data = filtered
                st.session_state.search_performed = False

    if st.session_state.show_duplicates and st.session_state.filtered_data is not None:
        st.markdown("<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
        
        for idx, (_, agent_row) in enumerate(st.session_state.filtered_data.iterrows()):
            agency_branch = str(agent_row.get('지사명','N/A')).strip()
            agent_display_name = str(agent_row.get('설계사명','N/A')).strip()
            agent_code = str(agent_row.get('현재대리점설계사조직코드','N/A')).strip()
            
            agent_display = f"{agency_branch} - {agent_display_name} ({agent_code})"
            if st.button(agent_display, key=f"agent_{idx}", use_container_width=True):
                st.session_state.search_performed = True
                st.session_state.selected_row = agent_row
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None

    if st.session_state.search_performed and st.session_state.selected_row is not None:
        row = st.session_state.selected_row
        
        agent_name_display = str(row["설계사명"]).strip()
        agent_code = str(row.get("현재대리점설계사조직코드", "N/A")).strip()
        agency_branch = str(row.get("지사명", "N/A")).strip()
        agency_name = str(row["대리점"]).strip()
        branch = str(row["지점명"]).strip()
        
        is_authentic = safe_float(row["어센틱구분"]) == 1
        is_partner_channel = "파트너채널" in branch
        
        col_left, col_right = st.columns([1.5, 1])
        
        with col_left:
            st.markdown("""
            <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%); border-radius: 8px; margin-bottom: 12px; box-shadow: 0 2px 6px rgba(74, 85, 104, 0.2);'>
            <p style='color: white; font-weight: 600; font-size: 13px; margin: 0;'>💡 대리점 시상안을 보고 달성 시상금을 확인하세요</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h3 style='color: #4a5568;'>📋 기본 정보</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
            <strong>지사명:</strong> {agency_branch}<br>
            <strong>설계사명(코드):</strong> {agent_name_display} ({agent_code})
            </div>
            """, unsafe_allow_html=True)
            
            cumulative = row["누계실적"]
            st.markdown("<h3 style='color: #4a5568;'>📈 3월 누계 실적</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='cumulative-box'>
            {format_display(cumulative)}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #4a5568;'>📅 주차별 실적</h3>", unsafe_allow_html=True)
            
            week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
            for idx, week_col in enumerate(week_columns, 1):
                week_value = row[week_col]
                is_current = (idx == current_week)
                
                if is_current:
                    st.markdown(f"""
                    <div class='weekly-row current'>
                    <div><strong>{week_col}</strong> ⭐</div>
                    <strong style='color: #92400e;'>{format_display(week_value)}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='weekly-row'>
                    <strong>{week_col}</strong> <strong style='color: #48bb78;'>{format_display(week_value)}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #4a5568;'>⭐ 현재주차 목표</h3>", unsafe_allow_html=True)
            
            if is_authentic:
                weekly_target_raw = row.get("어센틱주차목표", "0")
                weekly_shortage_raw = row.get("어센틱주차부족", "0")
            else:
                weekly_target_raw = row.get("주차목표", "0")
                weekly_shortage_raw = row.get("주차부족최종", "0")
            
            st.markdown(f"""
            <div class='target-box'>
            <strong>목표 →</strong> {format_display(weekly_target_raw)}<br>
            <strong>부족금액 →</strong> {format_display(weekly_shortage_raw)}
            </div>
            """, unsafe_allow_html=True)
            
            if not is_authentic:
                st.markdown("<h3 style='color: #4a5568;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
                bridge_target = row["브릿지 도전구간"]
                bridge_shortage = row["브릿지부족최종"]
                
                st.markdown(f"""
                <div class='bridge-box'>
                <strong>목표 →</strong> {format_display(bridge_target)}<br>
                <strong>부족금액 →</strong> {format_display(bridge_shortage)}
                </div>
                """, unsafe_allow_html=True)
            
            if is_authentic:
                st.markdown("<h3 style='color: #4a5568;'>💰 MC 성과</h3>", unsafe_allow_html=True)
                mc_challenge = row["MC도전구간"]
                mc_shortage = row["MC부족최종"]
                render_mc_box(mc_challenge, mc_shortage, is_authentic=True, is_mc_plus=False)
            
            st.markdown("<h3 style='color: #805ad5;'>💰 MC PLUS+ 성과</h3>", unsafe_allow_html=True)
            mc_plus_challenge = row["MC+구간"]
            mc_plus_shortage = row["MC+부족최종"]
            render_mc_box(mc_plus_challenge, mc_plus_shortage, is_authentic=is_authentic, is_mc_plus=True)
        
        with col_right:
            st.markdown("<h3 style='color: #4a5568;'>🎁 대리점 리플렛</h3>", unsafe_allow_html=True)
            image_id = get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel, agency_name)
            image = load_leaflet_template_from_drive(image_id)
            
            if image:
                st.image(image, use_container_width=True)
                
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    image.save(tmp_file.name, "JPEG")
                    with open(tmp_file.name, "rb") as f:
                        st.download_button(
                            label="📥 리플렛 다운로드",
                            data=f.read(),
                            file_name=f"{agency_name}_leaflet.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
            else:
                st.info(f"⚠️ 리플렛 이미지를 불러올 수 없습니다.\n(대리점: {agency_name})")
        
        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
        
        if st.button("🔄 초기화", use_container_width=True, key="reset_performance"):
            st.session_state.search_performed = False
            st.session_state.selected_row = None
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None

    elif not st.session_state.show_duplicates:
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);'>
        <p style='color: #4a5568; font-weight: 600; font-size: 15px; margin-bottom: 8px;'>🔒 지점명과 설계사명을 입력하고 검색 버튼을 클릭하세요.</p>
        <p style='color: #718096; font-weight: 400; font-size: 13px; margin-top: 8px;'>개인정보 보호를 위해 검색 후에만 데이터가 표시됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 탭2: 전화번호 조회 ====================
with tab2:
    contact_df = load_contact_data_from_google_sheets()
    
    if contact_df is None:
        st.error("❌ 전화번호 데이터를 불러올 수 없습니다.")
        st.stop()
    
    st.markdown("<h3 style='color: #4a5568; margin-top: 12px; margin-bottom: 12px; font-size: 16px;'>📞 전화번호 검색</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='search-label'>🔍 전화번호 또는 설계사명 입력</div>", unsafe_allow_html=True)
        contact_search = st.text_input("검색", placeholder="예: 010-1234-5678 또는 홍길동", label_visibility="collapsed", key="contact_search")
    
    with col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        contact_search_clicked = st.button("🔍 검색", use_container_width=True, key="contact_search_btn")
    
    if contact_search_clicked:
        if not contact_search:
            st.warning("⚠️ 전화번호 또는 설계사명을 입력해주세요.")
        else:
            search_value = contact_search.strip()
            
            # 전화번호 또는 설계사명으로 검색
            filtered_contacts = contact_df[
                (contact_df["휴대전화"].astype(str).str.contains(search_value, na=False)) |
                (contact_df["설계사명"].astype(str).str.contains(search_value, na=False))
            ]
            
            if len(filtered_contacts) == 0:
                st.error(f"❌ '{search_value}'에 해당하는 데이터를 찾을 수 없습니다.")
                st.session_state.contact_search_performed = False
            elif len(filtered_contacts) == 1:
                st.session_state.contact_search_performed = True
                st.session_state.contact_selected_row = filtered_contacts.iloc[0]
            else:
                st.markdown("<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>", unsafe_allow_html=True)
                
                for idx, (_, contact_row) in enumerate(filtered_contacts.iterrows()):
                    contact_name = str(contact_row.get('설계사명', 'N/A')).strip()
                    contact_phone = str(contact_row.get('휴대전화', 'N/A')).strip()
                    contact_branch = str(contact_row.get('지사', 'N/A')).strip()
                    
                    contact_display = f"{contact_name} - {contact_phone} ({contact_branch})"
                    
                    if st.button(contact_display, key=f"contact_{idx}", use_container_width=True):
                        st.session_state.contact_search_performed = True
                        st.session_state.contact_selected_row = contact_row
                        st.rerun()
    
    if st.session_state.contact_search_performed and st.session_state.contact_selected_row is not None:
        row = st.session_state.contact_selected_row
        
        name = str(row.get("설계사명", "N/A")).strip()
        code = str(row.get("설계사코드", "N/A")).strip()
        phone = str(row.get("휴대전화", "N/A")).strip()
        branch = str(row.get("지사", "N/A")).strip()
        office = str(row.get("지점", "N/A")).strip()
        manager = str(row.get("매니저", "N/A")).strip()
        join_date = str(row.get("위촉일자", "N/A")).strip()
        prev_month = format_display(row.get("전월실적", 0))
        prev_prev_month = format_display(row.get("전전월실적", 0))
        
        st.markdown("<h3 style='color: #4a5568;'>📋 설계사 정보</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='contact-box'>
        <strong>설계사명:</strong> {name}<br>
        <strong>설계사코드:</strong> {code}<br>
        <strong>📞 휴대전화:</strong> <span style='color: #48bb78; font-weight: 700; font-size: 16px;'>{phone}</span><br>
        <strong>소속지사:</strong> {branch}<br>
        <strong>소속지점:</strong> {office}<br>
        <strong>담당매니저:</strong> {manager}<br>
        <strong>위촉일자:</strong> {join_date}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #4a5568;'>📊 최근 실적</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='info-box'>
        <strong>1월 실적:</strong> {prev_prev_month}<br>
        <strong>2월 실적:</strong> {prev_month}
        </div>
        """, unsafe_allow_html=True)
        
        # vCard 생성 및 다운로드
        vcard_content = create_vcard(name, phone, branch, "설계사", office)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 연락처 저장 (vCard)",
                data=vcard_content,
                file_name=f"{name}_연락처.vcf",
                mime="text/vcard",
                use_container_width=True
            )
        
        with col2:
            if st.button("📋 정보 복사", use_container_width=True):
                copy_text = f"{name}\n{phone}\n{branch} | {office}\n담당: {manager}"
                st.code(copy_text, language=None)
                st.success("✅ 위 정보를 복사하세요!")
        
        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
        
        if st.button("🔄 초기화", use_container_width=True, key="reset_contact"):
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
            st.rerun()
    
    elif not st.session_state.contact_search_performed:
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);'>
        <p style='color: #4a5568; font-weight: 600; font-size: 15px; margin-bottom: 8px;'>📞 전화번호 또는 설계사명을 입력하고 검색하세요.</p>
        <p style='color: #718096; font-weight: 400; font-size: 13px; margin-top: 8px;'>예: 010-1234-5678 또는 홍길동</p>
        </div>
        """, unsafe_allow_html=True)
