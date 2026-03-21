import streamlit as st
import pandas as pd
import datetime
import pytz
import os
import tempfile
from PIL import Image
import gdown

# ====== 설정 ======
GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

LEAFLET_TEMPLATE_IDS = {
    "메가": "16l4rB2dRYkmEARfP7shI_N5L_HKio9wO",
    "토스": "17b27Cq0sN52ifJ5NvCsnr87KbaUcsqsr",
    "지금융": "19lR3nBPV6guyEIAk9xw_6GwDPO1N_wbw",
    "삼성": "1A1fP2qR3sT4uV5wX6yZ7aB8cD9eF0gH1",
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
}

st.set_page_config(page_title="메리츠 실적현황", layout="wide")

# ====== CSS 스타일 ======
st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap' rel='stylesheet'>
<style>
* { font-family: 'Noto Sans KR', sans-serif !important; }
html, body { background: #0f0f0f; color: #e0e0e0; }
input { autocomplete: off !important; }
input:-webkit-autofill { 
    box-shadow: 0 0 0 1000px #1a1a1a inset !important;
    color: #e0e0e0 !important;
}
.info-box {
    background: #1a1a1a;
    border-left: 4px solid #00d4ff;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0;
    font-size: 14px;
}
.target-box {
    background: #1a1a1a;
    border: 1px solid #444;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0;
    text-align: center;
}
.bridge-box {
    background: #1a1a1a;
    border-left: 4px solid #ff9800;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0;
}
.mc-box {
    background: #1a1a1a;
    border-left: 4px solid #4caf50;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0;
}
.mc-plus-box {
    background: #1a1a1a;
    border-left: 4px solid #9c27b0;
    padding: 12px;
    border-radius: 4px;
    margin: 8px 0;
}
.week-row {
    background: #1a1a1a;
    border: 1px solid #333;
    padding: 10px;
    margin: 6px 0;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.week-row.current {
    background: #2a2a2a;
    border: 1px solid #00d4ff;
}
.achievement { color: #4caf50; font-weight: bold; }
.shortage { color: #ff6b6b; }
.status-good { color: #4caf50; }
.status-warning { color: #ff9800; }
.status-critical { color: #ff6b6b; }
</style>
""", unsafe_allow_html=True)

# ====== 헬퍼 함수 ======
def safe_float(value):
    try:
        return float(value) if pd.notna(value) and value != '' else 0
    except:
        return 0

def safe_get_value(row, col_name):
    try:
        val = row.get(col_name)
        return val if pd.notna(val) and val != '' else 0
    except:
        return 0

def format_currency(value):
    v = safe_float(value)
    return f"₩{int(v):,}" if v != 0 else "₩0"

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
        return LEAFLET_TEMPLATE_IDS.get("none") if is_partner_channel else LEAFLET_TEMPLATE_IDS.get("어센틱")
    agency_name_lower = str(agency_name).strip().lower()
    for keyword, image_id in LEAFLET_TEMPLATE_IDS.items():
        if keyword.lower() in agency_name_lower:
            return image_id
    return LEAFLET_TEMPLATE_IDS.get("none")

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
    return pd.read_csv(url)

def load_leaflet_template_from_drive(file_id):
    try:
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "template.jpg")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", out, quiet=True)
            if os.path.exists(out):
                return Image.open(out).copy()
    except:
        pass
    return None

def render_mc_box(title, challenge, shortage, status_col=None, is_critical=False):
    box_class = "mc-box" if "MC+" not in title else "mc-plus-box"
    status_class = "status-critical" if is_critical else ("status-warning" if shortage > 0 else "status-good")
    status_text = "🔴 부족" if shortage > 0 else "🟢 달성"
    
    st.markdown(f"""
    <div class='{box_class}'>
        <b>{title}</b><br>
        목표: {format_currency(challenge)} | 부족: <span class='shortage'>{format_currency(shortage)}</span><br>
        <span class='{status_class}'>{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ====== 메인 UI ======
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("# 📊")
with col_title:
    st.markdown("# 메리츠 실적현황")

st.divider()

col_search1, col_search2, col_search_btn = st.columns([2, 2, 1])

with col_search1:
    manager_name = st.text_input("📌 매니저명", key="manager", placeholder="매니저 이름 입력")

with col_search2:
    agent_code = st.text_input("📌 설계사코드", key="agent_code", placeholder="설계사 코드 입력")

with col_search_btn:
    search_btn = st.button("🔍 검색", use_container_width=True, key="search_btn")

st.divider()

# ====== 검색 로직 ======
if search_btn:
    if not manager_name or not agent_code:
        st.warning("⚠️ 매니저명과 설계사코드를 모두 입력해주세요.")
    else:
        df = load_data_from_google_sheets()
        
        # 검색 필터링
        filtered = df[(df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())]
        
        if filtered.empty:
            st.error(f"❌ 검색 결과가 없습니다. (매니저: {manager_name}, 설계사코드: {agent_code})")
        else:
            row = filtered.iloc[0]
            
            # 기본 정보
            agent_name = safe_get_value(row, "설계사명")
            branch = safe_get_value(row, "지사명")
            agency = safe_get_value(row, "대리점")
            
            # 어센틱 구분 확인
            is_authentic = safe_float(safe_get_value(row, "어센틱구분")) == 1
            is_partner_channel = "파트너채널" in str(branch)
            
            st.markdown(f"""
            <div class='info-box'>
                <b>설계사:</b> {agent_name} | <b>지사:</b> {branch} | <b>대리점:</b> {agency}
            </div>
            """, unsafe_allow_html=True)
            
            # 3월 누계 실적
            march_cum = safe_float(safe_get_value(row, "3월실적"))
            st.markdown(f"""
            <div class='info-box'>
                <b>3월 누계 실적:</b> {format_currency(march_cum)}
            </div>
            """, unsafe_allow_html=True)
            
            # 주차별 실적
            current_week = get_current_week()
            week_cols = ["1주차", "2주차", "3주차", "4주차", "5주차"]
            
            st.markdown("### 📅 주차별 실적")
            for i, col_name in enumerate(week_cols, 1):
                week_val = safe_float(safe_get_value(row, col_name))
                is_current = i == current_week
                css_class = "week-row current" if is_current else "week-row"
                emphasis = "**" if is_current else ""
                st.markdown(f"""
                <div class='{css_class}'>
                    {emphasis}{'⭐ ' if is_current else ''}{i}주차: {format_currency(week_val)}{emphasis}
                </div>
                """, unsafe_allow_html=True)
            
            # 현재 주차 목표
            st.markdown("### 🎯 현재주차 목표")
            if is_authentic:
                week_target = safe_float(safe_get_value(row, "어센틱주차목표"))
                week_shortage = safe_float(safe_get_value(row, "어센틱주차부족최종"))
            else:
                week_target = safe_float(safe_get_value(row, "주차목표"))
                week_shortage = safe_float(safe_get_value(row, "주차부족"))
            
            st.markdown(f"""
            <div class='target-box'>
                <b>목표:</b> {format_currency(week_target)}<br>
                <b class='shortage'>부족:</b> {format_currency(week_shortage)}
            </div>
            """, unsafe_allow_html=True)
            
            # 브릿지 (어센틱이 아닌 경우만 표시)
            if not is_authentic:
                st.markdown("### 🌉 브릿지 성과")
                bridge_challenge = safe_float(safe_get_value(row, "브릿지 도전구간"))
                bridge_shortage = safe_float(safe_get_value(row, "브릿지 부족"))
                st.markdown(f"""
                <div class='bridge-box'>
                    <b>목표:</b> {format_currency(bridge_challenge)}<br>
                    <b class='shortage'>부족:</b> {format_currency(bridge_shortage)}
                </div>
                """, unsafe_allow_html=True)
            
            # MC / MC+ 성과
            st.markdown("### 💰 성과")
            
            if is_authentic and not is_partner_channel:
                # 어센틱: MC + MC+
                mc_challenge = safe_float(safe_get_value(row, "MC도전구간"))
                mc_shortage = safe_float(safe_get_value(row, "MC부족최종"))
                render_mc_box("MC", mc_challenge, mc_shortage)
                
                mc_plus_challenge = safe_float(safe_get_value(row, "MC+구간"))
                mc_plus_shortage = safe_float(safe_get_value(row, "MC+부족최종"))
                render_mc_box("MC+", mc_plus_challenge, mc_plus_shortage)
            else:
                # 기타 또는 파트너채널: MC+ 만
                mc_plus_challenge = safe_float(safe_get_value(row, "MC+구간"))
                mc_plus_shortage = safe_float(safe_get_value(row, "MC+부족최종"))
                render_mc_box("MC+", mc_plus_challenge, mc_plus_shortage)
            
            # 리플렛 이미지
            st.markdown("---")
            st.markdown("### 📋 안내장")
            
            image_id = get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel, agency)
            image = load_leaflet_template_from_drive(image_id)
            
            if image:
                st.image(image, use_container_width=True)
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    image.save(tmp.name, "JPEG")
                    with open(tmp.name, "rb") as f:
                        st.download_button(
                            "📥 안내장 다운로드",
                            f,
                            f"{branch}_안내장.jpg",
                            "image/jpeg",
                            use_container_width=True
                        )
            else:
                st.info("ℹ️ 안내장 이미지를 찾을 수 없습니다.")
            
            # 초기화 버튼
            if st.button("🔄 초기화", use_container_width=True):
                st.rerun()
else:
    st.markdown("""
    <div style='text-align:center;padding:50px;color:#999999;'>
        <h2>🔒 프라이버시 보호</h2>
        좌상단에서 <b>매니저명</b>과 <b>설계사코드</b>를 입력한 후 <b>검색</b> 버튼을 클릭하세요.
    </div>
    """, unsafe_allow_html=True)
