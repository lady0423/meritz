import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import os
import streamlit.components.v1 as components
import re

GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

PASSWORD = "2233"

# ✅ 반드시 set_page_config가 가장 먼저
st.set_page_config(page_title="메리츠 실적현황", layout="wide")

# ✅ unsafe_allow_html=True 필수
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { font-family: 'Noto Sans KR', sans-serif !important; }
html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stDecoration"] {
    background: #f8f9fa !important; color: #2c3e50;
}
[data-testid="stHeader"] { background: rgba(255,255,255,0.95) !important; }
h1, h2, h3 {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 700; letter-spacing: -0.5px; color: #2c3e50;
}
input::-webkit-autofill,
input::-webkit-autofill:hover,
input::-webkit-autofill:focus,
input::-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #ffffff inset !important;
    box-shadow: 0 0 0 30px #ffffff inset !important;
}
input::-webkit-autofill { -webkit-text-fill-color: #2c3e50 !important; }
.stButton > button {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    border: none; border-radius: 8px; padding: 10px 20px;
    color: white; transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(74,85,104,0.3);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    box-shadow: 0 4px 15px rgba(74,85,104,0.4);
    transform: translateY(-2px);
}
div[data-testid="stVerticalBlock"] .agent-card-btn > button {
    background: white !important;
    color: #2c3e50 !important;
    border: 1px solid #e2e8f0 !important;
    border-left: 4px solid #4a5568 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    text-align: left !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stVerticalBlock"] .agent-card-btn > button:hover {
    background: #f7fafc !important;
    border-left-color: #f59e0b !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    transform: translateX(2px) !important;
}
div[data-testid="stVerticalBlock"] .agent-card-btn-active > button {
    background: #fffbeb !important;
    border-left: 4px solid #f59e0b !important;
    border-color: #f6d860 !important;
    box-shadow: 0 2px 8px rgba(245,158,11,0.2) !important;
}
.info-box {
    background: white; border-left: 4px solid #4a5568;
    padding: 12px; border-radius: 8px; margin: 8px 0;
    font-size: 14px; line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-weight: 500; color: #2c3e50;
}
.contact-box {
    background: white; border-left: 4px solid #48bb78;
    padding: 12px; border-radius: 8px; margin: 8px 0;
    font-size: 14px; line-height: 1.6;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-weight: 500; color: #2c3e50;
}
.cumulative-box {
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    padding: 16px; border-radius: 8px; margin: 8px 0;
    font-size: 22px; font-weight: 700; color: white;
    text-align: center;
    box-shadow: 0 2px 12px rgba(74,85,104,0.25);
    letter-spacing: 0.5px;
}
.weekly-row {
    background: white; border-left: 4px solid #48bb78;
    padding: 10px 12px; border-radius: 8px; margin: 6px 0;
    font-size: 14px; display: flex;
    justify-content: space-between; align-items: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-weight: 600; color: #2c3e50;
}
.weekly-row.current {
    background: linear-gradient(135deg, #ffd93d 0%, #ffb93d 100%);
    border-left: 4px solid #f59e0b;
    box-shadow: 0 2px 10px rgba(245,158,11,0.3);
    color: #92400e;
}
.search-label {
    font-weight: 600; font-size: 13px;
    color: #4a5568; margin-bottom: 6px; display: block;
}
input, select {
    background-color: #ffffff !important;
    color: #2c3e50 !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important; padding: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important; transition: all 0.3s ease;
}
input:focus, select:focus {
    border-color: #4a5568 !important;
    box-shadow: 0 0 0 3px rgba(74,85,104,0.1) !important;
    outline: none !important;
}
input::placeholder { color: #a0aec0 !important; }
.stTextInput > label, .stSelectbox > label {
    font-weight: 600; color: #4a5568;
    font-family: 'Noto Sans KR', sans-serif; font-size: 14px;
}
[data-baseweb="select"] { width: 100%; }
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important; min-height: 40px;
}
[data-baseweb="select"] > div > div {
    color: #2c3e50 !important; font-weight: 500 !important;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600; padding: 10px 20px;
    border-radius: 8px 8px 0 0;
    background-color: #e2e8f0; color: #4a5568;
}
.stTabs [aria-selected="true"] { background-color: #4a5568; color: white; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
.login-box {
    max-width: 320px; margin: 30px auto; padding: 20px;
    background: white; border-radius: 12px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
}
.login-box h2 { font-size: 18px; margin-bottom: 15px; }
.login-box input { font-size: 14px !important; padding: 8px !important; }
h3 { font-size: 16px !important; margin-top: 12px !important; margin-bottom: 8px !important; }
[data-testid="stExpander"] {
    border: none !important; box-shadow: none !important; background: transparent !important;
}
[data-testid="stExpander"] summary { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 유틸 함수
# ============================================================
def safe_float(value):
    if pd.isna(value): return 0.0
    if value == "" or value is None: return 0.0
    try:
        v = str(value).strip()
        if v == "": return 0.0
        if "만원" in v:
            return float(v.replace("만원","").strip()) * 10000
        return float(v.replace(",",""))
    except: return 0.0

def format_display(value):
    v = str(value).strip()
    if v == "" or v == "nan": return "₩ 0"
    try:
        if "만원" in v:
            num = float(v.replace("만원","").strip()) * 10000
            return f"₩ {num:,.0f}"
        num = float(v.replace(",",""))
        return f"₩ {num:,.0f}"
    except: return v

def normalize_phone_number(phone):
    if pd.isna(phone): return ""
    return str(phone).replace("-","").replace(" ","").strip()

def extract_ga4_number(branch_str):
    match = re.search(r'GA4-(\d+)', str(branch_str))
    return int(match.group(1)) if match else 9999

def get_current_week():
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst).date()
    day = today.day
    if today.month == 3:
        if day <= 1: return 0
        elif day <= 8: return 1
        elif day <= 15: return 2
        elif day <= 22: return 3
        elif day <= 29: return 4
        else: return 5
    return 4

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
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=363789500"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"전화번호 데이터 로드 실패: {e}")
        return None

def get_current_month_performance(performance_df, agent_code):
    try:
        if performance_df is None: return 0.0
        filtered = performance_df[
            performance_df["현재대리점설계사조직코드"].astype(str).str.strip() == str(agent_code).strip()
        ]
        if len(filtered) > 0:
            return safe_float(filtered.iloc[0].get("누계실적", 0))
        return 0.0
    except: return 0.0

def create_vcard(name, phone, company):
    phone_clean = phone.replace("-","").replace(" ","")
    return f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL;TYPE=CELL:{phone_clean}\nORG:{company}\nEND:VCARD"

def load_logo():
    if os.path.exists("meritz.png"):
        return Image.open("meritz.png")
    return None

def copy_to_clipboard_button(text, button_label="📋 메시지 복사하기", key="clipboard_btn", height=80):
    escaped_text = text.replace("\\","\\\\").replace("`","\\`").replace("$","\\$")
    components.html(f"""
        <button onclick="copyText()" style="
            font-family:'Noto Sans KR',sans-serif; font-weight:600;
            background:linear-gradient(135deg,#4a5568 0%,#2d3748 100%);
            border:none; border-radius:8px; padding:8px 16px;
            color:white; cursor:pointer; width:100%; font-size:13px;
            box-shadow:0 2px 8px rgba(74,85,104,0.3);">
            {button_label}
        </button>
        <div id="copyMsg_{key}" style="
            display:none; margin-top:6px; padding:6px 10px;
            background:#c6f6d5; border-left:4px solid #48bb78;
            border-radius:6px; color:#276749;
            font-family:'Noto Sans KR',sans-serif;
            font-size:12px; font-weight:600;">
            ✅ 복사 완료! 카카오톡에 붙여넣기 하세요.
        </div>
        <script>
        function copyText() {{
            const text = `{escaped_text}`;
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(showSuccess, () => fallbackCopy(text));
            }} else {{ fallbackCopy(text); }}
        }}
        function fallbackCopy(text) {{
            const el = document.createElement('textarea');
            el.value = text; el.style.position='fixed'; el.style.left='-9999px';
            document.body.appendChild(el); el.focus(); el.select();
            try {{ document.execCommand('copy'); showSuccess(); }}
            catch(e) {{ alert('복사 실패: 메시지를 직접 드래그하여 복사해주세요.'); }}
            document.body.removeChild(el);
        }}
        function showSuccess() {{
            const msg = document.getElementById('copyMsg_{key}');
            msg.style.display='block';
            setTimeout(() => msg.style.display='none', 3000);
        }}
        </script>""", height=height)

def build_kakao_message(row, df, current_week, greeting=""):
    agency_branch = str(row.get("지사명","N/A")).strip()
    agent_name_display = str(row["설계사명"]).strip()
    cumulative = row["누계실적"]
    week_columns = ["1주차","2주차","3주차","4주차","5주차"]
    week_text = ""
    for idx, week_col in enumerate(week_columns, 1):
        if idx > current_week: break
        current_mark = " ⭐" if idx == current_week else ""
        week_text += f" • {week_col}: {format_display(row[week_col])}{current_mark}\n"
    greeting_line = f"{greeting}\n\n" if greeting.strip() else ""
    return f"""{greeting_line}📊메리츠 3월 실적 현황
{agency_branch} {agent_name_display}팀장님!

📈 3월 누계 실적
 {format_display(cumulative)}

📅 주차별 실적
{week_text}
💡 시상관련 궁금하신게 있다면 문의주세요~
이번주도 화이팅입니다!"""

def apply_manager_filter(agents_df, filter_mode, current_week):
    if filter_mode == 0:
        return agents_df
    if filter_mode == 1:
        week_cols = ["1주차","2주차","3주차","4주차","5주차"]
        if 1 <= current_week <= 5:
            col = week_cols[current_week - 1]
            if col in agents_df.columns:
                return agents_df[agents_df[col].apply(safe_float) > 0]
        return agents_df
    return agents_df


# ============================================================
# 세션 상태 초기화
# ============================================================
defaults = {
    'authenticated': False,
    'search_performed': False, 'selected_row': None,
    'show_duplicates': False, 'filtered_data': None,
    'contact_search_performed': False, 'contact_selected_row': None,
    'contact_show_duplicates': False, 'contact_filtered_data': None,
    'manager_search_performed': False, 'manager_agent_list': None,
    'manager_name_display': "", 'manager_expanded_idx': None,
    'manager_filter_mode': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ============================================================
# 로그인
# ============================================================
if not st.session_state.authenticated:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        logo = load_logo()
        if logo: st.image(logo, width=60)
    with col_title:
        st.markdown("<h1 style='color:#2c3e50;font-size:24px;margin-top:5px;'>메리츠 설계사 성과 조회</h1>",
                    unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #e2e8f0;margin:10px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='login-box'><h2 style='text-align:center;color:#4a5568;'>🔐 로그인하세요</h2></div>",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        password_input = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력",
                                       label_visibility="collapsed")
        if st.button("로그인", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")
    st.stop()


# ============================================================
# 메인 헤더
# ============================================================
col_logo, col_title = st.columns([1, 4])
with col_logo:
    logo = load_logo()
    if logo: st.image(logo, width=60)
    else: st.write("📊")
with col_title:
    st.markdown("<h1 style='color:#2c3e50;font-size:24px;margin-top:5px;'>메리츠 설계사 성과 조회</h1>",
                unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #e2e8f0;margin:8px 0;'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 실적조회", "📞 전화번호 조회", "👔 매니저별 발송"])


# ============================================================
# 탭1: 실적조회
# ============================================================
with tab1:
    df = load_data_from_google_sheets()
    if df is None: st.stop()
    current_week = get_current_week()

    st.markdown("<h3 style='color:#4a5568;margin-top:12px;margin-bottom:12px;font-size:16px;'>🔍 검색 정보 입력</h3>",
                unsafe_allow_html=True)
    ga4_branches = [f"GA4-{i}지점" for i in range(1, 14)]

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown("<div class='search-label'>📍 지점명</div>", unsafe_allow_html=True)
        selected_branch = st.selectbox("지점명", ga4_branches, index=1,
                                       label_visibility="collapsed", key="branch")
    with col2:
        st.markdown("<div class='search-label'>👔 설계사명</div>", unsafe_allow_html=True)
        agent_name = st.text_input("설계사명", placeholder="예: 홍길동",
                                   label_visibility="collapsed", key="agent", autocomplete="off")
    with col3:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        search_clicked = st.button("🔍 검색", use_container_width=True)

    if search_clicked:
        if not agent_name:
            st.error("⚠️ 설계사명을 입력해주세요.")
            st.session_state.search_performed = False
            st.session_state.show_duplicates = False
        else:
            filtered = df[
                (df["지점명"].astype(str).str.strip() == selected_branch.strip()) &
                (df["설계사명"].astype(str).str.strip() == agent_name.strip())
            ]
            if len(filtered) == 0:
                st.error("❌ 데이터를 찾을 수 없습니다")
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
        st.markdown("<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>동명이인이 있습니다. 선택해주세요:</p>",
                    unsafe_allow_html=True)
        for idx, (row_idx, agent_row) in enumerate(st.session_state.filtered_data.iterrows()):
            agent_display = f"{str(agent_row.get('지점명','N/A')).strip()} | {str(agent_row.get('지사명','N/A')).strip()}"
            if st.button(agent_display, key=f"agent_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.selected_row = agent_row
                st.session_state.search_performed = True
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None
                st.rerun()

    if st.session_state.search_performed and st.session_state.selected_row is not None:
        row = st.session_state.selected_row
        agent_name_display = str(row["설계사명"]).strip()
        agent_code = str(row.get("현재대리점설계사조직코드","N/A")).strip()
        agency_branch = str(row.get("지사명","N/A")).strip()
        agency_name = str(row["대리점"]).strip()
        branch = str(row["지점명"]).strip()

        manager_name_val = str(row.get(df.columns[3], "N/A")).strip()
        st.markdown("<h3 style='color:#4a5568;'>📋 기본 정보</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='info-box'>
        <strong>지사명:</strong> {agency_branch}<br>
        <strong>설계사명(코드):</strong> {agent_name_display} ({agent_code})<br>
        <strong>매니저명:</strong> {manager_name_val}
        </div>""", unsafe_allow_html=True)

        cumulative = row["누계실적"]
        st.markdown("<h3 style='color:#4a5568;'>📈 3월 누계 실적</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='cumulative-box'>{format_display(cumulative)}</div>",
                    unsafe_allow_html=True)

        st.markdown("<h3 style='color:#4a5568;'>📅 주차별 실적</h3>", unsafe_allow_html=True)
        for idx, week_col in enumerate(["1주차","2주차","3주차","4주차","5주차"], 1):
            week_value = row[week_col]
            if idx == current_week:
                st.markdown(f"""
                <div class='weekly-row current'>
                <div><strong>{week_col}</strong> ⭐</div>
                <strong style='color:#92400e;'>{format_display(week_value)}</strong>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='weekly-row'>
                <strong>{week_col}</strong>
                <strong style='color:#48bb78;'>{format_display(week_value)}</strong>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:15px 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#4a5568;'>📱 카카오톡 발송</h3>", unsafe_allow_html=True)
        kakao_message = build_kakao_message(row, df, current_week, greeting="")
        st.text_area("메시지 미리보기", value=kakao_message, height=250,
                     label_visibility="collapsed", key="kakao_preview")
        col_copy1, col_copy2 = st.columns([1, 1])
        with col_copy1:
            copy_to_clipboard_button(kakao_message, button_label="📋 메시지 복사하기",
                                     key="kakao_copy_main")
        with col_copy2:
            st.download_button(label="💾 텍스트 파일로 저장", data=kakao_message,
                file_name=f"{agent_name_display}_{agency_branch}_실적현황.txt",
                mime="text/plain", use_container_width=True)

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:15px 0;'>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True, key="reset_performance"):
            st.session_state.search_performed = False
            st.session_state.selected_row = None
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
            st.rerun()

    elif not st.session_state.show_duplicates:
        st.markdown("""
        <div style='text-align:center;margin-top:30px;padding:30px;background:white;
            border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'>
        <p style='color:#4a5568;font-weight:600;font-size:15px;margin-bottom:8px;'>
            🔒 지점명과 설계사명을 입력하고 검색 버튼을 클릭하세요.</p>
        <p style='color:#718096;font-weight:400;font-size:13px;margin-top:8px;'>
            개인정보 보호를 위해 검색 후에만 데이터가 표시됩니다.</p>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 탭2: 전화번호 조회
# ============================================================
with tab2:
    contact_df = load_contact_data_from_google_sheets()
    performance_df = load_data_from_google_sheets()
    if contact_df is None:
        st.error("❌ 전화번호 데이터를 불러올 수 없습니다.")
        st.stop()

    contact_df['휴대전화_normalized'] = contact_df['휴대전화'].apply(normalize_phone_number)
    st.markdown("<h3 style='color:#4a5568;margin-top:12px;margin-bottom:12px;font-size:16px;'>📞 전화번호 검색</h3>",
                unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='search-label'>🔍 전화번호 또는 설계사명 입력</div>", unsafe_allow_html=True)
        contact_search = st.text_input("검색",
            placeholder="예: 01012345678, 1234567, 123-4567, 홍길동",
            label_visibility="collapsed", key="contact_search", autocomplete="off")
    with col2:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        contact_search_clicked = st.button("🔍 검색", use_container_width=True, key="contact_search_btn")

    if contact_search_clicked:
        if not contact_search:
            st.warning("⚠️ 전화번호 또는 설계사명을 입력해주세요.")
            st.session_state.contact_search_performed = False
            st.session_state.contact_show_duplicates = False
        else:
            search_value = contact_search.strip()
            search_normalized = normalize_phone_number(search_value)
            search_normalized_with_010 = (
                "010" + search_normalized
                if search_normalized.isdigit() and len(search_normalized) <= 8
                else search_normalized
            )
            filtered_contacts = contact_df[
                (contact_df["휴대전화_normalized"].str.contains(search_normalized, na=False)) |
                (contact_df["휴대전화_normalized"].str.contains(search_normalized_with_010, na=False)) |
                (contact_df["설계사명"].astype(str).str.contains(search_value, na=False))
            ]
            if len(filtered_contacts) == 0:
                st.error(f"❌ '{search_value}'에 해당하는 데이터를 찾을 수 없습니다.")
                st.session_state.contact_search_performed = False
                st.session_state.contact_show_duplicates = False
            elif len(filtered_contacts) == 1:
                st.session_state.contact_search_performed = True
                st.session_state.contact_selected_row = filtered_contacts.iloc[0]
                st.session_state.contact_show_duplicates = False
            else:
                filtered_contacts = filtered_contacts.copy()
                filtered_contacts['_sort'] = filtered_contacts['지점'].apply(extract_ga4_number)
                filtered_contacts = filtered_contacts.sort_values('_sort').drop(
                    columns=['_sort']).reset_index(drop=True)
                st.session_state.contact_show_duplicates = True
                st.session_state.contact_filtered_data = filtered_contacts
                st.session_state.contact_search_performed = False

    if st.session_state.contact_show_duplicates and st.session_state.contact_filtered_data is not None:
        st.markdown("<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>",
                    unsafe_allow_html=True)
        for idx, (row_idx, contact_row) in enumerate(st.session_state.contact_filtered_data.iterrows()):
            contact_display = (
                f"{str(contact_row.get('지점','N/A')).strip()} | "
                f"{str(contact_row.get('지사','N/A')).strip()} | "
                f"{str(contact_row.get('설계사명','N/A')).strip()}"
            )
            if st.button(contact_display, key=f"contact_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.contact_selected_row = contact_row
                st.session_state.contact_search_performed = True
                st.session_state.contact_show_duplicates = False
                st.session_state.contact_filtered_data = None
                st.rerun()

    if st.session_state.contact_search_performed and st.session_state.contact_selected_row is not None:
        row = st.session_state.contact_selected_row
        name     = str(row.get("설계사명","N/A")).strip()
        code     = str(row.get("설계사코드","N/A")).strip()
        phone    = str(row.get("휴대전화","N/A")).strip()
        branch   = str(row.get("지사","N/A")).strip()
        office   = str(row.get("지점","N/A")).strip()
        manager  = str(row.get("매니저","N/A")).strip()
        join_date = str(row.get("위촉일자","N/A")).strip()
        prev_month      = format_display(row.get("전월실적",0))
        prev_prev_month = format_display(row.get("전전월실적",0))
        current_month   = format_display(get_current_month_performance(performance_df, code))

        st.markdown("<h3 style='color:#4a5568;'>📋 설계사 정보</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='contact-box'>
        <strong>설계사명:</strong> {name}<br>
        <strong>설계사코드:</strong> {code}<br>
        <strong>📞 휴대전화:</strong>
            <span style='color:#48bb78;font-weight:700;font-size:16px;'>{phone}</span><br>
        <strong>소속지사:</strong> {branch}<br>
        <strong>소속지점:</strong> {office}<br>
        <strong>담당매니저:</strong> {manager}<br>
        <strong>위촉일자:</strong> {join_date}
        </div>""", unsafe_allow_html=True)

        st.markdown("<h3 style='color:#4a5568;'>📊 최근 실적</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='info-box'>
        <strong>1월 실적:</strong> {prev_prev_month}<br>
        <strong>2월 실적:</strong> {prev_month}<br>
        <strong>3월 실적:</strong> {current_month}
        </div>""", unsafe_allow_html=True)

        vcard_content = create_vcard(f"{branch} {name}", phone, branch)
        st.download_button(label="📥 연락처 저장 (vCard)", data=vcard_content,
            file_name=f"{branch}_{name}_연락처.vcf", mime="text/vcard", use_container_width=True)

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:15px 0;'>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True, key="reset_contact"):
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
            st.rerun()

    elif not st.session_state.contact_show_duplicates:
        st.markdown("""
        <div style='text-align:center;margin-top:30px;padding:30px;background:white;
            border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'>
        <p style='color:#4a5568;font-weight:600;font-size:15px;margin-bottom:8px;'>
            📞 전화번호 또는 설계사명을 입력하고 검색하세요.</p>
        <p style='color:#718096;font-weight:400;font-size:13px;margin-top:8px;'>
            예: 01012345678, 1234567, 123-4567, 홍길동</p>
        <p style='color:#48bb78;font-weight:500;font-size:12px;margin-top:12px;'>
            ✨ 010 없이도 검색 가능합니다!</p>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 탭3: 매니저별 발송
# ============================================================
with tab3:
    st.markdown("### 👔 매니저별 발송")

    if "manager_search_performed" not in st.session_state:
        st.session_state.manager_search_performed = False
    if "manager_agent_list" not in st.session_state:
        st.session_state.manager_agent_list = pd.DataFrame()
    if "manager_name_display" not in st.session_state:
        st.session_state.manager_name_display = ""
    if "manager_expanded_idx" not in st.session_state:
        st.session_state.manager_expanded_idx = None
    if "manager_filter_mode" not in st.session_state:
        st.session_state.manager_filter_mode = 0
    if "manager_duplicate_list" not in st.session_state:
        st.session_state.manager_duplicate_list = []
    if "manager_duplicate_selected" not in st.session_state:
        st.session_state.manager_duplicate_selected = None

    df_main = load_data_from_google_sheets()
    current_week = get_current_week()

    col_names      = list(df_main.columns)
    mgr_name_col   = col_names[3]
    mgr_code_col   = col_names[4]
    branch_col_mgr = col_names[2]

    # ── 검색창 ──
    search_col1, search_col2 = st.columns([4, 1])
    with search_col1:
        manager_search_input = st.text_input(
            "매니저 검색",
            placeholder="매니저 코드 또는 이름 입력 (예: 326111222, 박메리)",
            key="manager_search_input"
        )
    with search_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 조회", key="manager_search_btn", use_container_width=True)

    # ── 검색 실행 ──
    if search_btn and manager_search_input.strip():
        query = manager_search_input.strip()
        mask = (
            (df_main[mgr_name_col].astype(str).str.strip() == query) |
            (df_main[mgr_code_col].astype(str).str.strip() == query)
        )
        matched = df_main[mask].copy()

        if matched.empty:
            st.warning(f"'{query}'에 해당하는 매니저를 찾을 수 없습니다.")
            st.session_state.manager_search_performed = False
            st.session_state.manager_duplicate_list = []
            st.session_state.manager_duplicate_selected = None
        else:
            unique_codes = matched[mgr_code_col].astype(str).str.strip().unique()
            if len(unique_codes) > 1:
                def extract_ga4_num_dup(s):
                    m = re.search(r'GA4[-\s]?(\d+)', str(s), re.IGNORECASE)
                    return int(m.group(1)) if m else 9999
                dup_list = []
                for code in unique_codes:
                    sub = df_main[df_main[mgr_code_col].astype(str).str.strip() == code]
                    branch_val = str(sub[branch_col_mgr].iloc[0]).strip() if not sub.empty else ""
                    mgr_nm_dup = str(sub[mgr_name_col].iloc[0]).strip() if not sub.empty else query
                    dup_list.append({
                        "code": code, "name": mgr_nm_dup,
                        "branch": branch_val,
                        "label": f"{branch_val}  |  {code}"
                    })
                dup_list.sort(key=lambda x: extract_ga4_num_dup(x["branch"]))
                st.session_state.manager_duplicate_list = dup_list
                st.session_state.manager_duplicate_selected = None
                st.session_state.manager_search_performed = False
            else:
                st.session_state.manager_duplicate_list = []
                st.session_state.manager_duplicate_selected = None
                agents = matched.copy()
                cumul_col = next((c for c in ["누계실적","누계","cumulative"] if c in agents.columns), None)
                if cumul_col:
                    agents["_cumul_float"] = agents[cumul_col].apply(safe_float)
                    agents = agents[agents["_cumul_float"] > 0].sort_values(
                        "_cumul_float", ascending=False).reset_index(drop=True)
                st.session_state.manager_agent_list = agents
                st.session_state.manager_name_display = str(matched[mgr_name_col].iloc[0]).strip()
                st.session_state.manager_search_performed = True
                st.session_state.manager_expanded_idx = None

    # ── 동명이인 ──
    if st.session_state.manager_duplicate_list:
        st.markdown(
            "<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>"
            "동명이인 매니저가 있습니다. 선택해주세요:</p>",
            unsafe_allow_html=True
        )
        for dup in st.session_state.manager_duplicate_list:
            if st.button(dup["label"], key=f"mgr_dup_{dup['code']}", use_container_width=True):
                sel_mask = df_main[mgr_code_col].astype(str).str.strip() == dup["code"]
                agents = df_main[sel_mask].copy()
                cumul_col = next((c for c in ["누계실적","누계","cumulative"] if c in agents.columns), None)
                if cumul_col:
                    agents["_cumul_float"] = agents[cumul_col].apply(safe_float)
                    agents = agents[agents["_cumul_float"] > 0].sort_values(
                        "_cumul_float", ascending=False).reset_index(drop=True)
                st.session_state.manager_agent_list = agents
                st.session_state.manager_name_display = f"{dup['name']} ({dup['branch']})"
                st.session_state.manager_duplicate_list = []
                st.session_state.manager_duplicate_selected = dup["code"]
                st.session_state.manager_search_performed = True
                st.session_state.manager_expanded_idx = None
                st.rerun()

    # ── 설계사 리스트 표시 ──
    if (
        st.session_state.manager_search_performed
        and st.session_state.manager_agent_list is not None
        and not st.session_state.manager_agent_list.empty
    ):
        all_agents = st.session_state.manager_agent_list
        mgr_name   = st.session_state.manager_name_display

        # 인사말
        st.markdown("""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
            padding:6px 12px;border-radius:8px;margin:8px 0 3px 0;'>
        <span style='color:white;font-size:11px;font-weight:500;'>
        💬 인사말을 입력하면 각 설계사 메시지 맨 앞에 자동으로 추가됩니다.</span>
        </div>""", unsafe_allow_html=True)
        greeting_text = st.text_area(
            "인사말", placeholder="예: 안녕하세요! 이번 주도 파이팅입니다 💪",
            height=60, label_visibility="collapsed", key="manager_greeting"
        )

        # 필터 + 카운트
        filter_options = {"📋 전체":0,"📅 현재주차 유실적자":1}
        col_filter, col_count = st.columns([3, 1])
        with col_filter:
            selected_filter_label = st.selectbox(
                "대상자 필터", list(filter_options.keys()),
                index=st.session_state.manager_filter_mode,
                label_visibility="collapsed", key="manager_filter_select"
            )
            new_filter_mode = filter_options[selected_filter_label]
            if new_filter_mode != st.session_state.manager_filter_mode:
                st.session_state.manager_filter_mode = new_filter_mode
                st.session_state.manager_expanded_idx = None
                st.rerun()

        filtered_agents = apply_manager_filter(
            all_agents, st.session_state.manager_filter_mode, current_week
        )

        with col_count:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#4a5568 0%,#2d3748 100%);
                padding:6px 10px;border-radius:8px;text-align:center;margin-top:2px;'>
            <span style='color:#ffd93d;font-weight:700;font-size:12px;'>{mgr_name}</span><br>
            <span style='color:white;font-size:12px;font-weight:600;'>{len(filtered_agents)}명</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        if len(filtered_agents) == 0:
            st.markdown("""
            <div style='text-align:center;padding:16px;background:white;border-radius:10px;
                color:#718096;font-size:14px;'>해당 조건의 설계사가 없습니다.</div>""",
                unsafe_allow_html=True)
        else:
            # ── 각 행 데이터 및 메시지 미리 계산 ──
            rows_data = []
            for i, (_, agent_row) in enumerate(filtered_agents.iterrows()):
                agent_nm     = str(agent_row["설계사명"]).strip()
                agent_branch = str(agent_row.get("지사명","")).strip()
                agent_office = str(agent_row.get("지점명","")).strip()
                cumul_val    = format_display(agent_row["누계실적"])

                border_colors = ["#f59e0b","#94a3b8","#86efac"]
                border_color  = border_colors[i] if i < 3 else "#cbd5e1"
                rank_emojis   = ["🥇","🥈","🥉"]
                rank_label    = rank_emojis[i] if i < 3 else f"#{i+1}"

                # 주차별 실적 (현재 주차까지만)
                week_cols_list = ["1주차","2주차","3주차","4주차","5주차"]
                week_lines = ""
                for wi, wc in enumerate(week_cols_list, 1):
                    if wi > current_week:
                        break
                    wv = format_display(agent_row[wc])
                    if wi == current_week:
                        week_lines += (
                            f"<div class='week-row'>"
                            f"<span style='color:#92400e;font-weight:700;'>{wc} ⭐</span>"
                            f"<span style='color:#92400e;font-weight:700;'>{wv}</span>"
                            f"</div>"
                        )
                    else:
                        week_lines += (
                            f"<div class='week-row'>"
                            f"<span style='color:#64748b;'>{wc}</span>"
                            f"<span style='color:#334155;font-weight:600;'>{wv}</span>"
                            f"</div>"
                        )

                # 카카오 메시지
                raw_msg = build_kakao_message(agent_row, df_main, current_week, greeting=greeting_text)
                escaped_msg = (
                    raw_msg
                    .replace("\\", "\\\\")
                    .replace("`", "\\`")
                    .replace("$", "\\$")
                    .replace("\r\n", "\\n")
                    .replace("\n", "\\n")
                )

                rows_data.append({
                    "i": i,
                    "agent_nm": agent_nm,
                    "agent_branch": agent_branch,
                    "agent_office": agent_office,
                    "cumul_val": cumul_val,
                    "border_color": border_color,
                    "rank_label": rank_label,
                    "week_lines": week_lines,
                    "escaped_msg": escaped_msg,
                })

            # ── 전체 HTML 빌드 ──
            items_html = ""
            for rd in rows_data:
                i            = rd["i"]
                agent_nm     = rd["agent_nm"]
                agent_branch = rd["agent_branch"]
                agent_office = rd["agent_office"]
                cumul_val    = rd["cumul_val"]
                border_color = rd["border_color"]
                rank_label   = rd["rank_label"]
                week_lines   = rd["week_lines"]
                escaped_msg  = rd["escaped_msg"]

                items_html += f"""
                <div class="card" id="card_{i}" style="border-left:3px solid {border_color};">
                  <div class="card-main" onclick="toggle({i})">
                    <div class="card-info">
                      <span class="rank">{rank_label}</span>
                      <span class="name">{agent_nm}</span>
                      <span class="sub"> · {agent_office} | {agent_branch}</span>
                      <span class="cumul">{cumul_val}</span>
                    </div>
                    <button class="copy-btn" id="cbtn_{i}"
                      onclick="event.stopPropagation(); copyMsg({i})">
                      📋 복사
                    </button>
                  </div>
                  <div class="detail" id="detail_{i}">
                    <div class="cumul-bar">📈 3월 누계: {cumul_val}</div>
                    <div class="detail-row" style="border-left-color:#38bdf8;flex-direction:column;align-items:stretch;">
                      <span class="dl" style="margin-bottom:3px;">📅 주차별 실적</span>
                      {week_lines}
                    </div>
                  </div>
                </div>
                <script>messages[{i}] = `{escaped_msg}`;</script>
                """

            # 높이: 항목당 44px 기본 + 상세 펼쳤을 때 여유분
            estimated_height = len(rows_data) * 44 + 220

            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
              * {{ box-sizing:border-box; margin:0; padding:0;
                   font-family:'Noto Sans KR',sans-serif; }}
              body {{ background:#f8f9fa; padding:2px 0 8px 0; overflow:hidden; }}

              .card {{
                background:#fff;
                border-bottom:1px solid #f1f5f9;
                overflow:hidden;
              }}
              .card:first-of-type {{ border-radius:8px 8px 0 0; }}
              .card:last-of-type  {{ border-radius:0 0 8px 8px; border-bottom:none; }}

              .card-main {{
                display:flex;
                align-items:center;
                padding:5px 6px 5px 10px;
                cursor:pointer;
                min-height:38px;
                gap:6px;
              }}
              .card-main:active {{ background:#f0f4f8; }}

              .card-info {{
                flex:1;
                min-width:0;
                font-size:12px;
                line-height:1.35;
              }}
              .rank  {{ font-weight:700; margin-right:3px; font-size:12px; }}
              .name  {{ font-weight:700; color:#1e293b; font-size:12px; }}
              .sub   {{ color:#64748b; font-size:10px; }}
              .cumul {{ color:#16a34a; font-weight:700; font-size:12px;
                        display:block; margin-top:1px; }}

              .copy-btn {{
                flex-shrink:0;
                background:linear-gradient(135deg,#4a5568,#2d3748);
                color:white; border:none; border-radius:6px;
                padding:5px 10px; font-size:11px; font-weight:600;
                cursor:pointer; white-space:nowrap;
                font-family:'Noto Sans KR',sans-serif;
                box-shadow:0 1px 3px rgba(74,85,104,0.35);
                min-width:52px; text-align:center;
              }}

              .detail {{
                display:none;
                background:#f8fafc;
                border-top:1px dashed #e2e8f0;
                padding:8px 10px;
                font-size:11px;
              }}
              .cumul-bar {{
                background:linear-gradient(135deg,#1e293b,#334155);
                color:white; font-weight:700; font-size:12px;
                border-radius:6px; padding:5px 10px;
                text-align:center; margin-bottom:5px;
              }}
              .detail-row {{
                background:white;
                border-left:3px solid #e2e8f0;
                border-radius:5px;
                padding:4px 8px;
                margin:3px 0;
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:6px;
                flex-wrap:wrap;
              }}
              .dl {{ color:#64748b; flex-shrink:0; font-weight:500; font-size:11px; }}
              .dr {{ color:#334155; font-weight:600; text-align:right;
                     flex:1; font-size:11px; }}
              .week-row {{
                display:flex;
                justify-content:space-between;
                padding:2px 0;
                font-size:11px;
              }}
            </style>
            </head>
            <body>

            <script>
              var messages = {{}};
              var openIdx  = -1;

              function toggle(i) {{
                var el = document.getElementById('detail_' + i);
                if (!el) return;

                if (openIdx === i) {{
                  el.style.display = 'none';
                  openIdx = -1;
                }} else {{
                  if (openIdx >= 0) {{
                    var prev = document.getElementById('detail_' + openIdx);
                    if (prev) prev.style.display = 'none';
                  }}
                  el.style.display = 'block';
                  openIdx = i;
                  setTimeout(function() {{
                    document.getElementById('card_' + i).scrollIntoView(
                      {{behavior:'smooth', block:'nearest'}}
                    );
                    resizeFrame();
                  }}, 50);
                }}
                resizeFrame();
              }}

              function resizeFrame() {{
                setTimeout(function() {{
                  var h = document.documentElement.scrollHeight;
                  window.parent.postMessage(
                    {{type:'streamlit:setFrameHeight', height: h + 20}},
                    '*'
                  );
                }}, 100);
              }}

              function copyMsg(i) {{
                var text = messages[i].replace(/\\\\n/g, '\\n');
                var btn  = document.getElementById('cbtn_' + i);
                function flash() {{
                  if (!btn) return;
                  var orig = btn.innerHTML;
                  btn.innerHTML = '✅';
                  btn.style.background = 'linear-gradient(135deg,#38a169,#276749)';
                  setTimeout(function() {{
                    btn.innerHTML = orig;
                    btn.style.background = 'linear-gradient(135deg,#4a5568,#2d3748)';
                  }}, 2000);
                }}
                if (navigator.clipboard && window.isSecureContext) {{
                  navigator.clipboard.writeText(text).then(flash,
                    function() {{ fallback(text, flash); }});
                }} else {{ fallback(text, flash); }}
              }}

              function fallback(text, cb) {{
                var el = document.createElement('textarea');
                el.value = text;
                el.style.position = 'fixed'; el.style.left = '-9999px';
                document.body.appendChild(el);
                el.focus(); el.select();
                try {{ document.execCommand('copy'); cb(); }}
                catch(e) {{ alert('복사 실패'); }}
                document.body.removeChild(el);
              }}

              window.addEventListener('load', function() {{
                resizeFrame();
              }});
            </script>

            <div style="background:white; border-radius:8px;
                        box-shadow:0 2px 10px rgba(0,0,0,0.08); overflow:visible;">
              {items_html}
            </div>

            </body>
            </html>
            """

            components.html(full_html, height=estimated_height, scrolling=True)

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:12px 0;'>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True, key="reset_manager"):
            st.session_state.manager_search_performed = False
            st.session_state.manager_agent_list = pd.DataFrame()
            st.session_state.manager_name_display = ""
            st.session_state.manager_expanded_idx = None
            st.session_state.manager_filter_mode = 0
            st.session_state.manager_duplicate_list = []
            st.session_state.manager_duplicate_selected = None
            st.rerun()

    elif not st.session_state.manager_search_performed and not st.session_state.manager_duplicate_list:
        st.markdown("""
        <div style='text-align:center;margin-top:30px;padding:30px;background:white;
            border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'>
        <p style='color:#4a5568;font-weight:600;font-size:15px;margin-bottom:8px;'>
            👔 매니저코드 또는 매니저명을 입력하고 조회하세요.</p>
        <p style='color:#718096;font-weight:400;font-size:13px;margin-top:8px;'>
            조회된 유실적자를 고실적 순으로 확인하고 카카오톡 메시지를 바로 복사할 수 있습니다.</p>
        <p style='color:#48bb78;font-weight:500;font-size:12px;margin-top:12px;'>
            ✨ 대상자 클릭으로 상세실적 확인, 메시지 복사 버튼으로 바로 발송하세요!</p>
        </div>""", unsafe_allow_html=True)
