import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os
import streamlit.components.v1 as components
import re

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
    "더금융": "1DeUpP_czQzEpa2CTiWyvcg_42e0FT-_Y",
    "더좋은보험": "1OLsK7oilx3OacZSw8f1VZP3pKBvYsLRj",
    "프라임에셋": "1iZie57BZYUNguiiuympKd4wsg_kkZxVt",
    "에이플러스": "1KYkiPglCCgKZ59HGSebkpKjPanr-os1b",
    "지에이코리아": "1xsc5JVGxyercM0553s2Cdx5vw8PbjccS",
    "메타리치": "13MXbTMcaq0E9ugf9V4Yh1wGfNcavQSvX",
    "글로벌금융": "1rLX4jeoFvzgQCEEBaMLYWp5eSs_XdNNE",
    "인카금융": "15l_dvr73h5RwdrEEi2GP4lbVReMyj8KJ",
    "아너스": "1DrMIR4hDRcXuI3l6Ue-l4aCfP0aEP0JS",
    "굿리치": "1xF8N3LCMECplAurB9sVpmlzzmUdcHh2_",
    "신한금융": "1XAAncz-bWC4scblwtO7sLxsprqpcmu7_",
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "none": "19ZnaS2s4X8JKv27NW9FFuMUVh32i3hc0"
}

PASSWORD = "2233"

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

.agent-card {
    background: white;
    border-left: 4px solid #4a5568;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 8px 0;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    transition: all 0.2s ease;
}

.agent-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateX(3px);
}

.agent-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.agent-rank {
    background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
    color: white;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
    margin-right: 10px;
}

.agent-name-text {
    font-size: 15px;
    font-weight: 700;
    color: #2c3e50;
}

.agent-perf-text {
    font-size: 15px;
    font-weight: 700;
    color: #48bb78;
}

.agent-branch-text {
    font-size: 12px;
    color: #718096;
    margin-top: 2px;
}

.greeting-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 16px;
    border-radius: 10px;
    margin: 10px 0;
    box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);
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


# ============================================================
# 유틸 함수들
# ============================================================

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

def normalize_phone_number(phone):
    if pd.isna(phone):
        return ""
    return str(phone).replace("-", "").replace(" ", "").strip()

def extract_ga4_number(branch_str):
    """GA4-숫자지점 형식에서 숫자 추출, 없으면 9999 반환"""
    match = re.search(r'GA4-(\d+)', str(branch_str))
    if match:
        return int(match.group(1))
    return 9999

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
        if performance_df is None:
            return 0.0
        filtered = performance_df[performance_df["현재대리점설계사조직코드"].astype(str).str.strip() == str(agent_code).strip()]
        if len(filtered) > 0:
            return safe_float(filtered.iloc[0].get("누계실적", 0))
        return 0.0
    except:
        return 0.0

def create_vcard(name, phone, company):
    phone_clean = phone.replace("-", "").replace(" ", "")
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone_clean}
ORG:{company}
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

def render_mc_box(mc_challenge, mc_shortage, is_authentic=False, is_mc_plus=False, mc_target_value=1):
    if not is_mc_plus and (mc_target_value == 0 or mc_target_value == 2):
        st.markdown(f"""
        <div class='mc-box'>
        <strong>도전구간 →</strong> 대상아님<br>
        <strong>부족금액 →</strong> ₩ 0<br>
        <strong>상태 →</strong> <span style='color: #ed8936; font-weight: 700;'>이번달 20만원 도전</span>
        </div>
        """, unsafe_allow_html=True)
        return

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


# ============================================================
# 클립보드 복사 컴포넌트
# ============================================================
def copy_to_clipboard_button(text, button_label="📋 메시지 복사하기", key="clipboard_btn"):
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    components.html(
        f"""
        <button onclick="copyText()" style="
            font-family: 'Noto Sans KR', sans-serif;
            font-weight: 600;
            background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            color: white;
            cursor: pointer;
            width: 100%;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(74, 85, 104, 0.3);
        " id="copyBtn_{key}">
            {button_label}
        </button>
        <div id="copyMsg_{key}" style="
            display: none;
            margin-top: 8px;
            padding: 8px 12px;
            background: #c6f6d5;
            border-left: 4px solid #48bb78;
            border-radius: 6px;
            color: #276749;
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 13px;
            font-weight: 600;
        ">
            ✅ 복사 완료! 카카오톡에 붙여넣기 하세요.
        </div>
        <script>
        function copyText() {{
            const text = `{escaped_text}`;
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(function() {{
                    showSuccess();
                }}, function() {{
                    fallbackCopy(text);
                }});
            }} else {{
                fallbackCopy(text);
            }}
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
        function showSuccess() {{
            const msg = document.getElementById('copyMsg_{key}');
            msg.style.display = 'block';
            setTimeout(function() {{
                msg.style.display = 'none';
            }}, 3000);
        }}
        </script>
        """,
        height=90,
    )


# ============================================================
# 탭3 전용: 설계사 행으로부터 카카오톡 메시지 생성
# ============================================================
def build_kakao_message(row, df, current_week, greeting=""):
    agency_branch = str(row.get("지사명", "N/A")).strip()
    agent_name_display = str(row["설계사명"]).strip()
    cumulative = row["누계실적"]
    is_authentic = safe_float(row["어센틱구분"]) == 1

    week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
    week_text = ""
    for idx, week_col in enumerate(week_columns, 1):
        if idx > current_week:
            break
        week_value = row[week_col]
        current_mark = " ⭐" if idx == current_week else ""
        week_text += f" • {week_col}: {format_display(week_value)}{current_mark}\n"

    if is_authentic:
        weekly_target = row.get("어센틱주차목표", "0")
        weekly_shortage = row.get("어센틱주차부족", "0")
    else:
        weekly_target = row.get("주차목표", "0")
        weekly_shortage = row.get("주차부족최종", "0")

    if is_authentic:
        try:
            mc_target_value = safe_float(df.iloc[row.name, 27])
        except:
            mc_target_value = 1
        if mc_target_value == 0 or mc_target_value == 2:
            mc_info = """💰 MC 성과
 • 도전구간: 대상아님
 • 부족금액: ₩ 0
 • 상태: 이번달 20만원 도전"""
        else:
            mc_challenge = row.get("MC도전구간", 0)
            mc_shortage = row.get("MC부족최종", 0)
            mc_info = f"""💰 MC 성과
 • 도전구간: {format_display(mc_challenge)}
 • 부족금액: {format_display(mc_shortage)}"""
    else:
        bridge_target = row["브릿지 도전구간"]
        bridge_shortage = row["브릿지부족최종"]
        mc_info = f"""🌉 브릿지 성과
 • 목표: {format_display(bridge_target)}
 • 부족금액: {format_display(bridge_shortage)}"""

    mc_plus_challenge = row["MC+구간"]
    mc_plus_shortage = row["MC+부족최종"]

    greeting_line = f"{greeting}\n\n" if greeting.strip() else ""

    message = f"""{greeting_line}📊메리츠 3월 실적 현황
{agency_branch} {agent_name_display}팀장님!

📈 3월 누계 실적
 {format_display(cumulative)}

📅 주차별 실적
{week_text}
⭐ 현재주차 목표
 • 목표: {format_display(weekly_target)}
 • 부족금액: {format_display(weekly_shortage)}

{mc_info}

💰 MC PLUS+ 성과
 • 도전구간: {format_display(mc_plus_challenge)}
 • 부족금액: {format_display(mc_plus_shortage)}

💡 시상관련 궁금하신게 있다면 문의주세요~
이번주도 화이팅입니다!"""
    return message


# ============================================================
# 세션 상태 초기화
# ============================================================
defaults = {
    'authenticated': False,
    'search_performed': False,
    'selected_row': None,
    'show_duplicates': False,
    'filtered_data': None,
    'contact_search_performed': False,
    'contact_selected_row': None,
    'contact_show_duplicates': False,
    'contact_filtered_data': None,
    'manager_search_performed': False,
    'manager_agent_list': None,
    'manager_name_display': "",
    'manager_expanded_idx': None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ============================================================
# 로그인 화면
# ============================================================
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


# ============================================================
# 메인 화면 헤더
# ============================================================
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

tab1, tab2, tab3 = st.tabs(["📊 실적조회", "📞 전화번호 조회", "👔 매니저별 발송"])


# ============================================================
# 탭1: 실적조회
# ============================================================
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
        for idx, (row_idx, agent_row) in enumerate(st.session_state.filtered_data.iterrows()):
            office_branch = str(agent_row.get('지점명', 'N/A')).strip()
            agency_branch = str(agent_row.get('지사명', 'N/A')).strip()
            agent_display = f"{office_branch} | {agency_branch}"
            if st.button(agent_display, key=f"agent_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.selected_row = agent_row
                st.session_state.search_performed = True
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None
                st.rerun()

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

            if is_authentic:
                st.markdown("<h3 style='color: #4a5568;'>💰 MC 성과</h3>", unsafe_allow_html=True)
                mc_challenge = row.get("MC도전구간", 0)
                mc_shortage = row.get("MC부족최종", 0)
                try:
                    mc_target_value = safe_float(df.iloc[row.name, 27])
                except:
                    mc_target_value = 1
                render_mc_box(mc_challenge, mc_shortage, is_authentic=True, is_mc_plus=False, mc_target_value=mc_target_value)
            else:
                st.markdown("<h3 style='color: #4a5568;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
                bridge_target = row["브릿지 도전구간"]
                bridge_shortage = row["브릿지부족최종"]
                st.markdown(f"""
                <div class='bridge-box'>
                <strong>목표 →</strong> {format_display(bridge_target)}<br>
                <strong>부족금액 →</strong> {format_display(bridge_shortage)}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<h3 style='color: #805ad5;'>💰 MC PLUS+ 성과</h3>", unsafe_allow_html=True)
            mc_plus_challenge = row["MC+구간"]
            mc_plus_shortage = row["MC+부족최종"]
            render_mc_box(mc_plus_challenge, mc_plus_shortage, is_authentic=is_authentic, is_mc_plus=True)

            st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #4a5568;'>📱 카카오톡 발송</h3>", unsafe_allow_html=True)

            if is_authentic:
                try:
                    mc_target_value = safe_float(df.iloc[row.name, 27])
                except:
                    mc_target_value = 1
                if mc_target_value == 0 or mc_target_value == 2:
                    mc_info = """💰 MC 성과
 • 도전구간: 대상아님
 • 부족금액: ₩ 0
 • 상태: 이번달 20만원 도전"""
                else:
                    mc_challenge = row.get("MC도전구간", 0)
                    mc_shortage = row.get("MC부족최종", 0)
                    mc_info = f"""💰 MC 성과
 • 도전구간: {format_display(mc_challenge)}
 • 부족금액: {format_display(mc_shortage)}"""
            else:
                bridge_target = row["브릿지 도전구간"]
                bridge_shortage = row["브릿지부족최종"]
                mc_info = f"""🌉 브릿지 성과
 • 목표: {format_display(bridge_target)}
 • 부족금액: {format_display(bridge_shortage)}"""

            week_text = ""
            week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
            for idx, week_col in enumerate(week_columns, 1):
                if idx > current_week:
                    break
                week_value = row[week_col]
                current_mark = " ⭐" if idx == current_week else ""
                week_text += f" • {week_col}: {format_display(week_value)}{current_mark}\n"

            if is_authentic:
                weekly_target = row.get("어센틱주차목표", "0")
                weekly_shortage = row.get("어센틱주차부족", "0")
            else:
                weekly_target = row.get("주차목표", "0")
                weekly_shortage = row.get("주차부족최종", "0")

            kakao_message = f"""📊메리츠 3월 실적 현황
{agency_branch} {agent_name_display}팀장님!

📈 3월 누계 실적
 {format_display(cumulative)}

📅 주차별 실적
{week_text}
⭐ 현재주차 목표
 • 목표: {format_display(weekly_target)}
 • 부족금액: {format_display(weekly_shortage)}

{mc_info}

💰 MC PLUS+ 성과
 • 도전구간: {format_display(mc_plus_challenge)}
 • 부족금액: {format_display(mc_plus_shortage)}

💡 시상관련 궁금하신게 있다면 문의주세요~
이번주도 화이팅입니다!"""

            st.text_area("메시지 미리보기", value=kakao_message, height=350, label_visibility="collapsed", key="kakao_preview")

            col_copy1, col_copy2 = st.columns([1, 1])
            with col_copy1:
                copy_to_clipboard_button(kakao_message, button_label="📋 메시지 복사하기", key="kakao_copy_main")
            with col_copy2:
                st.download_button(
                    label="💾 텍스트 파일로 저장",
                    data=kakao_message,
                    file_name=f"{agent_name_display}_{agency_branch}_실적현황.txt",
                    mime="text/plain",
                    use_container_width=True
                )

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
            st.rerun()

    elif not st.session_state.show_duplicates:
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);'>
        <p style='color: #4a5568; font-weight: 600; font-size: 15px; margin-bottom: 8px;'>🔒 지점명과 설계사명을 입력하고 검색 버튼을 클릭하세요.</p>
        <p style='color: #718096; font-weight: 400; font-size: 13px; margin-top: 8px;'>개인정보 보호를 위해 검색 후에만 데이터가 표시됩니다.</p>
        </div>
        """, unsafe_allow_html=True)


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

    st.markdown("<h3 style='color: #4a5568; margin-top: 12px; margin-bottom: 12px; font-size: 16px;'>📞 전화번호 검색</h3>", unsafe_allow_html=True)

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
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        contact_search_clicked = st.button("🔍 검색", use_container_width=True, key="contact_search_btn")

    if contact_search_clicked:
        if not contact_search:
            st.warning("⚠️ 전화번호 또는 설계사명을 입력해주세요.")
            st.session_state.contact_search_performed = False
            st.session_state.contact_show_duplicates = False
        else:
            search_value = contact_search.strip()
            search_normalized = normalize_phone_number(search_value)
            if search_normalized.isdigit() and len(search_normalized) <= 8:
                search_normalized_with_010 = "010" + search_normalized
            else:
                search_normalized_with_010 = search_normalized

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
                # ✅ GA4-1 ~ GA4-13 숫자 순 정렬
                filtered_contacts = filtered_contacts.copy()
                filtered_contacts['_지점_sort'] = filtered_contacts['지점'].apply(extract_ga4_number)
                filtered_contacts = filtered_contacts.sort_values(by='_지점_sort', ascending=True).drop(columns=['_지점_sort']).reset_index(drop=True)
                st.session_state.contact_show_duplicates = True
                st.session_state.contact_filtered_data = filtered_contacts
                st.session_state.contact_search_performed = False

    if st.session_state.contact_show_duplicates and st.session_state.contact_filtered_data is not None:
        st.markdown("<p style='color:#4a5568;font-weight:600;margin-top:12px;font-size:14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>", unsafe_allow_html=True)
        for idx, (row_idx, contact_row) in enumerate(st.session_state.contact_filtered_data.iterrows()):
            contact_office = str(contact_row.get('지점', 'N/A')).strip()
            contact_branch = str(contact_row.get('지사', 'N/A')).strip()
            contact_name = str(contact_row.get('설계사명', 'N/A')).strip()
            contact_display = f"{contact_office} | {contact_branch} | {contact_name}"
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

        prev_month_raw = row.get("전월실적", 0)
        prev_prev_month_raw = row.get("전전월실적", 0)
        prev_month = format_display(prev_month_raw)
        prev_prev_month = format_display(prev_prev_month_raw)
        current_month_perf = get_current_month_performance(performance_df, code)
        current_month = format_display(current_month_perf)

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
        <strong>2월 실적:</strong> {prev_month}<br>
        <strong>3월 실적:</strong> {current_month}
        </div>
        """, unsafe_allow_html=True)

        vcard_name = f"{branch} {name}"
        vcard_content = create_vcard(vcard_name, phone, branch)
        st.download_button(
            label="📥 연락처 저장 (vCard)",
            data=vcard_content,
            file_name=f"{branch}_{name}_연락처.vcf",
            mime="text/vcard",
            use_container_width=True
        )

        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True, key="reset_contact"):
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
            st.rerun()

    elif not st.session_state.contact_show_duplicates:
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);'>
        <p style='color: #4a5568; font-weight: 600; font-size: 15px; margin-bottom: 8px;'>📞 전화번호 또는 설계사명을 입력하고 검색하세요.</p>
        <p style='color: #718096; font-weight: 400; font-size: 13px; margin-top: 8px;'>예: 01012345678, 1234567, 123-4567, 홍길동</p>
        <p style='color: #48bb78; font-weight: 500; font-size: 12px; margin-top: 12px;'>✨ 010 없이도 검색 가능합니다!</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 탭3: 매니저별 발송
# ============================================================
with tab3:
    df_main = load_data_from_google_sheets()
    if df_main is None:
        st.error("❌ 데이터를 불러올 수 없습니다.")
        st.stop()

    current_week = get_current_week()

    st.markdown("<h3 style='color: #4a5568; margin-top: 12px; margin-bottom: 12px; font-size: 16px;'>👔 매니저별 유실적자 조회 및 메시지 발송</h3>", unsafe_allow_html=True)

    # ── 매니저코드 검색 ──
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='search-label'>🔑 매니저코드 또는 매니저명 입력</div>", unsafe_allow_html=True)
        manager_search_input = st.text_input(
            "매니저검색",
            placeholder="예: M001, 김대길",
            label_visibility="collapsed",
            key="manager_search_input",
            autocomplete="off"
        )
    with col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        manager_search_clicked = st.button("🔍 조회", use_container_width=True, key="manager_search_btn")

    if manager_search_clicked:
        if not manager_search_input:
            st.warning("⚠️ 매니저코드 또는 매니저명을 입력해주세요.")
            st.session_state.manager_search_performed = False
        else:
            search_val = manager_search_input.strip()

            # 매니저코드 컬럼명 후보 (실제 시트에 맞게 자동 탐색)
            possible_code_cols = ["매니저코드", "담당매니저코드", "매니저_코드", "ManagerCode"]
            possible_name_cols = ["매니저명", "담당매니저", "매니저", "ManagerName"]

            manager_code_col = next((c for c in possible_code_cols if c in df_main.columns), None)
            manager_name_col = next((c for c in possible_name_cols if c in df_main.columns), None)

            mask = pd.Series([False] * len(df_main), index=df_main.index)
            if manager_code_col:
                mask = mask | (df_main[manager_code_col].astype(str).str.strip() == search_val)
            if manager_name_col:
                mask = mask | (df_main[manager_name_col].astype(str).str.strip().str.contains(search_val, na=False))

            # 컬럼을 못 찾은 경우 모든 컬럼에서 부분 일치 시도
            if not manager_code_col and not manager_name_col:
                for col in df_main.columns:
                    if "매니저" in col or "manager" in col.lower():
                        mask = mask | (df_main[col].astype(str).str.strip().str.contains(search_val, na=False))

            filtered_by_manager = df_main[mask].copy()

            # 유실적자만: 누계실적 > 0
            filtered_by_manager['_누계_float'] = filtered_by_manager['누계실적'].apply(safe_float)
            active_agents = filtered_by_manager[filtered_by_manager['_누계_float'] > 0].copy()
            active_agents = active_agents.sort_values(by='_누계_float', ascending=False).reset_index(drop=True)

            if len(active_agents) == 0:
                st.error(f"❌ '{search_val}'에 해당하는 유실적자를 찾을 수 없습니다.")
                st.session_state.manager_search_performed = False
            else:
                # 매니저명 표시
                if manager_name_col and manager_name_col in active_agents.columns:
                    mgr_name = str(active_agents.iloc[0][manager_name_col]).strip()
                elif manager_code_col and manager_code_col in active_agents.columns:
                    mgr_name = str(active_agents.iloc[0][manager_code_col]).strip()
                else:
                    mgr_name = search_val

                st.session_state.manager_search_performed = True
                st.session_state.manager_agent_list = active_agents
                st.session_state.manager_name_display = mgr_name
                st.session_state.manager_expanded_idx = None

    # ── 결과 표시 ──
    if st.session_state.manager_search_performed and st.session_state.manager_agent_list is not None:
        active_agents = st.session_state.manager_agent_list
        mgr_name = st.session_state.manager_name_display

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%); padding: 14px 18px; border-radius: 10px; margin: 12px 0; box-shadow: 0 2px 10px rgba(74,85,104,0.25);'>
        <span style='color: white; font-weight: 700; font-size: 16px;'>👔 {mgr_name} 매니저 &nbsp;|&nbsp; 유실적자 {len(active_agents)}명</span>
        </div>
        """, unsafe_allow_html=True)

        # ── 오늘의 인사말 입력 (고정) ──
        st.markdown("<h3 style='color: #4a5568;'>✍️ 오늘의 인사말 입력</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;'>
        <span style='color: white; font-size: 12px; font-weight: 500;'>💬 아래에 인사말을 입력하면 각 설계사 메시지 맨 앞에 자동으로 추가됩니다.</span>
        </div>
        """, unsafe_allow_html=True)

        greeting_text = st.text_area(
            "인사말",
            placeholder="예: 안녕하세요! 이번 주도 파이팅입니다 💪\n좋은 결과 있으시길 바랍니다!",
            height=100,
            label_visibility="collapsed",
            key="manager_greeting"
        )

        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 12px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#4a5568; font-weight:600; font-size:14px; margin-bottom:8px;'>📋 유실적자 리스트 (누계실적 높은 순)</p>", unsafe_allow_html=True)

        # ── 설계사 카드 목록 ──
        for i, (_, agent_row) in enumerate(active_agents.iterrows()):
            agent_nm = str(agent_row["설계사명"]).strip()
            agent_branch = str(agent_row.get("지사명", "")).strip()
            agent_office = str(agent_row.get("지점명", "")).strip()
            cumul_val = safe_float(agent_row["누계실적"])
            cumul_display = format_display(agent_row["누계실적"])

            # 순위 뱃지 색상
            if i == 0:
                rank_color = "linear-gradient(135deg, #f6d365 0%, #fda085 100%)"
            elif i == 1:
                rank_color = "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
            elif i == 2:
                rank_color = "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)"
            else:
                rank_color = "linear-gradient(135deg, #4a5568 0%, #2d3748 100%)"

            rank_text_color = "#92400e" if i == 0 else ("#1a365d" if i == 1 else ("#1c4532" if i == 2 else "white"))

            st.markdown(f"""
            <div style='background: white; border-left: 4px solid #4a5568; padding: 12px 16px; border-radius: 8px; margin: 6px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.08);'>
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <div style='display: flex; align-items: center; gap: 10px;'>
                        <div style='background: {rank_color}; color: {rank_text_color}; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; flex-shrink: 0;'>{i+1}</div>
                        <div>
                            <div style='font-size: 15px; font-weight: 700; color: #2c3e50;'>{agent_nm}</div>
                            <div style='font-size: 12px; color: #718096; margin-top: 2px;'>{agent_office} | {agent_branch}</div>
                        </div>
                    </div>
                    <div style='font-size: 15px; font-weight: 700; color: #48bb78;'>{cumul_display}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 메시지 복사 버튼 (각 설계사마다)
            msg = build_kakao_message(agent_row, df_main, current_week, greeting=greeting_text)
            copy_to_clipboard_button(
                msg,
                button_label=f"📋 {agent_nm} 메시지 복사",
                key=f"mgr_copy_{i}_{agent_nm}"
            )

            st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True, key="reset_manager"):
            st.session_state.manager_search_performed = False
            st.session_state.manager_agent_list = None
            st.session_state.manager_name_display = ""
            st.session_state.manager_expanded_idx = None
            st.rerun()

    elif not st.session_state.manager_search_performed:
        st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);'>
        <p style='color: #4a5568; font-weight: 600; font-size: 15px; margin-bottom: 8px;'>👔 매니저코드 또는 매니저명을 입력하고 조회하세요.</p>
        <p style='color: #718096; font-weight: 400; font-size: 13px; margin-top: 8px;'>조회된 유실적자를 고실적 순으로 확인하고 카카오톡 메시지를 바로 복사할 수 있습니다.</p>
        <p style='color: #48bb78; font-weight: 500; font-size: 12px; margin-top: 12px;'>✨ 인사말을 먼저 입력한 후 복사하면 인사말이 메시지에 자동 포함됩니다!</p>
        </div>
        """, unsafe_allow_html=True)
