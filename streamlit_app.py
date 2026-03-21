import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os

# ===== 설정 =====
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
    "none": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
}

# ===== 페이지 설정 =====
st.set_page_config(page_title="메리츠 설계사 성과 조회", layout="wide")

# ===== CSS 스타일 =====
st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: #ffffff;
}

.info-box {
    background: linear-gradient(135deg, #2d2d2d 0%, #1f1f1f 100%);
    border-left: 4px solid #0066cc;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 14px;
}

.cumulative-box {
    background: linear-gradient(135deg, #1a3a52 0%, #0f2233 100%);
    border-left: 4px solid #00ccff;
    padding: 20px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 18px;
    font-weight: bold;
}

.weekly-row {
    background: linear-gradient(135deg, #2d3a2d 0%, #1f261f 100%);
    border-left: 4px solid #66cc66;
    padding: 15px;
    border-radius: 8px;
    margin: 8px 0;
    font-size: 14px;
    display: flex;
    justify-content: space-between;
}

.weekly-row.current {
    background: linear-gradient(135deg, #3d5a3d 0%, #2f4a2f 100%);
    border-left: 4px solid #ffcc00;
    box-shadow: 0 0 10px rgba(255, 204, 0, 0.3);
}

.bridge-box {
    background: linear-gradient(135deg, #4a2d2d 0%, #331f1f 100%);
    border-left: 4px solid #ff6666;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 14px;
}

.mc-box {
    background: linear-gradient(135deg, #3d2d4a 0%, #2a1f33 100%);
    border-left: 4px solid #cc66ff;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 14px;
}

.target-box {
    background: linear-gradient(135deg, #4a4a2d 0%, #33331f 100%);
    border-left: 4px solid #ffcc66;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    font-size: 14px;
}

input, select {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #0066cc;
    border-radius: 4px;
    padding: 8px;
}

button {
    background-color: #0066cc;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    cursor: pointer;
    font-weight: bold;
}

button:hover {
    background-color: #0052a3;
}
</style>
""", unsafe_allow_html=True)

# ===== 유틸리티 함수 =====
def safe_float(value):
    """문자열을 float로 안전하게 변환"""
    if pd.isna(value):
        return 0.0
    try:
        if isinstance(value, str):
            return float(value.replace(",", ""))
        return float(value)
    except:
        return 0.0

def safe_get_value(row, column_name):
    """행에서 값을 안전하게 추출"""
    try:
        return row.get(column_name, "")
    except:
        return ""

def format_currency(value):
    """숫자를 한국 원화로 포맷"""
    value = safe_float(value)
    return f"₩{value:,.0f}"

def get_current_week():
    """현재 주차 계산 (1~5주)"""
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(kst).date()
    year, month, day = today.year, today.month, today.day
    
    if month == 3:
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
    return 1

def get_image_id_by_agency_name(agency_name):
    """대리점명으로 이미지 ID 매칭"""
    agency_name_lower = str(agency_name).strip().lower()
    for keyword, image_id in LEAFLET_TEMPLATE_IDS.items():
        if keyword.lower() in agency_name_lower:
            return image_id
    return LEAFLET_TEMPLATE_IDS.get("none")

# ===== 데이터 로딩 함수 =====
@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    """Google Sheets에서 데이터 로드"""
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 이미지 로드"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "template.jpg")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=True)
            if os.path.exists(output_path):
                return Image.open(output_path)
    except:
        pass
    return None

# ===== UI 메인 =====
st.title("📊 메리츠 설계사 성과 조회")

# 데이터 로드
df = load_data_from_google_sheets()
if df is None:
    st.error("데이터를 로드할 수 없습니다.")
    st.stop()

current_week = get_current_week()

# 입력 섹션
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    manager_name = st.text_input("매니저명", placeholder="예: 김대길")
with col2:
    agent_code = st.text_input("설계사 코드", placeholder="예: 724043483")
with col3:
    search_clicked = st.button("🔍 검색", use_container_width=True)

# 검색 로직
if search_clicked:
    if not manager_name or not agent_code:
        st.error("⚠️ 매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        # 데이터 필터링
        filtered = df[(df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {manager_name} / {agent_code}")
        else:
            row = filtered.iloc[0]
            
            # ===== 기본 정보 =====
            agent_name = safe_get_value(row, "설계사명")
            branch = safe_get_value(row, "지사명")
            agency_name = safe_get_value(row, "대리점")
            
            col_left, col_right = st.columns([1.5, 1])
            
            with col_left:
                st.markdown("### 📋 기본 정보")
                st.markdown(f"""
                <div class='info-box'>
                <strong>설계사명:</strong> {agent_name}<br>
                <strong>지사:</strong> {branch}<br>
                <strong>대리점:</strong> {agency_name}
                </div>
                """, unsafe_allow_html=True)
                
                # ===== 누계 실적 =====
                cumulative = safe_float(safe_get_value(row, "3월실적"))
                st.markdown("### 📈 3월 누계 실적")
                st.markdown(f"""
                <div class='cumulative-box'>
                {format_currency(cumulative)}
                </div>
                """, unsafe_allow_html=True)
                
                # ===== 주차별 실적 =====
                st.markdown("### 📅 주차별 실적")
                week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
                for idx, week_col in enumerate(week_columns, 1):
                    week_value = safe_float(safe_get_value(row, week_col))
                    is_current = (idx == current_week)
                    
                    if is_current:
                        st.markdown(f"""
                        <div class='weekly-row current'>
                        <strong>{week_col}</strong> <span style='color: #ffcc00;'>⭐</span> {format_currency(week_value)}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='weekly-row'>
                        <strong>{week_col}</strong> {format_currency(week_value)}
                        </div>
                        """, unsafe_allow_html=True)
                
                # ===== 주차 목표 =====
                weekly_target = safe_float(safe_get_value(row, "주차목표"))
                st.markdown("### 🎯 현재주차 목표")
                st.markdown(f"""
                <div class='target-box'>
                <strong>1주차 목표:</strong> {format_currency(weekly_target)}
                </div>
                """, unsafe_allow_html=True)
                
                # ===== 브릿지 성과 =====
                st.markdown("### 🌉 브릿지 성과")
                bridge_achievement = safe_float(safe_get_value(row, "브릿지 실적"))
                bridge_target = safe_float(safe_get_value(row, "브릿지 도전구간"))
                bridge_shortage = safe_float(safe_get_value(row, "브릿지 부족"))
                
                st.markdown(f"""
                <div class='bridge-box'>
                <strong>진척:</strong> {format_currency(bridge_achievement)}<br>
                <strong>목표:</strong> {format_currency(bridge_target)}<br>
                <strong>부족금액:</strong> {format_currency(bridge_shortage)}
                </div>
                """, unsafe_allow_html=True)
                
                # ===== MC+ 성과 =====
                st.markdown("### 💎 MC+ 성과")
                mc_challenge = safe_float(safe_get_value(row, "MC+구간"))
                mc_achievement = safe_float(safe_get_value(row, "3월실적"))  # L열 = 3월실적과 동일
                mc_shortage = safe_float(safe_get_value(row, "MC부족최종"))  # V열
                
                st.markdown(f"""
                <div class='mc-box'>
                <strong>도전구간:</strong> {format_currency(mc_challenge)}<br>
                <strong>실적:</strong> {format_currency(mc_achievement)}<br>
                <strong>부족금액:</strong> {format_currency(mc_shortage)}
                </div>
                """, unsafe_allow_html=True)
            
            with col_right:
                st.markdown("### 🎁 대리점 리플렛")
                image_id = get_image_id_by_agency_name(agency_name)
                image = load_leaflet_template_from_drive(image_id)
                
                if image:
                    st.image(image, use_container_width=True)
                    
                    # 다운로드 버튼
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
            
            # ===== 하단 버튼 =====
            col_print, col_reset = st.columns(2)
            with col_print:
                if st.button("🖨️ 인쇄", use_container_width=True):
                    st.info("브라우저의 인쇄 기능을 사용해주세요 (Ctrl+P 또는 Cmd+P)")
            with col_reset:
                if st.button("🔄 초기화", use_container_width=True):
                    st.rerun()

# 팁
st.caption("💡 매니저명과 설계사 코드를 입력하고 검색 버튼을 클릭하세요.")
