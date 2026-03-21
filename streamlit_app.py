import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os

# ============================================
# 설정
# ============================================
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

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title="메리츠 실적현황",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS 스타일링 (메리츠 빨강색 테마 + 검은 배경)
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

* {
    font-family: 'Noto Sans KR', sans-serif !important;
}

body {
    background-color: #0f0f0f;
    color: #ffffff;
}

/* 메인 제목 */
.main-title {
    font-size: 40px;
    font-weight: 700;
    color: #ffffff;
    text-align: center;
    margin-bottom: 20px;
    margin-top: 10px;
}

/* 기본정보 박스 */
.info-box {
    background-color: #1a1a1a;
    border-left: 4px solid #c41e3a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 17px;
    line-height: 2;
}

/* 누계 박스 */
.cumulative-box {
    background-color: #1a1a1a;
    border-left: 4px solid #c41e3a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 26px;
    font-weight: 700;
    color: #ff6b7a;
    text-align: center;
}

/* 주차 진척 행 */
.weekly-row {
    background-color: #131313;
    border: 1px solid #2a2a2a;
    padding: 12px;
    margin-bottom: 10px;
    border-radius: 6px;
    font-size: 18px;
    line-height: 1.8;
}

.weekly-row.current {
    background-color: #2a2a2a;
    border: 2px solid #c41e3a;
    font-weight: 600;
}

/* 브릿지 박스 */
.bridge-box {
    background-color: #1a1a1a;
    border-left: 4px solid #ff6b7a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 17px;
    line-height: 2.2;
}

/* MC+ 박스 */
.mc-box {
    background-color: #1a1a1a;
    border-left: 4px solid #ff6b7a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 17px;
    line-height: 2.2;
}

/* 현재주차 목표 박스 */
.target-box {
    background-color: #1a1a1a;
    border-left: 4px solid #ff6b7a;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    font-size: 17px;
    line-height: 2.2;
}

/* 입력 필드 */
input, select, textarea {
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 6px !important;
    padding: 10px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

input::placeholder {
    color: #888888 !important;
}

/* 버튼 */
button {
    background-color: #c41e3a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    transition: all 0.3s ease !important;
}

button:hover {
    background-color: #a01830 !important;
}

/* 스크롤바 */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: #c41e3a;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a01830;
}

/* 텍스트 선택 */
::selection {
    background-color: #c41e3a;
    color: #ffffff;
}

/* 상태 색상 */
.status-achievement {
    color: #66ff66;
    font-weight: 700;
}

.status-challenge {
    color: #ffa500;
    font-weight: 700;
}

.status-inactive {
    color: #999999;
    font-weight: 700;
}

.status-shortage {
    color: #ff6b6b;
    font-weight: 700;
}

/* 캡션 */
.caption {
    color: #888888;
    font-size: 14px;
    text-align: center;
    margin-top: 20px;
}

/* 오류 메시지 */
.error-message {
    color: #ff6b6b;
    padding: 15px;
    background-color: #2a1a1a;
    border-left: 4px solid #ff6b6b;
    border-radius: 6px;
    margin-bottom: 15px;
}

/* 안내 메시지 */
.info-message {
    color: #888888;
    padding: 15px;
    background-color: #1a1a1a;
    border-left: 4px solid #c41e3a;
    border-radius: 6px;
    margin-bottom: 15px;
    text-align: center;
}

/* 자동완성 제거 */
input:-webkit-autofill {
    -webkit-box-shadow: 0 0 0 1000px #2a2a2a inset !important;
    -webkit-text-fill-color: #ffffff !important;
}

input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0 1000px #2a2a2a inset !important;
    -webkit-text-fill-color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# 유틸리티 함수
# ============================================

def safe_float(value):
    """안전한 float 변환"""
    if value is None or value == "":
        return 0.0
    try:
        return float(str(value).replace(",", ""))
    except:
        return 0.0

def safe_get_value(row, column_name):
    """안전한 행 값 조회"""
    try:
        val = row.get(column_name, "")
        if pd.isna(val):
            return ""
        return str(val).strip()
    except:
        return ""

def format_currency(value):
    """숫자를 통화 형식으로 변환"""
    try:
        num = safe_float(value)
        if num == 0:
            return "0"
        return f"{int(num):,}"
    except:
        return str(value)

def get_current_week():
    """현재 주차 계산 (3월 기준)"""
    today = datetime.now(pytz.timezone('Asia/Seoul'))
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

def get_image_id_by_agency_name(agency_name):
    """대리점명으로 리플렛 이미지 ID 조회"""
    if not agency_name:
        return LEAFLET_TEMPLATE_IDS.get("none", "")
    
    agency_lower = agency_name.lower()
    for key, image_id in LEAFLET_TEMPLATE_IDS.items():
        if key != "none" and key.lower() in agency_lower:
            return image_id
    return LEAFLET_TEMPLATE_IDS.get("none", "")

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    """Google Sheets에서 데이터 로드"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {str(e)}")
        return None

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 리플렛 이미지 다운로드"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "leaflet.pdf")
            download_url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(download_url, temp_file, quiet=True)
            if os.path.exists(temp_file):
                with open(temp_file, "rb") as f:
                    return f.read()
    except:
        pass
    return None

def load_logo():
    """로고 이미지 로드"""
    try:
        if os.path.exists("meritz.png"):
            return Image.open("meritz.png")
    except:
        pass
    return None

# ============================================
# UI - 로고와 제목
# ============================================
logo = load_logo()
col1, col2 = st.columns([1, 4])
with col1:
    if logo:
        st.image(logo, width=80)
    else:
        st.markdown("🏢", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-title">메리츠 실적현황</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# 데이터 로드
# ============================================
df = load_data_from_google_sheets()

if df is None:
    st.error("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")
    st.stop()

# ============================================
# 검색 섹션
# ============================================
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    manager_name = st.text_input("매니저명", placeholder="예: 박메리", autocomplete="off")

with col2:
    agent_code = st.text_input("설계사코드 (7로 시작)", placeholder="예: 7XXXXXX", autocomplete="off")

with col3:
    search_clicked = st.button("조회", use_container_width=True)

# ============================================
# 검색 결과 표시
# ============================================
if search_clicked:
    if not manager_name or not agent_code:
        st.markdown('<div class="error-message">⚠️ 매니저명과 설계사코드를 모두 입력해주세요.</div>', unsafe_allow_html=True)
    else:
        # 데이터 필터링
        filtered_df = df[
            (df['매니저'].astype(str).str.strip() == manager_name.strip()) &
            (df['현재대리점설계사조직코드'].astype(str).str.strip() == agent_code.strip())
        ]

        if filtered_df.empty:
            st.markdown('<div class="error-message">❌ 검색 결과가 없습니다. 매니저명과 설계사코드를 확인해주세요.</div>', unsafe_allow_html=True)
        else:
            row = filtered_df.iloc[0]

            # 기본정보
            agent_name = safe_get_value(row, "설계사명")
            branch_name = safe_get_value(row, "지사명")

            st.markdown(f"""
            <div class="info-box">
            <strong>설계사명:</strong> {agent_name}<br>
            <strong>지사:</strong> {branch_name}
            </div>
            """, unsafe_allow_html=True)

            # 3월 누계 실적
            march_total = safe_get_value(row, "3월실적")
            st.markdown(f"""
            <div class="cumulative-box">
            3월 누계 실적<br>
            {format_currency(march_total)}
            </div>
            """, unsafe_allow_html=True)

            # 주차 진척 (1~5주차)
            st.markdown("<h3 style='font-size: 22px; margin-top: 20px; margin-bottom: 15px;'>📊 주차 진척</h3>", unsafe_allow_html=True)
            current_week = get_current_week()
            
            for week in range(1, 6):
                week_col = f"{week}주차"
                week_value = safe_get_value(row, week_col)
                is_current = week == current_week
                current_class = "current" if is_current else ""
                current_badge = "🟡 현재주차" if is_current else ""
                
                st.markdown(f"""
                <div class="weekly-row {current_class}">
                {week}주차: <strong>{format_currency(week_value)}</strong> {current_badge}
                </div>
                """, unsafe_allow_html=True)

            # 현재주차 목표 및 부족금액
            st.markdown("<h3 style='font-size: 22px; margin-top: 20px; margin-bottom: 15px;'>🎯 현재주차 목표</h3>", unsafe_allow_html=True)
            weekly_target = safe_get_value(row, "주차목표")
            weekly_shortage = safe_get_value(row, "주차부족")
            
            st.markdown(f"""
            <div class="target-box">
            <strong>목표:</strong> {format_currency(weekly_target)}<br>
            <strong>부족금액:</strong> <span class="status-shortage">{format_currency(weekly_shortage)}</span>
            </div>
            """, unsafe_allow_html=True)

            # 브릿지 진척
            st.markdown("<h3 style='font-size: 22px; margin-top: 20px; margin-bottom: 15px;'>🌉 브릿지 진척</h3>", unsafe_allow_html=True)
            bridge_actual = safe_get_value(row, "브릿지 실적")
            bridge_target = safe_get_value(row, "브릿지 도전구간")
            bridge_shortage = safe_get_value(row, "브릿지 부족")
            
            st.markdown(f"""
            <div class="bridge-box">
            <strong>실적:</strong> {format_currency(bridge_actual)}<br>
            <strong>도전구간:</strong> {format_currency(bridge_target)}<br>
            <strong>부족금액:</strong> <span class="status-shortage">{format_currency(bridge_shortage)}</span>
            </div>
            """, unsafe_allow_html=True)

            # MC+ 성과
            st.markdown("<h3 style='font-size: 22px; margin-top: 20px; margin-bottom: 15px;'>⭐ MC+ 성과</h3>", unsafe_allow_html=True)
            
            mc_challenge = safe_get_value(row, "MC+구간")  # T열
            mc_shortage_amount = safe_get_value(row, "MC부족")  # U열
            mc_status = safe_get_value(row, "MC부족최종")  # V열

            # MC+ 상태 로직
            if mc_status and mc_status.strip():
                # V열 값이 있는 경우
                if "최종달성" in mc_status:
                    mc_display_status = "✅ 시상금확보"
                    mc_display_shortage = mc_status
                    mc_shortage_color = "#66ff66"
                elif "다음기회에" in mc_status or "재도전" in mc_status:
                    mc_display_status = "⚪ 대상아님"
                    mc_display_shortage = mc_status
                    mc_shortage_color = "#999999"
                elif "대상아님" in mc_status:
                    mc_display_status = "⚪ 대상아님"
                    mc_display_shortage = mc_status
                    mc_shortage_color = "#999999"
                else:
                    mc_display_status = "🟡 도전중"
                    mc_display_shortage = format_currency(mc_shortage_amount) if mc_shortage_amount else "-"
                    mc_shortage_color = "#ff6b6b"
            else:
                # V열이 비어있으면 U열(MC부족) 참고
                mc_shortage_float = safe_float(mc_shortage_amount)
                if mc_shortage_float <= 0:
                    mc_display_status = "✅ 시상금확보"
                    mc_display_shortage = "달성!"
                    mc_shortage_color = "#66ff66"
                else:
                    mc_display_status = "🟡 도전중"
                    mc_display_shortage = format_currency(mc_shortage_amount)
                    mc_shortage_color = "#ff6b6b"

            st.markdown(f"""
            <div class="mc-box">
            <strong>도전구간:</strong> {format_currency(mc_challenge)}<br>
            <strong>부족금액:</strong> <span style="color: {mc_shortage_color};">{mc_display_shortage}</span><br>
            <strong>상태:</strong> {mc_display_status}
            </div>
            """, unsafe_allow_html=True)

            # 리플렛 이미지 (우측 컬럼)
            st.markdown("---")
            st.markdown("<h3 style='font-size: 22px; margin-top: 20px; margin-bottom: 15px;'>📄 리플렛</h3>", unsafe_allow_html=True)
            
            agency_name = safe_get_value(row, "대리점")
            image_id = get_image_id_by_agency_name(agency_name)
            
            if image_id:
                leaflet_data = load_leaflet_template_from_drive(image_id)
                if leaflet_data:
                    st.download_button(
                        label="📥 리플렛 다운로드",
                        data=leaflet_data,
                        file_name=f"{agent_name}_leaflet.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.info(f"📧 리플렛을 다운로드할 수 없습니다. (대리점: {agency_name})")
            else:
                st.info(f"📧 리플렛이 등록되지 않았습니다. (대리점: {agency_name})")

            # 하단 버튼
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🖨️ 인쇄", use_container_width=True):
                    st.markdown("<script>window.print();</script>", unsafe_allow_html=True)
            with col2:
                if st.button("🔄 초기화", use_container_width=True):
                    st.rerun()

else:
    # 검색 전 안내 메시지
    st.markdown("""
    <div class="info-message">
    🔍 매니저명과 설계사코드를 입력하고 '조회' 버튼을 클릭하세요.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="caption">
© 2026 Meritz Financial Group. All rights reserved.
</div>
""", unsafe_allow_html=True)
