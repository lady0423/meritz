import streamlit as st
import pandas as pd
import datetime
import pytz
import io
import os
import tempfile
from PIL import Image
import gdown

# 설정
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

# 다크 테마 & Noto Sans KR 폰트 + 자동완성 비활성화
st.markdown("""
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap' rel='stylesheet'>
<style>
* { font-family: 'Noto Sans KR', sans-serif !important; }
html, body { background: #0f0f0f; color: #e0e0e0; }
.stApp { background: #0f0f0f; }
input { autocomplete: off !important; }
input:-webkit-autofill { -webkit-box-shadow: 0 0 0 1000px #1a1a1a inset !important; -webkit-text-fill-color: #e0e0e0 !important; }
.stTextInput input, .stNumberInput input { background: #1a1a1a; color: #e0e0e0; border: 2px solid #c41e3a !important; }
.stButton > button { background: #c41e3a; color: white; border: none; font-weight: 700; padding: 10px 20px; border-radius: 5px; }
.stButton > button:hover { background: #ff6b7a; }
.info-box { background: #1a1a1a; border-left: 5px solid #c41e3a; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
.cumulative-box { background: linear-gradient(135deg, #1a1a1a, #2a1a1a); border: 2px solid #ff6b7a; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
.weekly-row { background: #1a1a1a; border-left: 5px solid #666; padding: 12px; margin: 8px 0; border-radius: 5px; color: #e0e0e0; }
.weekly-row.current { background: #2a1a1a; border-left: 5px solid #ff6b7a; font-weight: 700; }
.target-box { background: #1a1a1a; border: 2px solid #ff8a99; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
.bridge-box { background: linear-gradient(135deg, #1a1a1a, #2a1a1a); border: 2px solid #ffb366; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
.mc-box { background: linear-gradient(135deg, #1a1a1a, #2a1a1a); border: 2px solid #ff6b7a; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
.mc-plus-box { background: linear-gradient(135deg, #1a1a1a, #2a1a1a); border: 2px solid #9d66ff; padding: 15px; border-radius: 5px; margin: 10px 0; color: #e0e0e0; }
</style>
""", unsafe_allow_html=True)

# 헬퍼 함수들
def safe_float(v):
    try:
        return float(v) if pd.notna(v) and v != '' else 0
    except:
        return 0

def safe_get_value(row, col):
    try:
        val = row.get(col)
        return val if pd.notna(val) and val != '' else 0
    except:
        return 0

def format_currency(value):
    if value == 0:
        return "₩0"
    return f"₩{int(value):,}"

def get_current_week():
    today = datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()
    march_1 = datetime.date(today.year, 3, 1)
    if today.month != 3:
        return 0
    days_diff = (today - march_1).days
    week = (days_diff // 7) + 1
    return min(week, 5)

def get_image_id_by_agency_name(agency_name, branch_name, is_authentic):
    """
    리플렛 이미지 ID를 결정하는 함수
    - is_authentic=True이고 branch_name이 "파트너채널"로 시작하지 않으면 → 어센틱
    - 그 외 → 기존 로직 또는 none
    """
    if is_authentic:
        # 어센틱이고 파트너채널이 아니면 어센틱 리플렛 사용
        if not str(branch_name).startswith("파트너채널"):
            return LEAFLET_TEMPLATE_IDS.get("어센틱")
        else:
            # 파트너채널은 none 사용
            return LEAFLET_TEMPLATE_IDS.get("none")
    else:
        # 기존 방식: 대리점명으로 매칭
        if not agency_name:
            return LEAFLET_TEMPLATE_IDS.get("none")
        for key, val in LEAFLET_TEMPLATE_IDS.items():
            if key.lower() in str(agency_name).lower():
                return val
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

# UI 레이아웃
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("<div style='text-align: center; padding: 10px;'>🏢</div>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='color: #ff8a99; font-size: 40px;'>🎯 3월 3주차 시상 진척</h1>", unsafe_allow_html=True)

st.divider()

# 검색 섹션
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    manager_name = st.text_input("📌 매니저명", key="manager", placeholder="매니저 이름 입력", autocomplete="off")
with col2:
    agent_code = st.text_input("📌 설계사코드", key="agent_code", placeholder="설계사 코드 입력", autocomplete="off")
with col3:
    search_btn = st.button("🔍 검색", use_container_width=True)

# 데이터 로드
df = load_data_from_google_sheets()

# 검색 결과 표시
if search_btn:
    if not manager_name or not agent_code:
        st.warning("⚠️ 매니저명과 설계사코드를 모두 입력해주세요.")
    else:
        # 필터링 (A열 설계사조직코드, D열 매니저명으로 검색)
        filtered = df[
            (df.iloc[:, 3].astype(str).str.strip().str.contains(manager_name.strip(), case=False, na=False)) &
            (df.iloc[:, 0].astype(str).str.strip() == agent_code.strip())
        ]
        
        if filtered.empty:
            st.error(f"❌ 검색 결과가 없습니다. (매니저: {manager_name}, 설계사코드: {agent_code})")
        else:
            row = filtered.iloc[0]
            
            # 기본 정보
            agent_name = safe_get_value(row, row.columns[6])  # G열 설계사명
            branch = safe_get_value(row, row.columns[2])  # C열 지점명
            branch_name = safe_get_value(row, row.columns[5])  # F열 지사명
            
            st.markdown(f"""
            <div class='info-box'>
            <strong>설계사명:</strong> {agent_name} | <strong>지사:</strong> {branch}
            </div>
            """, unsafe_allow_html=True)
            
            # 어센틱 여부 확인 (Y열 = 어센틱구분, 0-indexed 24)
            is_authentic = safe_float(row.iloc[24]) == 1
            
            # 3월 누계 (L열 = 3월실적)
            march_cumulative = safe_float(row.iloc[11])
            st.markdown(f"""
            <div class='cumulative-box'>
            <h3 style='color: #ff8a99;'>📊 3월 누계 실적</h3>
            <strong style='font-size: 24px;'>{format_currency(march_cumulative)}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            current_week = get_current_week()
            
            # 주차별 실적 표시
            st.markdown("<h3 style='color: #ff8a99;'>📈 주차별 실적</h3>", unsafe_allow_html=True)
            
            # 어센틱 (Y=1)인 경우: 새로운 주차 구조 사용
            if is_authentic:
                # 어센틱: 어센틱주차목표(AB열 = 27), 어센틱주차부족(AC열 = 28)
                week_target = safe_float(row.iloc[27])  # AB열
                week_shortage = safe_float(row.iloc[28])  # AC열
                week_result = week_target - week_shortage if week_target > 0 else 0
                
                st.markdown(f"""
                <div class='weekly-row current'>
                <strong>3주차(16~22일)</strong> → <strong style='color: #ff6b7a;'>{format_currency(week_result)}</strong> / 목표 {format_currency(week_target)}
                </div>
                """, unsafe_allow_html=True)
                
                # 현재주차 목표 & 부족
                st.markdown(f"""
                <div class='target-box'>
                <h4 style='color: #ff8a99;'>🎯 현재주차 목표</h4>
                <strong>목표금액:</strong> {format_currency(week_target)}<br>
                <strong>부족금액:</strong> <span style='color: #ff6b6b; font-weight: 700;'>{format_currency(week_shortage)}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # MC 성과 (추가 MC)
                mc_challenge = safe_float(row.iloc[25])  # AA열 MC도전구간
                mc_shortage_raw = safe_float(row.iloc[26])  # AB열 MC부족
                mc_status_raw = safe_get_value(row, row.columns[27])  # AC열 MC부족최종
                
                # MC 상태 로직
                if isinstance(mc_status_raw, str) and "최종달성" in mc_status_raw:
                    mc_display_status = "✅ 시상금확보"
                    mc_shortage_color = "#66ff66"
                elif isinstance(mc_status_raw, str) and ("다음기회에" in mc_status_raw or "재도전" in mc_status_raw):
                    mc_display_status = mc_status_raw
                    mc_shortage_color = "#999999"
                elif safe_float(mc_shortage_raw) > 0:
                    mc_display_status = "🟡 도전중"
                    mc_shortage_color = "#ffb366"
                else:
                    mc_display_status = "✅ 시상금확보"
                    mc_shortage_color = "#66ff66"
                
                st.markdown(f"""
                <div class='mc-box'>
                <h4 style='color: #ff8a99;'>⭐ MC 성과</h4>
                <strong>도전구간:</strong> {format_currency(mc_challenge)}<br>
                <strong>부족금액:</strong> <span style='color: {mc_shortage_color}; font-weight: 700;'>{format_currency(mc_shortage_raw)}</span><br>
                <strong>상태:</strong> <span style='color: #ffb366; font-weight: 700;'>{mc_display_status}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # MC+ 성과 (추가 MC+)
                mc_plus_challenge = safe_float(row.iloc[25])  # AA열 MC도전구간
                mc_plus_result = safe_float(row.iloc[11])  # L열 3월 실적 = MC추가 실적
                mc_plus_shortage = safe_float(row.iloc[26])  # AB열 MC부족
                mc_plus_status_raw = safe_get_value(row, row.columns[27])  # AC열 MC부족최종
                
                # MC+ 상태 로직
                if isinstance(mc_plus_status_raw, str) and "최종달성" in mc_plus_status_raw:
                    mc_plus_display_status = "✅ 시상금확보"
                    mc_plus_shortage_color = "#66ff66"
                elif isinstance(mc_plus_status_raw, str) and ("다음기회에" in mc_plus_status_raw or "재도전" in mc_plus_status_raw):
                    mc_plus_display_status = mc_plus_status_raw
                    mc_plus_shortage_color = "#999999"
                elif safe_float(mc_plus_shortage) > 0:
                    mc_plus_display_status = "🟡 도전중"
                    mc_plus_shortage_color = "#ffb366"
                else:
                    mc_plus_display_status = "✅ 시상금확보"
                    mc_plus_shortage_color = "#66ff66"
                
                st.markdown(f"""
                <div class='mc-plus-box'>
                <h4 style='color: #9d66ff;'>⭐⭐ MC+ 성과</h4>
                <strong>도전구간:</strong> {format_currency(mc_plus_challenge)}<br>
                <strong>부족금액:</strong> <span style='color: {mc_plus_shortage_color}; font-weight: 700;'>{format_currency(mc_plus_shortage)}</span><br>
                <strong>상태:</strong> <span style='color: #9d66ff; font-weight: 700;'>{mc_plus_display_status}</span>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                # 기존 방식: 기존 주차 구조 사용 (M~Q열 = 주차 1~5, 인덱스 12~16)
                for week in range(1, 6):
                    col_idx = 12 + (week - 1)
                    week_result = safe_float(row.iloc[col_idx])
                    is_current = week == current_week
                    row_class = "weekly-row current" if is_current else "weekly-row"
                    week_dates = ["", "1~8일", "9~15일", "16~22일", "23~29일", "30~31일"]
                    
                    st.markdown(f"""
                    <div class='{row_class}'>
                    <strong>{week}주차({week_dates[week]})</strong> → <strong style='color: #ff6b7a;'>{format_currency(week_result)}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 현재주차 목표 & 부족 (R열 주차목표 = 17, S열 주차부족 = 18)
                week_target = safe_float(row.iloc[17])
                week_shortage = safe_float(row.iloc[18])
                
                st.markdown(f"""
                <div class='target-box'>
                <h4 style='color: #ff8a99;'>🎯 현재주차 목표</h4>
                <strong>목표금액:</strong> {format_currency(week_target)}<br>
                <strong>부족금액:</strong> <span style='color: #ff6b6b; font-weight: 700;'>{format_currency(week_shortage)}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 브릿지 성과 (H열 브릿지실적 = 7, I열 브릿지도전구간 = 8, J열 브릿지부족 = 9)
                bridge_result = safe_float(row.iloc[7])
                bridge_target = safe_float(row.iloc[8])
                bridge_shortage = safe_float(row.iloc[9])
                
                st.markdown(f"""
                <div class='bridge-box'>
                <h4 style='color: #ffb366;'>🌉 브릿지 성과</h4>
                <strong>진척:</strong> {format_currency(bridge_result)}<br>
                <strong>목표:</strong> {format_currency(bridge_target)}<br>
                <strong>부족금액:</strong> <span style='color: #ffb366; font-weight: 700;'>{format_currency(bridge_shortage)}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # MC+ 성과 (기존 방식)
                # T열 MC+구간 = 19, U열 MC+부족 = 20, V열 MC+부족최종 = 21
                mc_challenge = safe_float(row.iloc[19])
                mc_shortage_raw = safe_float(row.iloc[20])
                mc_status_raw = safe_get_value(row, row.columns[21])
                
                if isinstance(mc_status_raw, str) and "최종달성" in mc_status_raw:
                    mc_display_status = "✅ 시상금확보"
                    mc_shortage_color = "#66ff66"
                elif isinstance(mc_status_raw, str) and ("다음기회에" in mc_status_raw or "재도전" in mc_status_raw):
                    mc_display_status = mc_status_raw
                    mc_shortage_color = "#999999"
                elif safe_float(mc_shortage_raw) > 0:
                    mc_display_status = "🟡 도전중"
                    mc_shortage_color = "#ffb366"
                else:
                    mc_display_status = "✅ 시상금확보"
                    mc_shortage_color = "#66ff66"
                
                st.markdown(f"""
                <div class='mc-plus-box'>
                <h4 style='color: #9d66ff;'>⭐⭐ MC+ 성과</h4>
                <strong>도전구간:</strong> {format_currency(mc_challenge)}<br>
                <strong>부족금액:</strong> <span style='color: {mc_shortage_color}; font-weight: 700;'>{format_currency(mc_shortage_raw)}</span><br>
                <strong>상태:</strong> <span style='color: #9d66ff; font-weight: 700;'>{mc_display_status}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # 대리점 리플렛
            st.markdown("<h3 style='color: #ff8a99;'>🎁 대리점 리플렛</h3>", unsafe_allow_html=True)
            image_id = get_image_id_by_agency_name(str(branch), str(branch_name), is_authentic)
            image = load_leaflet_template_from_drive(image_id)
            if image:
                st.image(image, use_container_width=True)
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    image.save(tmp.name, "JPEG")
                    with open(tmp.name, "rb") as f:
                        st.download_button(
                            label="📥 리플렛 다운로드",
                            data=f.read(),
                            file_name=f"{branch}_leaflet.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
            else:
                st.info("ℹ️ 리플렛 이미지를 찾을 수 없습니다.")
            
            # 초기화 버튼
            st.divider()
            if st.button("🔄 초기화", use_container_width=True):
                st.rerun()

else:
    st.markdown("""
    <div style='text-align: center; padding: 50px; color: #999999;'>
    <h2>🔒 프라이버시 보호</h2>
    <p>좌상단에서 <strong>매니저명</strong>과 <strong>설계사코드</strong>를 입력 후 <strong>검색</strong> 버튼을 클릭해주세요.</p>
    </div>
    """, unsafe_allow_html=True)
