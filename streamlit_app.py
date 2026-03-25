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
PASSWORD = "2233"

LEAFLET_TEMPLATE_IDS = {
    "메가": "1N0Aq60bQnPjg7o4GFv19lbqv3pUc57H8",
    "토스": "1Xn_hB6Xl6fojhcgyF2zVlpYtyQst5ann",
    "우리은행": "15Wn5m4DQUEq_yRO9ov85bnQSjx59BXHv",
    "기업은행": "12PU0IpTJmzmRWvfnB-qs7sGNr0t6LZ65",
    "하나은행": "1__qSDbxAjx_PD1oKh2xPxpqaRkWg6o6-",
    "NH농협": "1-vvvl3SebKK3vTxD_vLH7eZ7Qm8QcCYa",
    "GA 파트너_동구": "1CgxBxzxc9YU2hcIBkX7TfqQOqk4XWp89",
    "GA 파트너_부산": "1qIHsxZxSHFYTyB0qBQN6XM0lIXz2fkeq",
    "GA 파트너_서면": "1lzYdhzEW0y7vIKB85xN3T6TZ3xDZNiTs",
    "GA 파트너_인천": "1SQHoedp2_eESGv0FEzGrzDRq4DpBcqxQ",
    "GA 파트너_종로": "1RgJ3qCr-rxVpANXD4_QpQeQeRjeBOgWM",
    "GA 파트너_평촌": "1zMXG3Z61J_4QzTxNxOtALV6MVzqe-e6V",
    "토스파트너": "1nrgwqXBEn1vSr33xbQyPKy3rtzU1ZcY1",
    "토스인슈어런스": "1vu7-hRlOi8FS9_KqTcjyD1JQJVjjWxb4",
    "GA대리점_하": "1EKg6-nHgKDJ0N6aIXXxb8--vURHEI52U",
    "GA대리점_중": "1IcWP0khRGnjAnyKKlOUlmCZjJr71u5kL",
    "GA대리점_상": "1ifDCfJ3fWoSGM_Gf2zHRPfM_7cWxWv_L",
    "GA 오토_하": "16Pg4SiTsgz2OJ8BNjqlc5AQGi4dSGYKp",
    "GA 오토_중": "1jOG8gfbHMXdYlIz48SnV_jJKvkCv-Soc",
    "GA 오토_상": "1dMuU0CoCWNGvvblmUWrN4G68J8RZ-iFi"
}

# ==================== 페이지 설정 ====================
st.set_page_config(
    page_title="메리츠 실적현황",
    layout="wide",
    page_icon="📊"
)

# ==================== 스타일 ====================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 스크롤바 스타일링 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.5);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.1);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #667eea !important;
    }
    
    /* 입력 필드 */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid rgba(255,255,255,0.3);
        background-color: rgba(255,255,255,0.95);
        color: #2d3748;
        font-weight: 500;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: white;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.2);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        background: white;
        color: #667eea;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        background: #f7fafc;
    }
    
    /* 정보 박스 */
    .info-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .info-box strong {
        color: #667eea;
        font-weight: 600;
    }
    
    /* MC 박스 */
    .mc-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    .mc-box strong {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .mc-value {
        font-size: 24px;
        font-weight: 700;
        margin: 8px 0;
    }
    
    /* MC+ 박스 */
    .mc-plus-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(240,147,251,0.3);
    }
    
    /* 브릿지 박스 */
    .bridge-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(79,172,254,0.3);
    }
    
    /* 연락처 박스 */
    .contact-box {
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .contact-box strong {
        color: #667eea;
        font-weight: 600;
        display: inline-block;
        min-width: 100px;
    }
    
    /* 로그인 박스 */
    .login-container {
        background: white;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        max-width: 400px;
        margin: 100px auto;
    }
    
    .login-title {
        color: #667eea;
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 다운로드 버튼 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    /* 테이블 스타일 */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 헬퍼 함수 ====================
def safe_float(value):
    """안전하게 float으로 변환"""
    if pd.isna(value) or value == '' or value is None:
        return 0.0
    try:
        if isinstance(value, str):
            value = value.replace(',', '').replace('₩', '').replace('원', '').strip()
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def format_display(value):
    """숫자를 통화 형식으로 표시"""
    num = safe_float(value)
    if num == 0:
        return "0 원"
    return f"{int(num):,} 원"

def get_current_week():
    """현재 주차 계산"""
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(kst)
    first_day = datetime.datetime(now.year, now.month, 1, tzinfo=kst)
    days_offset = (now - first_day).days
    current_week = (days_offset // 7) + 1
    return min(current_week, 5)

def get_image_id_by_authentic_and_partner(is_authentic, partner_type):
    """어센틱 구분과 파트너 유형으로 이미지 ID 반환"""
    if is_authentic:
        key_prefix = "토스파트너" if partner_type == "토스" else "GA 파트너"
    else:
        key_prefix = "GA대리점" if partner_type == "대리점" else "GA 오토"
    
    for key in LEAFLET_TEMPLATE_IDS:
        if key.startswith(key_prefix):
            return LEAFLET_TEMPLATE_IDS[key]
    return None

def load_leaflet_template_from_drive(image_id):
    """구글 드라이브에서 리프렛 템플릿 로드"""
    if not image_id:
        return None
    try:
        url = f"https://drive.google.com/uc?id={image_id}"
        output_path = os.path.join(tempfile.gettempdir(), f"leaflet_{image_id}.png")
        gdown.download(url, output_path, quiet=True)
        img = Image.open(output_path)
        return img
    except Exception as e:
        st.error(f"리프렛 템플릿을 불러오는데 실패했습니다: {str(e)}")
        return None

def render_mc_box(challenge_value, shortage_value, is_authentic, is_mc_plus=False):
    """MC 또는 MC+ 박스 렌더링"""
    if is_mc_plus:
        box_class = "mc-plus-box"
        title = "💎 MC PLUS+"
    else:
        box_class = "mc-box"
        title = "💰 MC 성과"
    
    challenge_display = format_display(challenge_value)
    shortage_display = format_display(shortage_value)
    
    st.markdown(f"""
    <div class='{box_class}'>
        <div style='font-size: 18px; font-weight: 600; margin-bottom: 12px;'>{title}</div>
        <div style='margin-bottom: 10px;'>
            <strong>목표 →</strong>
            <div class='mc-value'>{challenge_display}</div>
        </div>
        <div>
            <strong>부족금액 →</strong>
            <div class='mc-value'>{shortage_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    """구글 시트에서 데이터 로드"""
    try:
        # 시트1 (실적 데이터)
        sheet1_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
        df1 = pd.read_csv(sheet1_url)
        
        # 시트2 (연락처 데이터) - 전화번호가 있는 시트 (gid=363789500)
        sheet2_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=363789500"
        df2 = pd.read_csv(sheet2_url)
        
        return df1, df2
    except Exception as e:
        st.error(f"데이터를 불러오는데 실패했습니다: {str(e)}")
        return None, None

def normalize_phone_number(phone):
    """전화번호 정규화 (하이픈 제거, 공백 제거)"""
    if pd.isna(phone):
        return ""
    phone_str = str(phone).replace("-", "").replace(" ", "").strip()
    return phone_str

def create_vcard(name, phone, branch):
    """vCard 형식 생성"""
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{branch}-{name}
TEL;TYPE=CELL:{phone}
END:VCARD"""
    return vcard

# ==================== 세션 상태 초기화 ====================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'search_name' not in st.session_state:
    st.session_state.search_name = ""
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'show_duplicates' not in st.session_state:
    st.session_state.show_duplicates = False
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'contact_search_name' not in st.session_state:
    st.session_state.contact_search_name = ""
if 'contact_search_performed' not in st.session_state:
    st.session_state.contact_search_performed = False
if 'contact_selected_row' not in st.session_state:
    st.session_state.contact_selected_row = None
if 'contact_show_duplicates' not in st.session_state:
    st.session_state.contact_show_duplicates = False
if 'contact_filtered_data' not in st.session_state:
    st.session_state.contact_filtered_data = None

# ==================== 로그인 화면 ====================
if not st.session_state.authenticated:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>🔐 로그인</div>", unsafe_allow_html=True)
    
    password_input = st.text_input("비밀번호를 입력하세요", type="password", key="password_input")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("로그인", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==================== 메인 화면 ====================
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>📊 메리츠 실적 현황</h1>", unsafe_allow_html=True)

# 데이터 로드
df1, df2 = load_data()

if df1 is None or df2 is None:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

# 전화번호 정규화
df2['정규화번호'] = df2.iloc[:, 2].apply(normalize_phone_number)

# ==================== 탭 생성 ====================
tab1, tab2 = st.tabs(["📈 실적조회", "📞 전화번호 조회"])

# ==================== 실적조회 탭 ====================
with tab1:
    st.markdown("<h2 style='color: white;'>실적 조회</h2>", unsafe_allow_html=True)
    
    search_col, button_col = st.columns([3, 1])
    with search_col:
        search_input = st.text_input("설계사명을 입력하세요", key="perf_search_input", label_visibility="collapsed", placeholder="설계사명 입력")
    with button_col:
        search_button = st.button("🔍 조회", key="perf_search_button", use_container_width=True)
    
    if search_button and search_input:
        filtered = df1[df1['설계사명'].str.contains(search_input, na=False, case=False)]
        
        if len(filtered) == 0:
            st.warning("❌ 검색 결과가 없습니다.")
            st.session_state.search_performed = False
            st.session_state.show_duplicates = False
            st.session_state.selected_row = None
        elif len(filtered) == 1:
            st.session_state.selected_row = filtered.iloc[0]
            st.session_state.search_performed = True
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
        else:
            st.session_state.show_duplicates = True
            st.session_state.filtered_data = filtered
            st.session_state.search_performed = False
            st.session_state.selected_row = None
    
    # 동명이인 선택
    if st.session_state.show_duplicates and st.session_state.filtered_data is not None:
        st.markdown("<p style='color:white;font-weight:600;margin-top:12px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
        
        for idx, (_, row) in enumerate(st.session_state.filtered_data.iterrows()):
            office_branch = str(row.get('지점명', 'N/A')).strip()
            agency_branch = str(row.get('지사명', 'N/A')).strip()
            display_text = f"{office_branch} | {agency_branch}"
            
            if st.button(display_text, key=f"dup_btn_{idx}", use_container_width=True):
                # 세션 상태 업데이트
                st.session_state.selected_row = row.copy()
                st.session_state.search_performed = True
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None
                st.rerun()
    
    # 검색 결과 표시
    if st.session_state.search_performed and st.session_state.selected_row is not None:
        row = st.session_state.selected_row
        
        # 어센틱 구분 확인 - AA열 (인덱스 26)
        is_authentic = False
        try:
            authentic_value = safe_float(df1.iloc[row.name, 26])  # AA열 = 인덱스 26
            is_authentic = (authentic_value == 1)
        except:
            is_authentic = False
        
        # 기본 정보
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown(f"""
        <strong>설계사명:</strong> {row.get('설계사명', 'N/A')}<br>
        <strong>설계사코드:</strong> {row.get('설계사코드', 'N/A')}<br>
        <strong>지점명:</strong> {row.get('지점명', 'N/A')}<br>
        <strong>지사명:</strong> {row.get('지사명', 'N/A')}
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 실적 정보
        st.markdown("<h3 style='color: white; margin-top: 20px;'>📊 실적 정보</h3>", unsafe_allow_html=True)
        
        # 이번달 실적 (시트1 M열)
        current_month_performance = safe_float(row.get('누계실적', 0))
        
        # 전월 실적 (AA열이 아니라 연락처 시트의 AA열에서 가져와야 함)
        # 연락처 시트에서 해당 설계사 찾기
        designer_code = str(row.get('설계사코드', ''))
        contact_row = df2[df2.iloc[:, 1].astype(str) == designer_code]
        
        if len(contact_row) > 0:
            prev_month = safe_float(contact_row.iloc[0, 26])  # AA열
            prev_prev_month = safe_float(contact_row.iloc[0, 27])  # AB열
        else:
            prev_month = 0
            prev_prev_month = 0
        
        st.markdown(f"""
        <div class='info-box'>
        <strong>이번달 누계실적:</strong> {format_display(current_month_performance)}<br>
        <strong>전월 실적:</strong> {format_display(prev_month)}<br>
        <strong>전전월 실적:</strong> {format_display(prev_prev_month)}
        </div>
        """, unsafe_allow_html=True)
        
        # 성과 표시 - 어센틱 구분에 따라 다르게 표시
        if is_authentic:
            # 어센틱 설계사 = MC 성과만 표시
            st.markdown("<h3 style='color: white;'>💰 MC 성과</h3>", unsafe_allow_html=True)
            mc_challenge = row.get("MC도전구간", 0)
            mc_shortage = row.get("MC부족최종", 0)
            render_mc_box(mc_challenge, mc_shortage, is_authentic=True, is_mc_plus=False)
        else:
            # 브릿지 설계사 = 브릿지 성과만 표시
            st.markdown("<h3 style='color: white;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
            bridge_target = row.get("브릿지 도전구간", 0)
            bridge_shortage = row.get("브릿지부족최종", 0)
            st.markdown(f"""
            <div class='bridge-box'>
                <div style='font-size: 18px; font-weight: 600; margin-bottom: 12px;'>🌉 브릿지 성과</div>
                <div style='margin-bottom: 10px;'>
                    <strong>목표 →</strong>
                    <div class='mc-value'>{format_display(bridge_target)}</div>
                </div>
                <div>
                    <strong>부족금액 →</strong>
                    <div class='mc-value'>{format_display(bridge_shortage)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # MC+ 성과 (모든 설계사에게 표시)
        st.markdown("<h3 style='color: white;'>💎 MC PLUS+ 성과</h3>", unsafe_allow_html=True)
        mc_plus_challenge = row.get("MC+구간", 0)
        mc_plus_shortage = row.get("MC+부족최종", 0)
        render_mc_box(mc_plus_challenge, mc_plus_shortage, is_authentic=is_authentic, is_mc_plus=True)
        
        # 리프렛 이미지
        st.markdown("<h3 style='color: white; margin-top: 20px;'>📄 주간 리프렛</h3>", unsafe_allow_html=True)
        
        partner_type = row.get('파트너 유형', '')
        image_id = get_image_id_by_authentic_and_partner(is_authentic, partner_type)
        
        if image_id:
            leaflet_image = load_leaflet_template_from_drive(image_id)
            if leaflet_image:
                st.image(leaflet_image, use_container_width=True)
        else:
            st.info("해당하는 리프렛 템플릿이 없습니다.")
        
        # 초기화 버튼
        if st.button("🔄 새로운 조회", key="reset_button", use_container_width=True):
            st.session_state.search_performed = False
            st.session_state.selected_row = None
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
            st.rerun()

# ==================== 전화번호 조회 탭 ====================
with tab2:
    st.markdown("<h2 style='color: white;'>전화번호 조회</h2>", unsafe_allow_html=True)
    
    contact_search_col, contact_button_col = st.columns([3, 1])
    with contact_search_col:
        contact_search_input = st.text_input(
            "설계사명 또는 전화번호를 입력하세요",
            key="contact_search_input",
            label_visibility="collapsed",
            placeholder="설계사명 또는 전화번호 입력 (예: 홍길동, 1112222, 010-1111-2222)"
        )
    with contact_button_col:
        contact_search_button = st.button("🔍 조회", key="contact_search_button", use_container_width=True)
    
    if contact_search_button and contact_search_input:
        search_term = contact_search_input.strip()
        
        # 전화번호 검색인지 이름 검색인지 판단
        normalized_search = normalize_phone_number(search_term)
        
        if normalized_search.isdigit():
            # 전화번호 검색
            # 010이 없으면 추가
            if len(normalized_search) <= 8:
                normalized_search = "010" + normalized_search
            
            filtered_contacts = df2[df2['정규화번호'].str.contains(normalized_search, na=False)]
        else:
            # 이름 검색
            filtered_contacts = df2[df2.iloc[:, 0].str.contains(search_term, na=False, case=False)]
        
        if len(filtered_contacts) == 0:
            st.warning("❌ 검색 결과가 없습니다.")
            st.session_state.contact_search_performed = False
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_selected_row = None
        elif len(filtered_contacts) == 1:
            st.session_state.contact_selected_row = filtered_contacts.iloc[0]
            st.session_state.contact_search_performed = True
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
        else:
            st.session_state.contact_show_duplicates = True
            st.session_state.contact_filtered_data = filtered_contacts
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
    
    # 동명이인 선택
    if st.session_state.contact_show_duplicates and st.session_state.contact_filtered_data is not None:
        st.markdown("<p style='color:white;font-weight:600;margin-top:12px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
        
        for idx, (_, contact_row) in enumerate(st.session_state.contact_filtered_data.iterrows()):
            branch = str(contact_row.iloc[5]).strip()  # 지점
            agency = str(contact_row.iloc[6]).strip()  # 지사
            display_text = f"{branch} | {agency}"
            
            if st.button(display_text, key=f"contact_dup_btn_{idx}", use_container_width=True):
                # 세션 상태 업데이트
                st.session_state.contact_selected_row = contact_row.copy()
                st.session_state.contact_search_performed = True
                st.session_state.contact_show_duplicates = False
                st.session_state.contact_filtered_data = None
                st.rerun()
    
    # 검색 결과 표시
    if st.session_state.contact_search_performed and st.session_state.contact_selected_row is not None:
        contact_row = st.session_state.contact_selected_row
        
        designer_name = str(contact_row.iloc[0])
        designer_code = str(contact_row.iloc[1])
        phone = str(contact_row.iloc[2])
        branch = str(contact_row.iloc[5])
        agency = str(contact_row.iloc[6])
        
        # 연락처 정보 표시
        st.markdown(f"""
        <div class='contact-box'>
        <strong>설계사명:</strong> {designer_name}<br>
        <strong>설계사코드:</strong> {designer_code}<br>
        <strong>전화번호:</strong> {phone}<br>
        <strong>지점:</strong> {branch}<br>
        <strong>지사:</strong> {agency}
        </div>
        """, unsafe_allow_html=True)
        
        # 실적 정보 가져오기 (시트1에서)
        matched_perf = df1[df1['설계사코드'].astype(str) == designer_code]
        
        if len(matched_perf) > 0:
            perf_row = matched_perf.iloc[0]
            
            # 이번달 누계실적
            current_month_perf = safe_float(perf_row.get('누계실적', 0))
            
            # 전월, 전전월 실적
            prev_month = safe_float(contact_row.iloc[26])  # AA열
            prev_prev_month = safe_float(contact_row.iloc[27])  # AB열
            
            st.markdown("<h3 style='color: white;'>📊 실적 정보</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
            <strong>이번달 누계실적:</strong> {format_display(current_month_perf)}<br>
            <strong>전월 실적:</strong> {format_display(prev_month)}<br>
            <strong>전전월 실적:</strong> {format_display(prev_prev_month)}
            </div>
            """, unsafe_allow_html=True)
        
        # vCard 다운로드 버튼
        vcard_data = create_vcard(designer_name, phone, agency)
        st.download_button(
            label="📇 vCard 다운로드",
            data=vcard_data,
            file_name=f"{agency}_{designer_name}_연락처.vcf",
            mime="text/vcard",
            use_container_width=True
        )
        
        # 초기화 버튼
        if st.button("🔄 새로운 조회", key="contact_reset_button", use_container_width=True):
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
            st.rerun()
