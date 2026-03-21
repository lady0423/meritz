import streamlit as st
import pandas as pd
import gdown
import tempfile
import os
import io
from datetime import datetime
import pytz
from PIL import Image

# ===== Configuration =====
GOOGLE_DRIVE_FILE_ID = "1Fskr_W72wVXYnIwEWgONldpWrLA-jngu"  # 새로운 ID

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

# ===== Page Config =====
st.set_page_config(
    page_title="실적 안내장 조회",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CSS Styling =====
st.markdown("""
<style>
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    body {
        background-color: #0f1419;
        color: #e0e0e0;
    }
    .main {
        background-color: #0f1419;
    }
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 12px;
        padding: 8px 0;
        border-bottom: 2px solid #4a90e2;
    }
    .info-box {
        background: linear-gradient(135deg, #1a2634 0%, #0f1f2e 100%);
        border-left: 4px solid #4a90e2;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 14px;
    }
    .cumulative-box {
        background: linear-gradient(135deg, #1a2634 0%, #0f1f2e 100%);
        border: 1px solid #3a5a7a;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
    }
    .cumulative-label {
        font-size: 12px;
        color: #a0a0a0;
        margin-bottom: 4px;
    }
    .cumulative-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    .weekly-row {
        background: linear-gradient(135deg, #1a2634 0%, #0f1f2e 100%);
        border: 1px solid #3a5a7a;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .weekly-row.highlight {
        background: linear-gradient(135deg, #cc3333 0%, #bb2222 100%);
        border: 1px solid #ff6666;
    }
    .weekly-label {
        font-size: 13px;
        color: #b0b0b0;
        font-weight: 500;
    }
    .weekly-value {
        font-size: 16px;
        color: #ffffff;
        font-weight: 600;
    }
    .bridge-box {
        background: linear-gradient(135deg, #2d5a3d 0%, #3d7a4f 100%);
        border: 1px solid #5a9a6f;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .bridge-label {
        font-size: 12px;
        color: #b0d9c0;
        margin-bottom: 6px;
    }
    .bridge-target {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }
    .bridge-bottom {
        display: flex;
        justify-content: space-between;
        gap: 12px;
    }
    .bridge-item {
        flex: 1;
        text-align: center;
    }
    .bridge-item-label {
        font-size: 11px;
        color: #b0d9c0;
        margin-bottom: 4px;
    }
    .bridge-item-value {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    .mc-box {
        background: linear-gradient(135deg, #1a4d6d 0%, #2570a0 100%);
        border: 1px solid #4a8ab8;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .mc-label {
        font-size: 12px;
        color: #a0d4f0;
        margin-bottom: 6px;
    }
    .mc-challenge {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }
    .mc-bottom {
        display: flex;
        justify-content: space-between;
        gap: 12px;
    }
    .mc-item {
        flex: 1;
        text-align: center;
    }
    .mc-item-label {
        font-size: 11px;
        color: #a0d4f0;
        margin-bottom: 4px;
    }
    .mc-item-value {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    input[type="text"] {
        background-color: #1a2634 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== Utility Functions =====
def safe_float(value):
    """안전하게 float 변환"""
    try:
        return float(value) if value not in [None, "", "nan"] else 0.0
    except:
        return 0.0

def safe_get_value(row, col_name):
    """행에서 안전하게 값 추출"""
    try:
        val = row[col_name] if col_name in row.index else None
        return val if val not in [None, "", "nan"] else 0
    except:
        return 0

def format_currency(amount):
    """통화 형식으로 변환"""
    amount = safe_float(amount)
    return f"₩{amount:,.0f}"

def get_current_week():
    """현재 주차 계산 (월별)"""
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).date()
    day = today.day
    return (day - 1) // 7 + 1

def get_image_id_by_agency_name(agency_name_full):
    """대리점명으로 이미지 ID 자동 매칭"""
    agency_name_full = str(agency_name_full).strip().lower()
    for keyword, image_id in LEAFLET_TEMPLATE_IDS.items():
        if keyword.lower() in agency_name_full:
            return image_id
    return None

# ===== Data Loading =====
@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    """Google Drive에서 Excel 데이터 로드"""
    temp_path = os.path.join(tempfile.gettempdir(), "temp_data.xlsx")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
    return pd.read_excel(temp_path, sheet_name=0, header=0)

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 이미지 로드"""
    temp_path = os.path.join(tempfile.gettempdir(), f"leaflet_{file_id}.jpg")
    try:
        gdown.download(f"https://drive.google.com/uc?id={file_id}", temp_path, quiet=True)
        if os.path.exists(temp_path):
            return Image.open(temp_path)
    except Exception as e:
        pass
    return None

# ===== Header =====
col_logo, col_title = st.columns([1, 9])
with col_logo:
    try:
        logo = Image.open("meritz.png")
        st.image(logo, width=60)
    except:
        st.write("🏢")

with col_title:
    st.markdown('<div class="section-header">실적 안내장 조회</div>', unsafe_allow_html=True)

kst = pytz.timezone('Asia/Seoul')
last_update = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"최신 업데이트: {last_update} (KST)")

st.markdown("---")

# ===== Search Input =====
col_manager, col_agent, col_search = st.columns([3, 3, 1])

with col_manager:
    manager_name = st.text_input(
        "매니저명",
        key="manager_input",
        autocomplete="off"
    )

with col_agent:
    agent_code = st.text_input(
        "설계사 코드",
        key="agent_input",
        autocomplete="off"
    )

with col_search:
    search_clicked = st.button("🔍 검색", use_container_width=True)

st.markdown("---")

# ===== Search Logic =====
if search_clicked:
    if not manager_name or not agent_code:
        st.error("매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        try:
            df = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)
            
            # 매니저명과 설계사코드로 필터링
            filtered = df[(df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                         (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())]
            
            if filtered.empty:
                st.warning("해당하는 데이터가 없습니다.")
            else:
                row = filtered.iloc[0]
                
                # 필드 추출
                agent_code_display = safe_get_value(row, "현재대리점설계사조직코드")
                agent_name = safe_get_value(row, "설계사명")
                branch = safe_get_value(row, "지사명")
                manager = safe_get_value(row, "매니저")
                agency_name = safe_get_value(row, "대리점")
                cumulative = safe_float(safe_get_value(row, "3월실적"))
                
                # 주차별 값
                weekly_values = [
                    safe_float(safe_get_value(row, "1주차")),
                    safe_float(safe_get_value(row, "2주차")),
                    safe_float(safe_get_value(row, "3주차")),
                    safe_float(safe_get_value(row, "4주차")),
                    safe_float(safe_get_value(row, "5주차")),
                ]
                
                # 브릿지
                bridge_progress = safe_float(safe_get_value(row, "브릿지 실적"))
                bridge_target = safe_float(safe_get_value(row, "브릿지 도전구간"))
                bridge_shortage = safe_float(safe_get_value(row, "브릿지 부족"))
                
                # MC+
                mc_challenge = safe_float(safe_get_value(row, "MC+구간"))
                mc_shortage = safe_float(safe_get_value(row, "MC부족최종"))
                
                current_week = get_current_week()
                
                # ===== 왼쪽 컬럼 =====
                col_left, col_right = st.columns([1, 1])
                
                with col_left:
                    # 기본 정보
                    st.markdown('<div class="section-header">📋 기본 정보</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>설계사:</strong> {agent_name}<br>
                        <strong>지사:</strong> {branch}<br>
                        <strong>코드:</strong> {agent_code_display}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 누계 실적
                    st.markdown('<div class="section-header">📊 누계 실적</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="cumulative-box">
                        <div class="cumulative-label">누계</div>
                        <div class="cumulative-value">{format_currency(cumulative)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 주차별 실적
                    st.markdown('<div class="section-header">📈 주차별 실적</div>', unsafe_allow_html=True)
                    for week_num in range(1, 6):
                        week_value = weekly_values[week_num - 1]
                        is_current = (week_num == current_week)
                        highlight_class = "highlight" if is_current else ""
                        st.markdown(f"""
                        <div class="weekly-row {highlight_class}">
                            <span class="weekly-label">{week_num}주차</span>
                            <span class="weekly-value">{format_currency(week_value)}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 브릿지 실적
                    st.markdown('<div class="section-header">🌉 브릿지 실적</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="bridge-box">
                        <div class="bridge-label">목표</div>
                        <div class="bridge-target">{format_currency(bridge_target)}</div>
                        <div class="bridge-bottom">
                            <div class="bridge-item">
                                <div class="bridge-item-label">진척</div>
                                <div class="bridge-item-value">{format_currency(bridge_progress)}</div>
                            </div>
                            <div class="bridge-item">
                                <div class="bridge-item-label">부족</div>
                                <div class="bridge-item-value">{format_currency(bridge_shortage)}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # MC+ 상태
                    st.markdown('<div class="section-header">⭐ MC+ 상태</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="mc-box">
                        <div class="mc-label">도전구간</div>
                        <div class="mc-challenge">{format_currency(mc_challenge)}</div>
                        <div class="mc-bottom">
                            <div class="mc-item" style="flex: 1;">
                                <div class="mc-item-label">부족금액</div>
                                <div class="mc-item-value">{format_currency(mc_shortage)}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # ===== 오른쪽 컬럼 (안내장) =====
                with col_right:
                    st.markdown('<div class="section-header">📄 안내장 템플릿</div>', unsafe_allow_html=True)
                    agency_name_str = str(agency_name).strip()
                    image_id = get_image_id_by_agency_name(agency_name_str)
                    
                    if image_id:
                        with st.spinner(f"🔄 {agency_name_str} 안내장 로드 중..."):
                            leaflet_img = load_leaflet_template_from_drive(image_id)
                        
                        if leaflet_img:
                            st.image(leaflet_img, use_container_width=True)
                            
                            # 다운로드 버튼
                            img_byte_arr = io.BytesIO()
                            leaflet_img.save(img_byte_arr, format='JPEG')
                            img_byte_arr.seek(0)
                            st.download_button(
                                label="📥 JPG 다운로드",
                                data=img_byte_arr,
                                file_name=f"{agency_name_str}_leaflet.jpg",
                                mime="image/jpeg",
                                use_container_width=True
                            )
                        else:
                            st.warning(f"⚠️ 이미지를 로드할 수 없습니다.\n\n**대리점:** {agency_name_str}")
                    else:
                        st.info(f"📌 **대리점명:** {agency_name_str}\n\n이 대리점의 이미지가 설정되지 않았습니다.")
                
                st.markdown("---")
                
                # 인쇄 및 초기화 버튼
                col_print, col_reset = st.columns(2)
                with col_print:
                    st.button("🖨️ 인쇄", use_container_width=True)
                with col_reset:
                    if st.button("🔄 초기화", use_container_width=True):
                        st.rerun()
        
        except Exception as e:
            st.error(f"오류 발생: {e}")
            with st.expander("🔍 상세 오류 정보"):
                st.write(str(e))

st.markdown("---")
st.caption("💡 팁: 매니저명과 설계사 코드를 입력하고 검색 버튼을 클릭하세요.")
