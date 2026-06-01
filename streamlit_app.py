import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import os
import streamlit.components.v1 as components
import re


# ============================================================
# 기본 설정
# ============================================================
PASSWORD = "2233"

DATA_FILE_PATH = "data.xlsx"
PHONE_FILE_PATH = "phone.xlsx"

st.set_page_config(page_title="메리츠 실적현황", layout="wide")


# ============================================================
# 컬럼명 매핑
# ============================================================
COLS = {
    "manager": "매니저명",
    "manager_code": "매니저코드",

    "agent_code": "현재대리점설계사조직코드",
    "agent_name": "현재대리점설계사조직명",

    "agency_name": "현재영업가족명",
    "branch_name": "현재대리점지사명",
    "hq_name": "현재영업단조직명",
    "office_name": "현재지점조직명",

    "current_cumulative": "인정실적",
    "prev_cumulative": "이전월인정실적",
    "prev_prev_cumulative": "전전월인정실적",
}


def get_week_col(week_num):
    return f"실적_{week_num}주차"


def get_week_columns():
    return [get_week_col(i) for i in range(1, 6)]


# ============================================================
# CSS
# ============================================================
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
    background: rgba(255,255,255,0.95) !important;
}

h1, h2, h3 {
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #2c3e50;
}

.stButton > button {
    font-weight: 600;
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(74,85,104,0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
    box-shadow: 0 4px 15px rgba(74,85,104,0.4);
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
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
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
    box-shadow: 0 2px 12px rgba(74,85,104,0.25);
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
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-weight: 600;
    color: #2c3e50;
}

.weekly-row.current {
    background: linear-gradient(135deg, #ffd93d 0%, #ffb93d 100%);
    border-left: 4px solid #f59e0b;
    box-shadow: 0 2px 10px rgba(245,158,11,0.3);
    color: #92400e;
}

.search-label {
    font-weight: 600;
    font-size: 13px;
    color: #4a5568;
    margin-bottom: 6px;
    display: block;
}

.login-box {
    max-width: 320px;
    margin: 30px auto;
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
}

.update-box {
    text-align: right;
    color: #718096;
    font-size: 12px;
    font-weight: 500;
    margin-top: -6px;
    margin-bottom: 6px;
}

.manager-card {
    background: white;
    border-left: 4px solid #4a5568;
    border-radius: 10px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.manager-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.manager-name {
    font-size: 15px;
    font-weight: 700;
    color: #1e293b;
}

.manager-sub {
    font-size: 12px;
    color: #64748b;
}

.manager-money {
    font-size: 15px;
    font-weight: 700;
    color: #16a34a;
}

h3 {
    font-size: 16px !important;
    margin-top: 12px !important;
    margin-bottom: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 유틸 함수
# ============================================================
def safe_float(value):
    if pd.isna(value):
        return 0.0

    if value is None or value == "":
        return 0.0

    try:
        v = str(value).strip()

        if v == "" or v.lower() == "nan":
            return 0.0

        if "만원" in v:
            return float(v.replace("만원", "").replace(",", "").strip()) * 10000

        return float(v.replace(",", ""))

    except:
        return 0.0


def format_display(value):
    v = str(value).strip()

    if v == "" or v.lower() == "nan" or v == "None":
        return "₩ 0"

    try:
        if "만원" in v:
            num = float(v.replace("만원", "").replace(",", "").strip()) * 10000
            return f"₩ {num:,.0f}"

        num = float(v.replace(",", ""))
        return f"₩ {num:,.0f}"

    except:
        return v


def normalize_phone_number(phone):
    if pd.isna(phone):
        return ""

    return (
        str(phone)
        .replace("-", "")
        .replace(" ", "")
        .replace(".0", "")
        .strip()
    )


def extract_ga4_number(branch_str):
    match = re.search(r"GA4[-\s]?(\d+)", str(branch_str), re.IGNORECASE)
    return int(match.group(1)) if match else 9999


def get_current_month():
    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).date()
    return today.month


def get_prev_months():
    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).date()

    current_month = today.month
    prev_month = current_month - 1
    prev_prev_month = current_month - 2

    if prev_month <= 0:
        prev_month += 12

    if prev_prev_month <= 0:
        prev_prev_month += 12

    return current_month, prev_month, prev_prev_month


def get_current_week():
    kst = pytz.timezone("Asia/Seoul")
    today = datetime.datetime.now(kst).date()
    day = today.day

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


def get_file_modified_time(file_path):
    try:
        modified_timestamp = os.path.getmtime(file_path)
        kst = pytz.timezone("Asia/Seoul")
        modified_dt = datetime.datetime.fromtimestamp(modified_timestamp, kst)
        return modified_dt.strftime("%Y-%m-%d %H:%M")

    except:
        return None


def require_columns(df, required_cols, title="데이터"):
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(
            f"❌ {title}에 필요한 컬럼이 없습니다.\n\n"
            f"누락 컬럼: {', '.join(missing)}"
        )
        return False

    return True


def load_logo():
    if os.path.exists("meritz.png"):
        return Image.open("meritz.png")

    return None


def create_vcard(name, phone, company):
    phone_clean = normalize_phone_number(phone)

    return (
        f"BEGIN:VCARD\n"
        f"VERSION:3.0\n"
        f"FN:{name}\n"
        f"TEL;TYPE=CELL:{phone_clean}\n"
        f"ORG:{company}\n"
        f"END:VCARD"
    )


# ============================================================
# 엑셀 로드
# ============================================================
@st.cache_data(ttl=300)
def load_data_from_excel():
    try:
        df = pd.read_excel(DATA_FILE_PATH, dtype=str)
        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        st.error(f"실적 데이터 로드 실패: {e}")
        return None


@st.cache_data(ttl=300)
def load_contact_data_from_excel():
    try:
        df = pd.read_excel(PHONE_FILE_PATH, dtype=str)
        df.columns = df.columns.str.strip()

        df = df.rename(columns={
            "이름": "설계사명",
            "ID": "설계사코드",
            "휴대전화": "휴대전화",
            "지사": "지사",
            "지점": "지점",
            "매니저": "매니저",
            "위촉일자": "위촉일자",
        })

        return df

    except Exception as e:
        st.error(f"전화번호 데이터 로드 실패: {e}")
        return None


# ============================================================
# 복사 버튼
# ============================================================
def copy_to_clipboard_button(text, button_label="📋 메시지 복사하기", key="clipboard_btn", height=80):
    escaped_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("$", "\\$")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )

    components.html(f"""
        <button onclick="copyText_{key}()" style="
            font-family:'Noto Sans KR',sans-serif;
            font-weight:600;
            background:linear-gradient(135deg,#4a5568 0%,#2d3748 100%);
            border:none;
            border-radius:8px;
            padding:8px 16px;
            color:white;
            cursor:pointer;
            width:100%;
            font-size:13px;
            box-shadow:0 2px 8px rgba(74,85,104,0.3);">
            {button_label}
        </button>

        <div id="copyMsg_{key}" style="
            display:none;
            margin-top:6px;
            padding:6px 10px;
            background:#c6f6d5;
            border-left:4px solid #48bb78;
            border-radius:6px;
            color:#276749;
            font-family:'Noto Sans KR',sans-serif;
            font-size:12px;
            font-weight:600;">
            ✅ 복사 완료! 카카오톡에 붙여넣기 하세요.
        </div>

        <script>
        function copyText_{key}() {{
            const text = `{escaped_text}`.replace(/\\\\n/g, '\\n');

            function showSuccess() {{
                const msg = document.getElementById('copyMsg_{key}');
                msg.style.display = 'block';

                setTimeout(function() {{
                    msg.style.display = 'none';
                }}, 2500);
            }}

            function fallbackCopy(text) {{
                const el = document.createElement('textarea');
                el.value = text;
                el.style.position = 'fixed';
                el.style.left = '-9999px';

                document.body.appendChild(el);
                el.focus();
                el.select();

                try {{
                    document.execCommand('copy');
                    showSuccess();
                }} catch(e) {{
                    alert('복사 실패: 메시지를 직접 드래그하여 복사해주세요.');
                }}

                document.body.removeChild(el);
            }}

            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(showSuccess, function() {{
                    fallbackCopy(text);
                }});
            }} else {{
                fallbackCopy(text);
            }}
        }}
        </script>
    """, height=height)


# ============================================================
# 메시지 생성
# ============================================================
def build_kakao_message(row, current_week, greeting=""):
    current_month = get_current_month()

    agency_branch = str(row.get(COLS["branch_name"], "N/A")).strip()
    agent_name_display = str(row.get(COLS["agent_name"], "N/A")).strip()
    cumulative = row.get(COLS["current_cumulative"], 0)

    week_text = ""

    for idx in range(1, 6):
        if idx > current_week:
            break

        week_col = get_week_col(idx)

        if week_col not in row.index:
            continue

        current_mark = " ⭐" if idx == current_week else ""
        week_text += f" • {idx}주차: {format_display(row.get(week_col, 0))}{current_mark}\n"

    greeting_line = f"{greeting}\n\n" if greeting.strip() else ""

    return f"""{greeting_line}📊메리츠 {current_month}월 실적 현황
{agency_branch} {agent_name_display}팀장님!

📈 {current_month}월 누계 실적
 {format_display(cumulative)}

📅 주차별 실적
{week_text}
💡 시상관련 궁금하신게 있다면 문의주세요~
이번주도 화이팅입니다!"""


def apply_manager_filter(agents_df, filter_mode, current_week):
    if filter_mode == 0:
        return agents_df

    if filter_mode == 1:
        col = get_week_col(current_week)

        if col in agents_df.columns:
            return agents_df[agents_df[col].apply(safe_float) > 0]

    return agents_df


def get_performance_row_by_agent_code(performance_df, agent_code):
    try:
        if performance_df is None:
            return None

        if COLS["agent_code"] not in performance_df.columns:
            return None

        filtered = performance_df[
            performance_df[COLS["agent_code"]].astype(str).str.strip()
            == str(agent_code).strip()
        ]

        if len(filtered) > 0:
            return filtered.iloc[0]

        return None

    except:
        return None


def get_recent_performance_html(performance_df, contact_row):
    current_month, prev_month, prev_prev_month = get_prev_months()

    code = str(contact_row.get("설계사코드", "")).strip()
    perf_row = get_performance_row_by_agent_code(performance_df, code)

    if perf_row is not None:
        current_value = format_display(perf_row.get(COLS["current_cumulative"], 0))
        prev_value = format_display(perf_row.get(COLS["prev_cumulative"], 0))
        prev_prev_value = format_display(perf_row.get(COLS["prev_prev_cumulative"], 0))
    else:
        current_value = "₩ 0"
        prev_value = format_display(contact_row.get("전월실적", 0))
        prev_prev_value = format_display(contact_row.get("전전월실적", 0))

    return f"""
    <div class='info-box'>
    <strong>{prev_prev_month}월 실적:</strong> {prev_prev_value}<br>
    <strong>{prev_month}월 실적:</strong> {prev_value}<br>
    <strong>{current_month}월 실적:</strong> {current_value}
    </div>
    """


# ============================================================
# 세션 상태 초기화
# ============================================================
defaults = {
    "authenticated": False,

    "search_performed": False,
    "selected_row": None,
    "show_duplicates": False,
    "filtered_data": None,

    "contact_search_performed": False,
    "contact_selected_row": None,
    "contact_show_duplicates": False,
    "contact_filtered_data": None,

    "manager_search_performed": False,
    "manager_agent_list": pd.DataFrame(),
    "manager_name_display": "",
    "manager_filter_mode": 0,
    "manager_duplicate_list": [],
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
        if logo:
            st.image(logo, width=60)

    with col_title:
        st.markdown(
            "<h1 style='color:#2c3e50;font-size:24px;margin-top:5px;'>메리츠 설계사 성과 조회</h1>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border:1px solid #e2e8f0;margin:10px 0;'>", unsafe_allow_html=True)

    st.markdown(
        "<div class='login-box'><h2 style='text-align:center;color:#4a5568;'>🔐 로그인하세요</h2></div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([0.5, 2, 0.5])

    with col2:
        password_input = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호 입력",
            label_visibility="collapsed"
        )

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

    if logo:
        st.image(logo, width=60)
    else:
        st.write("📊")

with col_title:
    st.markdown(
        "<h1 style='color:#2c3e50;font-size:24px;margin-top:5px;'>메리츠 설계사 성과 조회</h1>",
        unsafe_allow_html=True
    )

data_modified_at = get_file_modified_time(DATA_FILE_PATH)
phone_modified_at = get_file_modified_time(PHONE_FILE_PATH)

st.markdown(f"""
<div class='update-box'>
    실적 파일 수정일: {data_modified_at or '-'} /
    연락처 파일 수정일: {phone_modified_at or '-'}
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #e2e8f0;margin:8px 0;'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 실적조회", "📞 전화번호 조회", "👔 매니저별 발송"])


# ============================================================
# 탭1: 실적조회
# ============================================================
with tab1:
    df = load_data_from_excel()

    if df is None:
        st.stop()

    required_cols_tab1 = [
        COLS["manager"],
        COLS["agent_code"],
        COLS["agent_name"],
        COLS["agency_name"],
        COLS["branch_name"],
        COLS["hq_name"],
        COLS["office_name"],
        COLS["current_cumulative"],
    ] + get_week_columns()

    if not require_columns(df, required_cols_tab1, "실적 파일 data.xlsx"):
        st.stop()

    current_week = get_current_week()
    current_month = get_current_month()

    st.markdown(
        "<h3 style='color:#4a5568;margin-top:12px;margin-bottom:12px;font-size:16px;'>🔍 검색 정보 입력</h3>",
        unsafe_allow_html=True
    )

    ga4_branches = (
        df[COLS["office_name"]]
        .dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .tolist()
    )

    ga4_branches = sorted(ga4_branches, key=extract_ga4_number)

    if len(ga4_branches) == 0:
        st.error("❌ 지점 데이터가 없습니다.")
        st.stop()

    default_index = 1 if len(ga4_branches) > 1 else 0

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown("<div class='search-label'>📍 지점명</div>", unsafe_allow_html=True)
        selected_branch = st.selectbox(
            "지점명",
            ga4_branches,
            index=default_index,
            label_visibility="collapsed",
            key="branch"
        )

    with col2:
        st.markdown("<div class='search-label'>👔 설계사명</div>", unsafe_allow_html=True)
        agent_name = st.text_input(
            "설계사명",
            placeholder="예: 홍길동",
            label_visibility="collapsed",
            key="agent",
            autocomplete="off"
        )

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
                (df[COLS["office_name"]].astype(str).str.strip() == selected_branch.strip())
                & (df[COLS["agent_name"]].astype(str).str.strip() == agent_name.strip())
            ]

            if len(filtered) == 0:
                st.error("❌ 데이터를 찾을 수 없습니다.")
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
        st.markdown(
            "<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>동명이인이 있습니다. 선택해주세요:</p>",
            unsafe_allow_html=True
        )

        for idx, (row_idx, agent_row) in enumerate(st.session_state.filtered_data.iterrows()):
            agent_display = (
                f"{str(agent_row.get(COLS['office_name'], 'N/A')).strip()} | "
                f"{str(agent_row.get(COLS['branch_name'], 'N/A')).strip()} | "
                f"{str(agent_row.get(COLS['agent_code'], 'N/A')).strip()}"
            )

            if st.button(agent_display, key=f"agent_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.selected_row = agent_row
                st.session_state.search_performed = True
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None
                st.rerun()

    if st.session_state.search_performed and st.session_state.selected_row is not None:
        row = st.session_state.selected_row

        agent_name_display = str(row.get(COLS["agent_name"], "N/A")).strip()
        agent_code = str(row.get(COLS["agent_code"], "N/A")).strip()
        agency_branch = str(row.get(COLS["branch_name"], "N/A")).strip()
        agency_name = str(row.get(COLS["agency_name"], "N/A")).strip()
        branch = str(row.get(COLS["office_name"], "N/A")).strip()
        hq_name = str(row.get(COLS["hq_name"], "N/A")).strip()
        manager_name_val = str(row.get(COLS["manager"], "N/A")).strip()

        st.markdown("<h3 style='color:#4a5568;'>📋 기본 정보</h3>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='info-box'>
        <strong>본부:</strong> {hq_name}<br>
        <strong>지점:</strong> {branch}<br>
        <strong>지사명:</strong> {agency_branch}<br>
        <strong>대리점명:</strong> {agency_name}<br>
        <strong>설계사명(코드):</strong> {agent_name_display} ({agent_code})<br>
        <strong>매니저명:</strong> {manager_name_val}
        </div>
        """, unsafe_allow_html=True)

        cumulative = row.get(COLS["current_cumulative"], 0)

        st.markdown(
            f"<h3 style='color:#4a5568;'>📈 {current_month}월 누계 실적</h3>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='cumulative-box'>{format_display(cumulative)}</div>",
            unsafe_allow_html=True
        )

        st.markdown("<h3 style='color:#4a5568;'>📅 주차별 실적</h3>", unsafe_allow_html=True)

        for idx in range(1, 6):
            week_col = get_week_col(idx)

            if week_col not in row.index:
                continue

            week_value = row.get(week_col, 0)

            if idx == current_week:
                st.markdown(f"""
                <div class='weekly-row current'>
                <div><strong>{idx}주차</strong> ⭐</div>
                <strong style='color:#92400e;'>{format_display(week_value)}</strong>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class='weekly-row'>
                <strong>{idx}주차</strong>
                <strong style='color:#48bb78;'>{format_display(week_value)}</strong>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:15px 0;'>", unsafe_allow_html=True)

        st.markdown("<h3 style='color:#4a5568;'>📱 카카오톡 발송</h3>", unsafe_allow_html=True)

        kakao_message = build_kakao_message(row, current_week, greeting="")

        st.text_area(
            "메시지 미리보기",
            value=kakao_message,
            height=250,
            label_visibility="collapsed",
            key="kakao_preview"
        )

        col_copy1, col_copy2 = st.columns([1, 1])

        with col_copy1:
            copy_to_clipboard_button(
                kakao_message,
                button_label="📋 메시지 복사하기",
                key="kakao_copy_main"
            )

        with col_copy2:
            st.download_button(
                label="💾 텍스트 파일로 저장",
                data=kakao_message,
                file_name=f"{agent_name_display}_{agency_branch}_실적현황.txt",
                mime="text/plain",
                use_container_width=True
            )

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
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 탭2: 전화번호 조회
# ============================================================
with tab2:
    contact_df = load_contact_data_from_excel()
    performance_df = load_data_from_excel()

    if contact_df is None:
        st.error("❌ 전화번호 데이터를 불러올 수 없습니다.")
        st.stop()

    required_contact_cols = [
        "휴대전화",
        "설계사명",
        "설계사코드",
        "지사",
        "지점",
        "매니저",
        "위촉일자",
    ]

    if not require_columns(contact_df, required_contact_cols, "연락처 파일 phone.xlsx"):
        st.stop()

    contact_df["휴대전화_normalized"] = contact_df["휴대전화"].apply(normalize_phone_number)

    st.markdown(
        "<h3 style='color:#4a5568;margin-top:12px;margin-bottom:12px;font-size:16px;'>📞 전화번호 검색</h3>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("<div class='search-label'>🔍 전화번호 또는 설계사명 입력</div>", unsafe_allow_html=True)
        contact_search = st.text_input(
            "검색",
            placeholder="예: 01012345678, 1234567, 123-4567, 홍길동",
            label_visibility="collapsed",
            key="contact_search",
            autocomplete="off"
        )

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
                (contact_df["휴대전화_normalized"].str.contains(search_normalized, na=False))
                | (contact_df["휴대전화_normalized"].str.contains(search_normalized_with_010, na=False))
                | (contact_df["설계사명"].astype(str).str.contains(search_value, na=False))
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
                filtered_contacts["_sort"] = filtered_contacts["지점"].apply(extract_ga4_number)
                filtered_contacts = (
                    filtered_contacts
                    .sort_values("_sort")
                    .drop(columns=["_sort"])
                    .reset_index(drop=True)
                )

                st.session_state.contact_show_duplicates = True
                st.session_state.contact_filtered_data = filtered_contacts
                st.session_state.contact_search_performed = False

    if st.session_state.contact_show_duplicates and st.session_state.contact_filtered_data is not None:
        st.markdown(
            "<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>",
            unsafe_allow_html=True
        )

        for idx, (row_idx, contact_row) in enumerate(st.session_state.contact_filtered_data.iterrows()):
            contact_display = (
                f"{str(contact_row.get('지점', 'N/A')).strip()} | "
                f"{str(contact_row.get('지사', 'N/A')).strip()} | "
                f"{str(contact_row.get('설계사명', 'N/A')).strip()}"
            )

            if st.button(contact_display, key=f"contact_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.contact_selected_row = contact_row
                st.session_state.contact_search_performed = True
                st.session_state.contact_show_duplicates = False
                st.session_state.contact_filtered_data = None
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
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color:#4a5568;'>📊 최근 실적</h3>", unsafe_allow_html=True)
        st.markdown(get_recent_performance_html(performance_df, row), unsafe_allow_html=True)

        vcard_content = create_vcard(f"{branch} {name}", phone, branch)

        st.download_button(
            label="📥 연락처 저장 (vCard)",
            data=vcard_content,
            file_name=f"{branch}_{name}_연락처.vcf",
            mime="text/vcard",
            use_container_width=True
        )

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
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 탭3: 매니저별 발송
# ============================================================
with tab3:
    st.markdown("### 👔 매니저별 발송")

    df_main = load_data_from_excel()

    if df_main is None:
        st.stop()

    required_cols_manager = [
        COLS["manager"],
        COLS["manager_code"],
        COLS["agent_code"],
        COLS["agent_name"],
        COLS["branch_name"],
        COLS["office_name"],
        COLS["current_cumulative"],
    ] + get_week_columns()

    if not require_columns(df_main, required_cols_manager, "실적 파일 data.xlsx"):
        st.stop()

    current_week = get_current_week()
    current_month = get_current_month()

    search_col1, search_col2 = st.columns([4, 1])

    with search_col1:
        manager_search_input = st.text_input(
            "매니저 검색",
            placeholder="매니저 코드 또는 이름 입력",
            key="manager_search_input"
        )

    with search_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 조회", key="manager_search_btn", use_container_width=True)

    if search_btn and manager_search_input.strip():
        query = manager_search_input.strip()

        mask = (
            (df_main[COLS["manager"]].astype(str).str.strip() == query)
            | (df_main[COLS["manager_code"]].astype(str).str.strip() == query)
        )

        matched = df_main[mask].copy()

        if matched.empty:
            st.warning(f"'{query}'에 해당하는 매니저를 찾을 수 없습니다.")
            st.session_state.manager_search_performed = False
            st.session_state.manager_duplicate_list = []

        else:
            unique_codes = matched[COLS["manager_code"]].astype(str).str.strip().unique()

            if len(unique_codes) > 1:
                dup_list = []

                for code in unique_codes:
                    sub = df_main[df_main[COLS["manager_code"]].astype(str).str.strip() == code]

                    branch_val = str(sub[COLS["office_name"]].iloc[0]).strip() if not sub.empty else ""
                    mgr_nm_dup = str(sub[COLS["manager"]].iloc[0]).strip() if not sub.empty else query

                    dup_list.append({
                        "code": code,
                        "name": mgr_nm_dup,
                        "branch": branch_val,
                        "label": f"{mgr_nm_dup} | {branch_val} | {code}"
                    })

                dup_list.sort(key=lambda x: extract_ga4_number(x["branch"]))

                st.session_state.manager_duplicate_list = dup_list
                st.session_state.manager_search_performed = False

            else:
                agents = matched.copy()
                agents["_cumul_float"] = agents[COLS["current_cumulative"]].apply(safe_float)
                agents = (
                    agents[agents["_cumul_float"] > 0]
                    .sort_values("_cumul_float", ascending=False)
                    .reset_index(drop=True)
                )

                st.session_state.manager_duplicate_list = []
                st.session_state.manager_agent_list = agents
                st.session_state.manager_name_display = str(matched[COLS["manager"]].iloc[0]).strip()
                st.session_state.manager_search_performed = True

    if st.session_state.manager_duplicate_list:
        st.markdown(
            "<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>"
            "동명이인 매니저가 있습니다. 선택해주세요:</p>",
            unsafe_allow_html=True
        )

        for dup in st.session_state.manager_duplicate_list:
            if st.button(dup["label"], key=f"mgr_dup_{dup['code']}", use_container_width=True):
                sel_mask = df_main[COLS["manager_code"]].astype(str).str.strip() == dup["code"]

                agents = df_main[sel_mask].copy()
                agents["_cumul_float"] = agents[COLS["current_cumulative"]].apply(safe_float)
                agents = (
                    agents[agents["_cumul_float"] > 0]
                    .sort_values("_cumul_float", ascending=False)
                    .reset_index(drop=True)
                )

                st.session_state.manager_agent_list = agents
                st.session_state.manager_name_display = f"{dup['name']} ({dup['branch']})"
                st.session_state.manager_duplicate_list = []
                st.session_state.manager_search_performed = True

                st.rerun()

    if (
        st.session_state.manager_search_performed
        and st.session_state.manager_agent_list is not None
        and not st.session_state.manager_agent_list.empty
    ):
        all_agents = st.session_state.manager_agent_list
        mgr_name = st.session_state.manager_name_display

        st.markdown("""
        <div style='background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
            padding:6px 12px;border-radius:8px;margin:8px 0 3px 0;'>
        <span style='color:white;font-size:11px;font-weight:500;'>
        💬 인사말을 입력하면 각 설계사 메시지 맨 앞에 자동으로 추가됩니다.</span>
        </div>
        """, unsafe_allow_html=True)

        greeting_text = st.text_area(
            "인사말",
            placeholder="예: 안녕하세요! 이번 주도 파이팅입니다 💪",
            height=60,
            label_visibility="collapsed",
            key="manager_greeting"
        )

        filter_options = {
            "📋 전체": 0,
            "📅 현재주차 유실적자": 1,
        }

        col_filter, col_count = st.columns([3, 1])

        with col_filter:
            selected_filter_label = st.selectbox(
                "대상자 필터",
                list(filter_options.keys()),
                index=st.session_state.manager_filter_mode,
                label_visibility="collapsed",
                key="manager_filter_select"
            )

            st.session_state.manager_filter_mode = filter_options[selected_filter_label]

        filtered_agents = apply_manager_filter(
            all_agents,
            st.session_state.manager_filter_mode,
            current_week
        )

        with col_count:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#4a5568 0%,#2d3748 100%);
                padding:6px 10px;border-radius:8px;text-align:center;margin-top:2px;'>
            <span style='color:#ffd93d;font-weight:700;font-size:12px;'>{mgr_name}</span><br>
            <span style='color:white;font-size:12px;font-weight:600;'>{len(filtered_agents)}명</span>
            </div>
            """, unsafe_allow_html=True)

        if len(filtered_agents) == 0:
            st.markdown("""
            <div style='text-align:center;padding:16px;background:white;border-radius:10px;
                color:#718096;font-size:14px;'>해당 조건의 설계사가 없습니다.</div>
            """, unsafe_allow_html=True)

        else:
            for i, (_, agent_row) in enumerate(filtered_agents.iterrows()):
                agent_nm = str(agent_row.get(COLS["agent_name"], "")).strip()
                agent_branch = str(agent_row.get(COLS["branch_name"], "")).strip()
                agent_office = str(agent_row.get(COLS["office_name"], "")).strip()
                agent_code = str(agent_row.get(COLS["agent_code"], "")).strip()
                cumul_val = format_display(agent_row.get(COLS["current_cumulative"], 0))

                rank_emojis = ["🥇", "🥈", "🥉"]
                rank_label = rank_emojis[i] if i < 3 else f"#{i + 1}"

                st.markdown(f"""
                <div class='manager-card'>
                    <div class='manager-card-top'>
                        <div>
                            <div class='manager-name'>{rank_label} {agent_nm}</div>
                            <div class='manager-sub'>{agent_office} | {agent_branch} | {agent_code}</div>
                        </div>
                        <div class='manager-money'>{cumul_val}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"📅 {agent_nm} 주차별 실적 / 메시지 보기"):
                    st.markdown(f"### 📈 {current_month}월 누계: {cumul_val}")

                    for wi in range(1, 6):
                        if wi > current_week:
                            break

                        wc = get_week_col(wi)

                        if wc not in agent_row.index:
                            continue

                        wv = format_display(agent_row.get(wc, 0))

                        if wi == current_week:
                            st.markdown(f"""
                            <div class='weekly-row current'>
                            <div><strong>{wi}주차</strong> ⭐</div>
                            <strong style='color:#92400e;'>{wv}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class='weekly-row'>
                            <strong>{wi}주차</strong>
                            <strong style='color:#48bb78;'>{wv}</strong>
                            </div>
                            """, unsafe_allow_html=True)

                    raw_msg = build_kakao_message(
                        agent_row,
                        current_week,
                        greeting=greeting_text
                    )

                    st.text_area(
                        "메시지 미리보기",
                        value=raw_msg,
                        height=220,
                        key=f"mgr_msg_preview_{i}",
                        label_visibility="collapsed"
                    )

                    col_m1, col_m2 = st.columns([1, 1])

                    with col_m1:
                        copy_to_clipboard_button(
                            raw_msg,
                            button_label="📋 메시지 복사",
                            key=f"mgr_copy_{i}",
                            height=70
                        )

                    with col_m2:
                        st.download_button(
                            label="💾 저장",
                            data=raw_msg,
                            file_name=f"{agent_nm}_{agent_branch}_실적현황.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key=f"mgr_download_{i}"
                        )

        st.markdown("<hr style='border:1px solid #e2e8f0;margin:12px 0;'>", unsafe_allow_html=True)

        if st.button("🔄 초기화", use_container_width=True, key="reset_manager"):
            st.session_state.manager_search_performed = False
            st.session_state.manager_agent_list = pd.DataFrame()
            st.session_state.manager_name_display = ""
            st.session_state.manager_filter_mode = 0
            st.session_state.manager_duplicate_list = []
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
            ✨ 대상자를 펼쳐서 상세실적 확인, 메시지 복사 버튼으로 바로 발송하세요!</p>
        </div>
        """, unsafe_allow_html=True)
