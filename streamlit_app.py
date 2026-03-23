import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os

# ==================== 상수 정의 ====================
GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"
PASSWORD = "2603"

LEAFLET_TEMPLATE_IDS = {
    "메가": "1N0Aq60bQnPjg7o4GFv19lbqv3pUc57H8",
    "토스": "17b27Cq0sN52ifJ5NvCsnr87KbaUcsqsr",
    "신한금융": "1z3Ayg6mJsUeeHdebaOrWyOK4lz1-ROB_",
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
    "한화생명": "1F9z1vXXFXI-b1S3ZfVFtzKOpFaC8EfsL",
    "미래에셋증권": "1GJ9t6AKYvGr8u5U4HCqYMSyQR-YLdNGF",
    "NH투자증권": "1GvXvE9HrJmI-_Q6YyFnRONJAp_lp_3Mh",
    "KB증권": "1M2xZLwjKbmvHbZQJxHlpqxKQo_gWFAKW",
    "삼성증권": "1S7SjVJpGGr9nN2KqLxMzPqRs_tUvW5Yn"
}

st.set_page_config(page_title="메리츠 실적현황", layout="wide")

# ==================== 커스텀 CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #4a5568;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .search-box {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .info-box {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .cumulative-box {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .weekly-row {
        background-color: white;
        padding: 1rem 1.5rem;
        border-left: 4px solid #48bb78;
        margin-bottom: 0.5rem;
        border-radius: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .current-week {
        background: linear-gradient(135deg, #ffd93d 0%, #f6b93b 100%);
        border-left: 4px solid #f39c12;
        font-weight: 700;
    }
    
    .target-box {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .bridge-box {
        background: linear-gradient(135deg, #ed64a6 0%, #d53f8c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .mc-box {
        background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .mc-plus-box {
        background: linear-gradient(135deg, #805ad5 0%, #6b46c1 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74,85,104,0.3);
    }
    
    div[data-baseweb="select"] > div {
        background-color: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* 셀렉트박스 스크롤바 스타일링 */
    div[data-baseweb="popover"] {
        z-index: 9999;
    }
    
    /* 스크롤바 스타일링 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a5568;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 유틸리티 함수 ====================
def safe_float(value, default=0.0):
    """값을 안전하게 float로 변환"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        # 문자열인 경우 처리
        if isinstance(value, str):
            value = value.strip()
            # "10만원" 같은 텍스트는 변환
            if '만원' in value:
                number = value.replace('만원', '').strip()
                return float(number) * 10000
            # 숫자가 아닌 문자 제거
            value = ''.join(c for c in value if c.isdigit() or c == '.' or c == '-')
            if not value:
                return default
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return default

def format_display(value):
    """숫자를 한국 원화 형식으로 표시"""
    if value == 0:
        return "0 ₩"
    return f"{int(value):,} ₩"

def get_current_week():
    """현재 주차 반환 (KST 기준)"""
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(kst)
    
    # 3월 기준
    if now.month != 3:
        return 0
    
    day = now.day
    if day <= 7:
        return 1
    elif day <= 14:
        return 2
    elif day <= 21:
        return 3
    elif day <= 28:
        return 4
    else:
        return 5

def get_image_id_by_authentic_and_partner(is_authentic, partner_channel, agency_name):
    """어센틱 구분, 파트너 채널, 대리점명에 따라 리플렛 이미지 ID 반환"""
    if is_authentic == 1:
        partner_map = {
            "메가": "메가",
            "토스": "토스",
            "신한금융": "신한금융"
        }
        key = partner_map.get(partner_channel, "none")
    else:
        agency_map = {
            "한화생명": "한화생명",
            "미래에셋증권": "미래에셋증권",
            "NH투자증권": "NH투자증권",
            "KB증권": "KB증권",
            "삼성증권": "삼성증권"
        }
        key = agency_map.get(agency_name, "none")
    
    return LEAFLET_TEMPLATE_IDS.get(key, LEAFLET_TEMPLATE_IDS["none"])

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    """구글 시트에서 데이터 로드"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {str(e)}")
        return pd.DataFrame()

def load_leaflet_template_from_drive(file_id):
    """구글 드라이브에서 리플렛 이미지 로드"""
    try:
        url = f"https://drive.google.com/uc?id={file_id}"
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        gdown.download(url, temp_file.name, quiet=True)
        img = Image.open(temp_file.name)
        temp_file.close()
        os.unlink(temp_file.name)
        return img
    except Exception as e:
        st.error(f"리플렛 이미지 로드 실패: {str(e)}")
        return None

def load_logo():
    """로고 이미지 로드"""
    try:
        return Image.open("meritz.png")
    except:
        return None

def render_mc_box(title, target_col, shortage_col, row, box_class):
    """MC / MC+ 박스 렌더링"""
    target = safe_float(row.get(target_col, 0))
    shortage = safe_float(row.get(shortage_col, 0))
    
    if shortage == 0 or shortage < 0:
        status = "달성! ✅"
        color = "#48bb78"
    elif shortage == target:
        status = "미달성 ⚪"
        color = "#a0aec0"
    else:
        status = "진행중 🟡"
        color = "#ed8936"
    
    st.markdown(f"""
    <div class="{box_class}">
        <h3 style='margin:0 0 1rem 0;'>{title} {status}</h3>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
            <span style='font-size:0.9rem;'>목표:</span>
            <span style='font-size:1.1rem; font-weight:600;'>{format_display(target)}</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='font-size:0.9rem;'>부족:</span>
            <span style='font-size:1.1rem; font-weight:600; color:{color};'>{format_display(shortage)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== 세션 상태 초기화 ====================
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
    st.session_state.last_search_params = {'branch': None, 'agent': None}

# ==================== 로그인 ====================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>🔐 메리츠 실적현황 시스템</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password_input = st.text_input("비밀번호를 입력하세요", type="password", key="password")
        if st.button("로그인", key="login_btn"):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")
    st.stop()

# ==================== 메인 UI ====================
# 헤더
logo_col, title_col = st.columns([1, 5])
with logo_col:
    logo = load_logo()
    if logo:
        st.image(logo, width=120)

with title_col:
    st.markdown("<h1 class='main-title'>메리츠 실적현황 대시보드</h1>", unsafe_allow_html=True)

# 데이터 로드
df = load_data_from_google_sheets()
if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# 지점 목록 생성
try:
    ga4_branches = sorted(df['지점명'].dropna().unique().tolist())
    default_idx = ga4_branches.index("GA4-2지점") if "GA4-2지점" in ga4_branches else 0
except:
    ga4_branches = [f"GA4-{i}지점" for i in range(1, 14)]
    default_idx = 1

# 검색 패널
st.markdown("<div class='search-box'>", unsafe_allow_html=True)
st.markdown("### 🔍 실적 조회")

col1, col2 = st.columns([1, 2])
with col1:
    selected_branch = st.selectbox(
        "📍 지점 선택",
        options=ga4_branches,
        index=default_idx,
        key="branch_select"
    )

with col2:
    agent_name = st.text_input("👔 설계사명", key="agent_input")

# 검색 파라미터 변경 감지
current_params = {
    'branch': selected_branch,
    'agent': agent_name
}

if current_params != st.session_state.last_search_params:
    st.session_state.search_performed = False
    st.session_state.selected_row = None
    st.session_state.show_duplicates = False
    st.session_state.filtered_data = None
    st.session_state.last_search_params = current_params

if st.button("🔍 검색", key="search_btn"):
    if not agent_name:
        st.warning("⚠️ 설계사명을 입력해주세요.")
    else:
        filtered = df[
            (df['지점명'] == selected_branch) &
            (df['설계사명'].str.contains(agent_name, na=False))
        ]
        
        if filtered.empty:
            st.error(f"❌ '{selected_branch}' 지점에서 '{agent_name}' 설계사를 찾을 수 없습니다.")
        elif len(filtered) == 1:
            st.session_state.search_performed = True
            st.session_state.selected_row = filtered.iloc[0]
            st.session_state.show_duplicates = False
        else:
            st.session_state.show_duplicates = True
            st.session_state.filtered_data = filtered
            st.session_state.search_performed = False

st.markdown("</div>", unsafe_allow_html=True)

# 동명이인 처리
if st.session_state.show_duplicates and st.session_state.filtered_data is not None:
    st.markdown("### 👥 동명이인이 있습니다. 선택해주세요:")
    for idx, (_, row) in enumerate(st.session_state.filtered_data.iterrows()):
        branch_name = row.get('지사명', row.get('지점명', ''))
        agent_code = row.get('현재대리점설계사조직코드', '')
        label = f"{branch_name} - {row['설계사명']} ({agent_code})"
        
        if st.button(label, key=f"agent_{idx}"):
            st.session_state.search_performed = True
            st.session_state.selected_row = row
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
            st.rerun()

# 검색 결과 표시
if st.session_state.search_performed and st.session_state.selected_row is not None:
    row = st.session_state.selected_row
    
    # 현재 주차
    current_week = get_current_week()
    
    # 기본 정보
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # 기본 정보 박스
        branch_name = row.get('지사명', row.get('지점명', ''))
        agent_code = row.get('현재대리점설계사조직코드', '')
        st.markdown(f"""
        <div class='info-box'>
            <h3 style='margin:0;'>📋 기본 정보</h3>
            <div style='margin-top:1rem; font-size:1.1rem;'>
                <div style='margin-bottom:0.5rem;'><strong>지사명:</strong> {branch_name}</div>
                <div><strong>설계사명:</strong> {row['설계사명']} ({agent_code})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 누적 실적
        cumulative = safe_float(row.get('누계실적', 0))
        st.markdown(f"""
        <div class='cumulative-box'>
            <h2 style='margin:0 0 0.5rem 0;'>3월 누적 실적</h2>
            <h1 style='margin:0; font-size:2.5rem;'>{format_display(cumulative)}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # 주차별 실적
        st.markdown("### 📊 주차별 실적")
        for week in range(1, 6):
            week_col = f"{week}주차"
            week_value = safe_float(row.get(week_col, 0))
            is_current = (week == current_week)
            row_class = "weekly-row current-week" if is_current else "weekly-row"
            star = " ⭐" if is_current else ""
            
            st.markdown(f"""
            <div class='{row_class}'>
                <span style='font-weight:600;'>{week}주차{star}</span>
                <span style='font-size:1.1rem; font-weight:600;'>{format_display(week_value)}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # 현재 주차 목표 - S열(주차목표)와 U열(주차부족최종) 직접 사용
        is_authentic = safe_float(row.get('어센틱구분', 0))
        
        # S열: 주차목표 (텍스트 그대로 표시)
        if is_authentic == 1:
            weekly_target_text = str(row.get('어센틱주차목표', '0'))
        else:
            weekly_target_text = str(row.get('주차목표', '0'))
        
        # 텍스트를 숫자로 변환 (표시용)
        weekly_target_value = safe_float(weekly_target_text)
        
        # U열: 주차부족최종 (숫자)
        if is_authentic == 1:
            weekly_shortage = safe_float(row.get('어센틱주차부족', 0))
        else:
            weekly_shortage = safe_float(row.get('주차부족최종', 0))
        
        st.markdown(f"""
        <div class='target-box'>
            <h3 style='margin:0 0 1rem 0;'>🎯 현재 주차 목표</h3>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
                <span>목표:</span>
                <span style='font-size:1.2rem; font-weight:700;'>{format_display(weekly_target_value)}</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span>부족:</span>
                <span style='font-size:1.2rem; font-weight:700;'>{format_display(weekly_shortage)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 브릿지 실적 (어센틱이 아닌 경우만)
        if is_authentic != 1:
            bridge_target_text = str(row.get('브릿지 도전구간', '0'))
            bridge_target = safe_float(bridge_target_text)
            bridge_shortage = safe_float(row.get('브릿지부족최종', 0))
            
            st.markdown(f"""
            <div class='bridge-box'>
                <h3 style='margin:0 0 1rem 0;'>🌉 브릿지 실적</h3>
                <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
                    <span>목표:</span>
                    <span style='font-size:1.1rem; font-weight:600;'>{format_display(bridge_target)}</span>
                </div>
                <div style='display:flex; justify-content:space-between;'>
                    <span>부족:</span>
                    <span style='font-size:1.1rem; font-weight:600;'>{format_display(bridge_shortage)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # MC 실적
        render_mc_box("MC 챌린지", "MC도전구간", "MC부족최종", row, "mc-box")
        
        # MC PLUS+ 실적
        render_mc_box("MC PLUS+ 챌린지", "MC+구간", "MC+부족최종", row, "mc-plus-box")
    
    with right_col:
        # 리플렛 이미지
        st.markdown("### 📄 리플렛")
        partner_channel = row.get('파트너채널', '')
        agency_name = row.get('대리점', '')
        
        image_id = get_image_id_by_authentic_and_partner(is_authentic, partner_channel, agency_name)
        leaflet_img = load_leaflet_template_from_drive(image_id)
        
        if leaflet_img:
            st.image(leaflet_img, use_container_width=True)
            
            # 다운로드 버튼
            buf = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            leaflet_img.save(buf.name, 'JPEG')
            with open(buf.name, 'rb') as f:
                st.download_button(
                    label="📥 리플렛 다운로드",
                    data=f,
                    file_name=f"{agency_name}_leaflet.jpg",
                    mime="image/jpeg"
                )
            os.unlink(buf.name)
    
    # 리셋 버튼
    if st.button("🔄 초기화", key="reset_btn"):
        st.session_state.search_performed = False
        st.session_state.selected_row = None
        st.session_state.show_duplicates = False
        st.session_state.filtered_data = None
        st.rerun()

else:
    if not st.session_state.show_duplicates:
        st.info("💡 설계사명을 입력하고 검색 버튼을 눌러주세요.")
