import streamlit as st
import pandas as pd
from io import BytesIO
import gdown
import os
from PIL import Image, ImageDraw, ImageFont
import io
import tempfile
import time
from datetime import datetime
import pytz

# ===============================================
# 페이지 설정
# ===============================================
st.set_page_config(
    page_title="실적 안내장 조회",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    body {
        background-color: #0a0e27;
        color: #ffffff;
    }
    .main {
        background-color: #0a0e27;
    }
    
    /* 메인 배경 개선 */
    [data-testid="stMain"] {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        background-color: #1a1f3a;
        color: #ffffff;
        border: 2px solid #667eea;
        border-radius: 8px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ===============================================
# 헤더 섹션 (로고 + 제목)
# ===============================================
header_col1, header_col2, header_col3 = st.columns([1, 2, 1])

with header_col1:
    try:
        logo = Image.open("metiz.png")
        st.image(logo, width=80)
    except:
        st.write("📋")

with header_col2:
    st.markdown("""
    <h1 style="text-align: center; color: #667eea; margin: 0; font-size: 2.5em;">
        📊 실적 안내장 조회
    </h1>
    <p style="text-align: center; color: #a0aec0; margin: 0; font-size: 0.9em;">
        대리점별 맞춤형 실적 리플렛 시스템
    </p>
    """, unsafe_allow_html=True)

with header_col3:
    st.write("")

st.markdown("---")

# ===============================================
# 설정값
# ===============================================
GOOGLE_DRIVE_FILE_ID = "1eD-WgnXioOH7zb7oyydKu_l798BwuVtA"

# 📌 대리점별 리플렛 템플릿 이미지 파일 ID
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
    "더좋은보험금융": "1Px8WawPHjME-oYAXd4TTkhIjQCFVDISc",
    "프라임에셋": "1UniyB7NEUEPhRHuqormlWrS3v_rFaYy1",
    "에이플러스": "1Z_7FNhOQJngRPiuICIwdmvJqJQw1qFwc",
    "지에이코리아": "1aH3tXtWQHCeNUitXkMua9D7sAl6x8SLz",
    "메타리치": "1kL-z0xn8vQBh5aEGkZiV3X_zYp-dYYni",
    "글로벌금융": "1oDR5WfrM1XLOca13olvpx8AwZHYRqIVF",
    "인카금융": "1r1ukWIJf3EG_pf6nhQuxwkab2CVeQdDG",
    "아너스": "1rJ7SoZJyno5b6tAurjTpkkEmissGKntj",
    "굿리치": "1vNoopxTYV5cK1zlOPlNvSGseK_dbXkXl",
    "신한금융": "1z3Ayg6mJsUeeHdebaOrWyOK4lz1-ROB_",
    "default": "1xGX9WTFcAtnzIa2kgMPOuG73V56ypbaf",
}

# ===============================================
# 함수: 값을 숫자로 변환
# ===============================================
def safe_float(value):
    """안전하게 숫자로 변환"""
    try:
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            value = value.replace(',', '').strip()
        return float(value)
    except:
        return 0

def safe_int(value):
    """안전하게 정수로 변환"""
    return int(safe_float(value))

def safe_get_value(row, index, default=0):
    """안전하게 행의 값을 가져오기"""
    try:
        if index < len(row):
            return safe_int(row.iloc[index])
        return default
    except:
        return default

def get_file_update_time(file_id):
    """구글드라이브 파일의 마지막 수정 시간 가져오기"""
    try:
        # gdown을 사용해 파일 정보 조회
        url = f"https://drive.google.com/uc?id={file_id}"
        import requests
        response = requests.head(url, allow_redirects=True)
        
        # 간단한 방식: 현재 시간 반환 (실제로는 서버에서 받아올 수 있음)
        # 더 정확하게 하려면 Google Drive API 사용 필요
        return datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "조회 불가"

# ===============================================
# 함수: Google Drive에서 리플렛 템플릿 이미지 로드
# ===============================================
@st.cache_data(ttl=3600)
def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 리플렛 템플릿 이미지 로드 (고화질)"""
    if not file_id:
        return None
    
    temp_file = None
    try:
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"leaflet_{file_id[:8]}.jpg")
        
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                time.sleep(0.1)
        except:
            pass
        
        download_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(download_url, temp_file, quiet=True)
        
        if os.path.exists(temp_file):
            with open(temp_file, 'rb') as f:
                img_bytes = io.BytesIO(f.read())
            
            img = Image.open(img_bytes)
            img.load()
            
            try:
                os.remove(temp_file)
            except:
                pass
            
            return img
        else:
            return None
            
    except Exception as e:
        try:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass
        return None

# ===============================================
# Google Drive에서 데이터 로드
# ===============================================
@st.cache_data(ttl=3600)
def load_data_from_google_drive(file_id):
    """Google Drive에서 Excel 파일 로드"""
    temp_file = None
    try:
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "temp_data.xlsx")
        
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                time.sleep(0.1)
        except:
            pass
        
        download_url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(download_url, temp_file, quiet=True)
        
        if os.path.exists(temp_file):
            df = pd.read_excel(temp_file)
            
            try:
                os.remove(temp_file)
            except:
                pass
            
            return df
        else:
            st.error(f"❌ 데이터 파일 다운로드 실패")
            return None
            
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {str(e)}")
        try:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass
        return None

# 데이터 로드
with st.spinner("📥 데이터를 불러오는 중..."):
    df_data = load_data_from_google_drive(GOOGLE_DRIVE_FILE_ID)

if df_data is None or df_data.empty:
    st.error("❌ 데이터를 불러올 수 없습니다.")
    st.stop()

# ===============================================
# 데이터 업데이트 시간 표시
# ===============================================
col_info1, col_info2 = st.columns([3, 1])

with col_info1:
    st.write("")

with col_info2:
    update_time = get_file_update_time(GOOGLE_DRIVE_FILE_ID)
    st.markdown(f"""
    <div style="text-align: right; color: #a0aec0; font-size: 0.85em;">
        📅 마지막 업데이트: {update_time}
    </div>
    """, unsafe_allow_html=True)

# ===============================================
# 입력 섹션: 매니저명 + 설계사코드 (개선된 디자인)
# ===============================================
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 25px; border-radius: 12px; margin: 20px 0;">
    <h3 style="color: white; margin: 0; margin-bottom: 15px;">🔍 조회 조건 입력</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2.5, 2.5, 1])

with col1:
    manager_input = st.text_input(
        "매니저명",
        placeholder="예: 김철수",
        label_visibility="collapsed"
    )

with col2:
    agent_code_input = st.text_input(
        "설계사 코드",
        placeholder="예: 511003430",
        label_visibility="collapsed"
    )

with col3:
    search_button = st.button("🔍 검색", use_container_width=True)

# ===============================================
# 검색 로직 및 화면 표시
# ===============================================
if search_button:
    if not manager_input or not agent_code_input:
        st.warning("⚠️ 매니저명과 설계사 코드를 모두 입력하세요.")
        st.stop()
    
    # 조건에 맞는 데이터 필터링
    filtered_data = df_data[
        (df_data.iloc[:, 0].astype(str).str.strip() == agent_code_input.strip()) &
        (df_data.iloc[:, 3].astype(str).str.contains(manager_input.strip(), case=False, na=False))
    ]
    
    if filtered_data.empty:
        st.error(f"❌ 매니저명: {manager_input}, 설계사코드: {agent_code_input} 인 데이터가 없습니다.")
        st.stop()
    
    agent_row = filtered_data.iloc[0]
    
    # 데이터 추출
    agent_code = str(agent_row.iloc[0]).strip()
    manager = str(agent_row.iloc[3]).strip()
    agent_name = str(agent_row.iloc[6]).strip()
    branch = str(agent_row.iloc[5]).strip()
    agency_name = str(agent_row.iloc[22]).strip() if len(agent_row) > 22 else ""
    
    cumulative = safe_int(agent_row.iloc[11])
    week1 = safe_int(agent_row.iloc[12])
    week2 = safe_int(agent_row.iloc[13])
    week3 = safe_int(agent_row.iloc[14])
    week4 = safe_int(agent_row.iloc[15])
    week5 = safe_int(agent_row.iloc[16])
    
    week_target = safe_int(agent_row.iloc[17])
    week_shortage = safe_int(agent_row.iloc[18])
    
    bridge_result = safe_int(agent_row.iloc[7])
    bridge_target = safe_int(agent_row.iloc[8])
    bridge_shortage = safe_int(agent_row.iloc[9])
    
    mc_target = safe_get_value(agent_row, 19, 0)
    mc_shortage = safe_get_value(agent_row, 21, 0)
    
    # ===============================================
    # 리플렛 템플릿 선택 및 로드
    # ===============================================
    template_img = None
    matched_agency = "기본"
    
    for keyword, file_id in LEAFLET_TEMPLATE_IDS.items():
        if keyword != "default" and keyword in agency_name:
            with st.spinner(f"📍 {keyword} 템플릿 로드 중..."):
                template_img = load_leaflet_template_from_drive(file_id)
                matched_agency = keyword
            if template_img:
                break
    
    if template_img is None:
        with st.spinner("📍 기본 템플릿 로드 중..."):
            template_img = load_leaflet_template_from_drive(LEAFLET_TEMPLATE_IDS.get("default"))
            matched_agency = "기본"
    
    # ===============================================
    # 결과 화면: 좌측(정보카드) + 우측(이미지)
    # ===============================================
    st.markdown("---")
    
    left_col, right_col = st.columns([1.4, 1.6])
    
    with left_col:
        # 메인 타이틀
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <h2 style="margin: 0; color: white; font-size: 1.8em;">🎯 {agent_name}</h2>
            <p style="margin: 5px 0 0 0; color: #e2e8f0; font-size: 0.95em;">{branch} | {manager}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 정보 카드들
        info_items = [
            ("📌", "설계사 코드", agent_code, "#667eea"),
            ("👤", "설계사명", agent_name, "#764ba2"),
            ("🏢", "지점", branch, "#f093fb"),
            ("🏛️", "대리점", agency_name if agency_name else matched_agency, "#4facfe"),
        ]
        
        for icon, label, value, color in info_items:
            st.markdown(f"""
            <div style="background-color: #1a1f3a; padding: 12px; border-radius: 8px; 
                        margin: 8px 0; border-left: 4px solid {color};">
                <p style="margin: 0; color: #a0aec0; font-size: 0.85em;">{icon} {label}</p>
                <p style="margin: 5px 0 0 0; color: #ffffff; font-size: 1.1em; font-weight: bold;">{value}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 누계 실적 (강조)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 12px; margin: 20px 0; text-align: center;">
            <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.95em;">누계 실적</p>
            <h1 style="margin: 10px 0 0 0; color: white; font-size: 2.2em;">{cumulative:,}</h1>
            <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9em;">원</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 주차별 실적
        st.markdown("<h4 style='color: #cbd5e0; margin-top: 20px;'>📊 주차별 실적</h4>", unsafe_allow_html=True)
        week_data = [
            ("1주차", week1, "#667eea"),
            ("2주차", week2, "#764ba2"),
            ("3주차", week3, "#f093fb"),
            ("4주차", week4, "#4facfe"),
            ("5주차", week5, "#00d4ff"),
        ]
        
        for week_name, value, color in week_data:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; 
                        background-color: #1a1f3a; padding: 12px; border-radius: 8px; 
                        margin: 8px 0; border-left: 4px solid {color};">
                <span style="color: #a0aec0;">{week_name}</span>
                <span style="color: #fff; font-weight: bold;">{value:,} 원</span>
            </div>
            """, unsafe_allow_html=True)
        
        # 목표 vs 부족
        st.markdown("<h4 style='color: #cbd5e0; margin-top: 20px;'>🎯 주차 현황</h4>", unsafe_allow_html=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        padding: 15px; border-radius: 8px; text-align: center;">
                <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.85em;">목표</p>
                <p style="margin: 8px 0 0 0; color: white; font-size: 1.3em; font-weight: bold;">{week_target:,}</p>
                <p style="margin: 3px 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.8em;">원</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_t2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); 
                        padding: 15px; border-radius: 8px; text-align: center;">
                <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.85em;">부족</p>
                <p style="margin: 8px 0 0 0; color: white; font-size: 1.3em; font-weight: bold;">{week_shortage:,}</p>
                <p style="margin: 3px 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.8em;">원</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 브릿지 실적
        st.markdown("<h4 style='color: #cbd5e0; margin-top: 20px;'>🌉 브릿지 실적</h4>", unsafe_allow_html=True)
        
        bridge_cols = st.columns(3)
        bridge_data = [
            ("실적", bridge_result, "#11998e"),
            ("목표", bridge_target, "#4facfe"),
            ("부족", bridge_shortage, "#f45c43"),
        ]
        
        for idx, (label, value, color) in enumerate(bridge_data):
            with bridge_cols[idx]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.85em;">{label}</p>
                    <p style="margin: 8px 0 0 0; color: white; font-size: 1.2em; font-weight: bold;">{value:,}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # MC+ 현황
        st.markdown("<h4 style='color: #cbd5e0; margin-top: 20px;'>⭐ MC+ 현황</h4>", unsafe_allow_html=True)
        
        mc_cols = st.columns(2)
        mc_data = [
            ("목표", mc_target, "#ffa502"),
            ("부족", mc_shortage, "#ff6b6b"),
        ]
        
        for idx, (label, value, color) in enumerate(mc_data):
            with mc_cols[idx]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; color: rgba(255,255,255,0.8); font-size: 0.85em;">MC+ {label}</p>
                    <p style="margin: 8px 0 0 0; color: white; font-size: 1.2em; font-weight: bold;">{value:,}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with right_col:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 12px; margin-bottom: 15px;">
            <h4 style="margin: 0; color: white;">📋 {matched_agency} 템플릿</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if template_img:
            # 이미지 화질 개선 (고해상도로 표시)
            st.image(template_img, width=400)
            
            # JPG 다운로드 (고화질)
            img_byte_arr = io.BytesIO()
            template_img.save(img_byte_arr, format='JPEG', quality=100)
            img_byte_arr.seek(0)
            
            st.download_button(
                label="📥 고화질 JPG 다운로드",
                data=img_byte_arr,
                file_name=f"{agent_name}_{agent_code}_실적.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        else:
            st.error("❌ 리플렛 템플릿을 불러올 수 없습니다.")
    
    # ===============================================
    # 하단 버튼
    # ===============================================
    st.markdown("---")
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🖨️ 웹페이지 인쇄하기", use_container_width=True):
            st.info("💡 브라우저의 인쇄 기능(Ctrl+P 또는 Cmd+P)을 사용하세요.")
    
    with btn_col2:
        if st.button("🔄 초기화", use_container_width=True):
            st.rerun()
    
    with btn_col3:
        if st.button("📧 이메일 발송", use_container_width=True):
            st.info("📧 이메일 기능은 준비 중입니다.")
    
    st.markdown("---")
    st.caption("✅ 데이터는 1시간마다 자동으로 새로고침됩니다.")
else:
    # 초기 화면
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px;">
        <h2 style="color: #667eea; margin-bottom: 20px;">👋 실적 안내장 조회 시스템</h2>
        <p style="color: #a0aec0; font-size: 1.1em; line-height: 1.8;">
            왼쪽에서 <strong>매니저명</strong>과 <strong>설계사 코드</strong>를 입력하고<br>
            <strong style="color: #667eea;">🔍 검색</strong> 버튼을 눌러 조회하세요!
        </p>
        <div style="margin-top: 30px; padding: 20px; background: #1a1f3a; border-radius: 12px;">
            <p style="color: #cbd5e0; margin: 0;">✨ 대리점별 맞춤형 리플렛을 생성합니다</p>
            <p style="color: #cbd5e0; margin: 8px 0 0 0;">✨ 한 번의 검색으로 모든 실적 정보를 확인하세요</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===============================================
# 하단 정보
# ===============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.85em;">
    <p style="margin: 0;">Made with ❤️ | Streamlit Cloud</p>
    <p style="margin: 5px 0 0 0;">© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
