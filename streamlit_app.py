import streamlit as st
import pandas as pd
import datetime
import pytz
import os
import tempfile
from PIL import Image
import gdown

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
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
* { font-family: 'Noto Sans KR', sans-serif; }

body { background-color: #1a1a1a; color: #ffffff; }

.info-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #ff8a99;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.cumulative-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #66d9ff;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.weekly-row {
    background: #2a2a2a;
    padding: 10px;
    border-radius: 8px;
    margin: 5px 0;
    border-left: 4px solid #999999;
}

.weekly-row.current {
    background: linear-gradient(135deg, #3a3a2a 0%, #2f2f1a 100%);
    border-left: 4px solid #ffff00;
    box-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
}

.target-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #ff8a99;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.bridge-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #ff8a99;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.mc-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #ff8a99;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.mc-plus-box {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    border-left: 4px solid #9d66ff;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

button {
    background: linear-gradient(135deg, #ff8a99 0%, #ff6b7a 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
    transition: all 0.3s ease;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(255, 138, 153, 0.4);
}

input {
    background-color: #2a2a2a;
    border: 1px solid #444444;
    color: #ffffff;
    padding: 10px;
    border-radius: 8px;
}

input::placeholder {
    color: #888888;
}

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
    background: #777777;
}
</style>
""", unsafe_allow_html=True)

def safe_float(v):
    if pd.isna(v) or v == "" or v is None:
        return 0.0
    try:
        return float(str(v).replace(",", "").strip())
    except:
        return 0.0

def format_display(v):
    v_str = str(v).strip()
    if v_str == "" or pd.isna(v):
        return "₩ 0"
    
    try:
        num = float(v_str.replace(",", ""))
        if num == int(num):
            return f"₩ {int(num):,}"
        else:
            return f"₩ {num:,.0f}"
    except:
        return v_str

def get_current_week():
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst).date()
    if today.month != 3:
        return 1
    day = today.day
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

def get_image_id_by_authentic_and_partner(is_auth, is_partner, agency):
    if is_auth:
        return LEAFLET_TEMPLATE_IDS.get("어센틱" if not is_partner else "none")
    agency_lower = str(agency).lower()
    for key, file_id in LEAFLET_TEMPLATE_IDS.items():
        if key.lower() in agency_lower:
            return file_id
    return LEAFLET_TEMPLATE_IDS["none"]

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

def render_mc_box(mc_challenge, mc_shortage, is_mc_plus=False):
    mc_challenge_display = format_display(mc_challenge)
    mc_shortage_display = format_display(mc_shortage)
    mc_shortage_val = safe_float(mc_shortage)

    mc_shortage_str = str(mc_shortage).strip()

    if "최종달성" in mc_shortage_str:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#66ff66"
    elif "전월 20만원 미달성" in mc_shortage_str or "다음기회에" in mc_shortage_str or "재도전" in mc_shortage_str or "대상아님" in mc_shortage_str:
        mc_display_status = "⚪ 대상아님"
        mc_shortage_color = "#999999"
    elif mc_shortage_val < 0 or mc_shortage_val == 0:
        mc_display_status = "✅ 시상금확보"
        mc_shortage_color = "#66ff66"
    else:
        mc_display_status = "🟡 도전중"
        mc_shortage_color = "#ffb366"

    box_class = "mc-plus-box" if is_mc_plus else "mc-box"
    status_color = "#9d66ff" if is_mc_plus else "#ffb366"

    st.markdown(f"""
    <div class='{box_class}'>
    <strong>도전구간:</strong> {mc_challenge_display}<br>
    <strong>부족금액:</strong> <span style='color: {mc_shortage_color}; font-weight: 700;'>{mc_shortage_display}</span><br>
    <strong>상태:</strong> <span style='color: {status_color}; font-weight: 700;'>{mc_display_status}</span>
    </div>
    """, unsafe_allow_html=True)

logo = load_logo()
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if logo:
        st.image(logo, width=100)
with col_title:
    st.title("📊 메리츠화재 설계사 성과 조회")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    manager_name = st.text_input("📌 매니저명", placeholder="예: 장혜정")
    agent_code = st.text_input("📌 설계사 코드", placeholder="예: 722019151")
    search_clicked = st.button("🔍 검색", use_container_width=True)

with col2:
    st.write("")
    st.write("")
    reset_clicked = st.button("🔄 초기화", use_container_width=True)

if reset_clicked:
    st.rerun()

df = load_data_from_google_sheets()

if df is None:
    st.error("데이터를 불러올 수 없습니다.")
elif search_clicked:
    if not manager_name or not agent_code:
        st.error("⚠️ 매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        filtered = df[
            (df["매니저"].astype(str).str.strip() == manager_name.strip()) &
            (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())
        ]

        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {manager_name} / {agent_code}")
        else:
            row = filtered.iloc[0]
            
            is_auth = safe_float(row.get("어센틱구분", 0)) == 1
            is_partner = "파트너채널" in str(row.get("지사명", "")).strip()
            
            agent_name = row.get("설계사명", "N/A")
            branch_name = row.get("지사명", "N/A")
            
            st.markdown(f"""
            <div class='info-box'>
            <strong>설계사명:</strong> {agent_name}<br>
            <strong>지사:</strong> {branch_name}
            </div>
            """, unsafe_allow_html=True)
            
            cumulative = format_display(row.get("누계실적", 0))
            st.markdown(f"""
            <div class='cumulative-box'>
            <strong>3월 누계 실적:</strong> {cumulative}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #66d9ff; font-size: 18px;'>📅 주별 성과</h3>", unsafe_allow_html=True)
            current_week = get_current_week()
            
            weeks = [
                ("1주차", "1주차"),
                ("2주차", "2주차"),
                ("3주차", "3주차"),
                ("4주차", "4주차"),
                ("5주차", "5주차"),
            ]
            
            for week_num, (col_name, label) in enumerate(weeks, start=1):
                week_value = format_display(row.get(col_name, 0))
                is_current = (week_num == current_week)
                css_class = "weekly-row current" if is_current else "weekly-row"
                marker = "⭐" if is_current else ""
                
                st.markdown(f"""
                <div class='{css_class}'>
                <strong>{marker} {label}:</strong> {week_value}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>⭐ 현재주차 목표</h3>", unsafe_allow_html=True)
            
            if is_auth and not is_partner:
                weekly_target = format_display(row.get("어센틱주차목표", 0))
                weekly_shortage = format_display(row.get("어센틱주차부족최종", 0))
            else:
                weekly_target = format_display(row.get("주차목표", 0))
                weekly_shortage = format_display(row.get("주차부족최종", 0))
            
            st.markdown(f"""
            <div class='target-box'>
            <strong>목표 →</strong> {weekly_target}<br>
            <strong>부족금액 →</strong> {weekly_shortage}
            </div>
            """, unsafe_allow_html=True)
            
            if not is_auth:
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
                bridge_target = format_display(row.get("브릿지 도전구간", 0))
                bridge_shortage = format_display(row.get("브릿지부족최종", 0))
                
                st.markdown(f"""
                <div class='bridge-box'>
                <strong>목표 →</strong> {bridge_target}<br>
                <strong>부족금액 →</strong> {bridge_shortage}
                </div>
                """, unsafe_allow_html=True)
            
            if is_auth:
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>💰 MC 성과</h3>", unsafe_allow_html=True)
                mc_challenge = row.get("MC도전구간", 0)
                mc_shortage = row.get("MC부족최종", 0)
                render_mc_box(mc_challenge, mc_shortage, is_mc_plus=False)
            
            st.markdown("<h3 style='color: #9d66ff; font-size: 18px;'>💰 MC PLUS +</h3>", unsafe_allow_html=True)
            mc_plus_challenge = row.get("MC+구간", 0)
            mc_plus_shortage = row.get("MC+부족최종", 0)
            render_mc_box(mc_plus_challenge, mc_plus_shortage, is_mc_plus=True)
            
            col_left, col_right = st.columns([1, 1])
            
            with col_right:
                image_id = get_image_id_by_authentic_and_partner(is_auth, is_partner, branch_name)
                leaflet_image = load_leaflet_template_from_drive(image_id)
                
                if leaflet_image:
                    st.image(leaflet_image, use_container_width=True)
                    
                    img_byte_arr = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    leaflet_image.save(img_byte_arr.name)
                    
                    with open(img_byte_arr.name, "rb") as f:
                        st.download_button(
                            label="📥 리플렛 다운로드",
                            data=f.read(),
                            file_name=f"{branch_name}_leaflet.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    
                    os.unlink(img_byte_arr.name)
else:
    st.info("💡 매니저명과 설계사 코드를 입력하고 검색 버튼을 클릭하세요.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888888; font-size: 12px;'>© 2024 Meritz Fire Insurance</div>", unsafe_allow_html=True)
