import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os

GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

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
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
}

st.set_page_config(page_title="메리츠 실적현황", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">

<style>
* {
    font-family: 'Noto Sans KR', sans-serif !important;
}

html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stDecoration"] {
    background: #0f0f0f !important;
    color: #e0e0e0;
}

[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0.3) !important;
}

h1, h2, h3 {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
}

input::-webkit-autofill,
input::-webkit-autofill:hover,
input::-webkit-autofill:focus,
input::-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #1a1a1a inset !important;
    box-shadow: 0 0 0 30px #1a1a1a inset !important;
}

input::-webkit-autofill {
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    background: linear-gradient(135deg, #c41e3a 0%, #a01729 100%);
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(196, 30, 58, 0.4);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #a01729 0%, #7d111f 100%);
    box-shadow: 0 6px 20px rgba(196, 30, 58, 0.6);
    transform: translateY(-2px);
}

.info-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #c41e3a;
    padding: 18px;
    border-radius: 10px;
    margin: 12px 0;
    font-size: 17px;
    line-height: 2;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    font-weight: 500;
}

.cumulative-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #ff6b7a;
    padding: 25px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 26px;
    font-weight: 700;
    color: #ff8a99;
    text-align: center;
    box-shadow: 0 4px 20px rgba(196, 30, 58, 0.3);
    letter-spacing: 1px;
}

.weekly-row {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #66cc66;
    padding: 16px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.4);
    font-weight: 600;
}

.weekly-row.current {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #ffcc00;
    box-shadow: 0 0 15px rgba(255, 204, 0, 0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 15px rgba(255, 204, 0, 0.3); }
    50% { box-shadow: 0 0 25px rgba(255, 204, 0, 0.5); }
}

.bridge-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #ff8a99;
    padding: 18px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 17px;
    line-height: 2.2;
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.2);
    font-weight: 600;
}

.mc-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #ff6b7a;
    padding: 18px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 17px;
    line-height: 2.2;
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.2);
    font-weight: 600;
    color: #ffffff;
}

.mc-plus-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #9d66ff;
    padding: 18px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 17px;
    line-height: 2.2;
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.2);
    font-weight: 600;
    color: #ffffff;
}

.target-box {
    background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%);
    border-left: 5px solid #ffb366;
    padding: 18px;
    border-radius: 10px;
    margin: 15px 0;
    font-size: 17px;
    line-height: 2.2;
    box-shadow: 0 4px 12px rgba(196, 30, 58, 0.15);
    font-weight: 600;
}

input, select {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 2px solid #c41e3a !important;
    border-radius: 8px !important;
    padding: 12px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.3s ease;
}

input:focus, select:focus {
    border-color: #ff6b7a !important;
    box-shadow: 0 0 10px rgba(255, 107, 122, 0.3) !important;
}

input::placeholder {
    color: #666666 !important;
}

.stTextInput > label, .stSelectbox > label {
    font-weight: 600;
    color: #ffffff;
    font-family: 'Noto Sans KR', sans-serif;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0f0f0f;
}

::-webkit-scrollbar-thumb {
    background: #c41e3a;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ff6b7a;
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
        return float(v.replace(",", ""))
    except:
        return 0.0

def format_display(value):
    v = str(value).strip()
    if v == "" or v == "nan":
        return "₩ 0"
    try:
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
    return 1

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
        mc_shortage_color = "#66ff66"
    elif "다음기회에" in shortage_str or "재도전" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#999999"
    elif "대상아님" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#999999"
    elif "미달성" in shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#999999"
    elif is_authentic and not is_mc_plus and "전월" in str(mc_challenge):
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#999999"
    elif mc_shortage_val < 0:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#66ff66"
    elif mc_shortage_val == 0:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#66ff66"
    else:
        mc_display_status = "🟡 도전중"
        mc_shortage_color = "#ffb366"
    
    box_class = "mc-plus-box" if is_mc_plus else "mc-box"
    status_color = "#9d66ff" if is_mc_plus else "#ffb366"
    
    st.markdown(f"""
    <div class='{box_class}'>
    <strong>도전구간 →</strong> {mc_challenge_display}<br>
    <strong>부족금액 →</strong> <span style='color: {mc_shortage_color}; font-weight: 700;'>{mc_shortage_display}</span><br>
    <strong>상태 →</strong> <span style='color: {status_color}; font-weight: 700;'>{mc_display_status}</span>
    </div>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None

col_logo, col_title = st.columns([1, 4])
with col_logo:
    logo = load_logo()
    if logo:
        st.image(logo, width=80)
    else:
        st.write("📊")

with col_title:
    st.markdown("<h1 style='color: #ffffff; font-size: 28px; margin-top: 10px;'>메리츠 설계사 성과 조회</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #c41e3a;'>", unsafe_allow_html=True)

df = load_data_from_google_sheets()
if df is None:
    st.stop()

current_week = get_current_week()

st.markdown("<h3 style='color: #ffffff; margin-top: 20px; font-size: 18px;'>🔍 검색 정보 입력</h3>", unsafe_allow_html=True)

# 지점명 드롭다운 추가 (GA4-2지점 기본값)
branches = sorted(df['지사명'].unique())
default_idx = branches.index("GA4-2지점") if "GA4-2지점" in branches else 0

col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1])
with col1:
    selected_branch = st.selectbox("1️⃣ 지점명", branches, index=default_idx, label_visibility="collapsed", key="branch")

with col2:
    manager_name = st.text_input("2️⃣ 매니저명", placeholder="예: 박메리", label_visibility="collapsed", key="manager", autocomplete="off")

with col3:
    agent_name = st.text_input("3️⃣ 설계사명", placeholder="예: 홍길동", label_visibility="collapsed", key="agent", autocomplete="off")

with col4:
    search_clicked = st.button("🔍 검색", use_container_width=True)

# 검색 로직
if search_clicked:
    if not manager_name or not agent_name:
        st.error("⚠️ 매니저명과 설계사명을 모두 입력해주세요.")
        st.session_state.search_performed = False
    else:
        filtered = df[(df["지사명"].astype(str).str.strip() == selected_branch.strip()) &
                      (df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["설계사명"].astype(str).str.strip() == agent_name.strip())]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다")
            st.session_state.search_performed = False
        elif len(filtered) == 1:
            st.session_state.search_performed = True
            st.session_state.selected_row = filtered.iloc[0]
        else:
            st.markdown("<p style='color:#fff;font-weight:600;margin-top:20px;font-size:14px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
            for idx, (_, agent_row) in enumerate(filtered.iterrows()):
                agent_display = f"{agent_row.get('지사명','N/A')} - {agent_row.get('설계사명','N/A')} ({agent_row.get('현재대리점설계사조직코드','N/A')})"
                if st.button(agent_display, key=f"agent_{idx}", use_container_width=True):
                    st.session_state.search_performed = True
                    st.session_state.selected_row = agent_row
                    st.rerun()

# 결과 표시
if st.session_state.search_performed and st.session_state.selected_row is not None:
    row = st.session_state.selected_row
    
    agent_name = str(row["설계사명"]).strip()
    branch = str(row["지사명"]).strip()
    agency_name = str(row["대리점"]).strip()
    
    is_authentic = safe_float(row["어센틱구분"]) == 1
    is_partner_channel = "파트너채널" in branch
    
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown("""
        <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-radius: 10px; border-left: 5px solid #ffb366; margin-bottom: 20px;'>
        <p style='color: #ffb366; font-weight: 600; font-size: 15px; margin: 0;'>💡 대리점 시상안을 보고 달성 시상금을 확인하세요</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📋 기본 정보</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='info-box'>
        <strong>설계사명:</strong> {agent_name}<br>
        <strong>지사:</strong> {branch}
        </div>
        """, unsafe_allow_html=True)
        
        cumulative = row["누계실적"]
        st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📈 3월 누계 실적</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='cumulative-box'>
        {format_display(cumulative)}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📅 주차별 실적</h3>", unsafe_allow_html=True)
        
        week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
        for idx, week_col in enumerate(week_columns, 1):
            week_value = row[week_col]
            is_current = (idx == current_week)
            
            if is_current:
                st.markdown(f"""
                <div class='weekly-row current'>
                <strong>{week_col}</strong> <span style='color: #ffcc00; font-size: 20px;'>⭐</span> <strong style='color: #ffcc00;'>{format_display(week_value)}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='weekly-row'>
                <strong>{week_col}</strong> <strong style='color: #66cc66;'>{format_display(week_value)}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>⭐ 현재주차 목표</h3>", unsafe_allow_html=True)
        
        if is_authentic:
            weekly_target = row["어센틱주차목표"]
            weekly_shortage = row["어센틱주차부족최종"]
        else:
            weekly_target = row["주차목표"]
            weekly_shortage = row["주차부족최종"]
        
        st.markdown(f"""
        <div class='target-box'>
        <strong>목표 →</strong> {format_display(weekly_target)}<br>
        <strong>부족금액 →</strong> {format_display(weekly_shortage)}
        </div>
        """, unsafe_allow_html=True)
        
        if not is_authentic:
            st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
            bridge_target = row["브릿지 도전구간"]
            bridge_shortage = row["브릿지부족최종"]
            
            st.markdown(f"""
            <div class='bridge-box'>
            <strong>목표 →</strong> {format_display(bridge_target)}<br>
            <strong>부족금액 →</strong> {format_display(bridge_shortage)}
            </div>
            """, unsafe_allow_html=True)
        
        if is_authentic:
            st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>💰 MC 성과</h3>", unsafe_allow_html=True)
            mc_challenge = row["MC도전구간"]
            mc_shortage = row["MC부족최종"]
            render_mc_box(mc_challenge, mc_shortage, is_authentic=True, is_mc_plus=False)
        
        st.markdown("<h3 style='color: #9d66ff; font-size: 18px;'>💰 MC PLUS+ 성과</h3>", unsafe_allow_html=True)
        mc_plus_challenge = row["MC+구간"]
        mc_plus_shortage = row["MC+부족최종"]
        render_mc_box(mc_plus_challenge, mc_plus_shortage, is_authentic=is_authentic, is_mc_plus=True)
    
    with col_right:
        st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🎁 대리점 리플렛</h3>", unsafe_allow_html=True)
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
    
    st.markdown("<hr style='border: 1px solid #c41e3a; margin: 30px 0;'>", unsafe_allow_html=True)
    
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.search_performed = False
        st.session_state.selected_row = None
        st.rerun()

else:
    st.markdown("""
    <div style='text-align: center; margin-top: 60px; padding: 40px; background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-radius: 10px; border-left: 5px solid #c41e3a;'>
    <p style='color: #ff8a99; font-weight: 600; font-size: 16px;'>🔒 매니저명과 설계사명을 입력하고 검색 버튼을 클릭하세요.</p>
    <p style='color: #888888; font-weight: 400; font-size: 14px; margin-top: 10px;'>개인정보 보호를 위해 검색 후에만 데이터가 표시됩니다.</p>
    </div>
    """, unsafe_allow_html=True)
