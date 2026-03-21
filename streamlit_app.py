import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
from PIL import Image
import gdown
import tempfile
import os

# ===== 상수 정의 =====
GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"
LEAFLET_TEMPLATE_IDS = {
    "메가": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
}

# ===== 페이지 설정 =====
st.set_page_config(
    page_title="Meritz Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CSS 스타일 =====
st.markdown("""
<style>
    body {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .info-box {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .performance-box {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #444;
    }
    .mc-box {
        background-color: #1e3a1f;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #66bb6a;
        margin: 8px 0;
    }
    .mc-plus-box {
        background-color: #1a2a3a;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #42a5f5;
        margin: 8px 0;
    }
    .bridge-box {
        background-color: #3a2a1a;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #ffa726;
        margin: 8px 0;
    }
    .title-header {
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin: 20px 0;
    }
    button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        font-weight: bold !important;
    }
    button:hover {
        background-color: #45a049 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== 유틸 함수 =====
def safe_float(value):
    """안전하게 float로 변환"""
    if pd.isna(value):
        return 0.0
    if isinstance(value, str):
        value = value.strip()
        if value == "" or value.lower() == "nan":
            return 0.0
        value = value.replace(",", "").replace("만원", "").replace("만", "").strip()
    try:
        return float(value)
    except:
        return 0.0

def format_currency(value):
    """통화 포맷팅"""
    value = safe_float(value)
    if value >= 1000000:
        return f"{value / 1000000:.1f}백만원"
    elif value >= 10000:
        return f"{value / 10000:.0f}만원"
    else:
        return f"{value:,.0f}원"

def get_current_week():
    """현재 주차 계산 (3월 기준)"""
    today = datetime.now(pytz.timezone('Asia/Seoul')).date()
    year = today.year
    march_1 = datetime(year, 3, 1).date()
    
    if today < march_1:
        return 0
    
    week = (today - march_1).days // 7 + 1
    return min(week, 5)

def load_data_from_google_sheets():
    """Google Sheet에서 데이터 로드 및 컬럼명 정제"""
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
    df = pd.read_csv(url)
    # 컬럼명 앞뒤 공백 제거
    df.columns = df.columns.str.strip()
    return df

def load_leaflet_template_from_drive(file_id):
    """Google Drive에서 이미지 다운로드"""
    if file_id == "none":
        return None
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "leaflet.jpg")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=True)
            if os.path.exists(output):
                return Image.open(output)
    except:
        pass
    return None

def get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel):
    """어센틱 여부와 파트너채널 여부에 따라 리플렛 이미지 ID 선택"""
    if is_authentic and not is_partner_channel:
        return LEAFLET_TEMPLATE_IDS.get("어센틱", "none")
    return "none"

def render_mc_box(title, target, shortage, box_type="mc"):
    """MC/MC+ 박스 렌더링"""
    target_val = safe_float(target)
    shortage_val = safe_float(shortage)
    
    if box_type == "mc":
        css_class = "mc-box"
        icon = "🎯"
    elif box_type == "mc-plus":
        css_class = "mc-plus-box"
        icon = "⭐"
    else:  # bridge
        css_class = "bridge-box"
        icon = "🌉"
    
    st.markdown(f"""
    <div class="{css_class}">
        <b>{icon} {title}</b><br>
        목표: {format_currency(target_val)}<br>
        부족: {format_currency(shortage_val)}
    </div>
    """, unsafe_allow_html=True)

# ===== 메인 UI =====
st.markdown('<div class="title-header">📊 메리츠화재 설계사 성과 조회</div>', unsafe_allow_html=True)

# 사이드바 입력
with st.sidebar:
    st.markdown("### 📋 검색 조건")
    manager_name = st.text_input("매니저명", placeholder="예: 장혜정")
    agent_code = st.text_input("설계사 코드", placeholder="예: 722019151")
    search_clicked = st.button("🔍 검색")
    reset_clicked = st.button("🔄 초기화")

# 데이터 로드
df = load_data_from_google_sheets()

# 검색 실행
if reset_clicked:
    st.rerun()

if search_clicked:
    if not manager_name or not agent_code:
        st.error("⚠️ 매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        # 데이터 필터링
        filtered = df[
            (df["매니저"].astype(str).str.strip() == manager_name.strip()) &
            (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())
        ]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {manager_name} / {agent_code}")
        else:
            row = filtered.iloc[0]
            
            # 기본 정보 추출
            designer_name = row.get("설계사명", "N/A")
            branch_name = row.get("지점명", "N/A")
            is_authentic = int(safe_float(row.get("어센틱구분", 0))) == 1
            is_partner_channel = str(branch_name).strip().startswith("파트너채널")
            
            # 컬럼 매핑 (Y=1 어센틱 vs Y=0 비어센틱)
            if is_authentic and not is_partner_channel:
                current_week_target = safe_float(row.get("어센틱주차목표", 0))
                current_week_shortage = safe_float(row.get("어센틱주차부족최종", 0))
                mc_target = safe_float(row.get("MC도전구간", 0))
                mc_shortage = safe_float(row.get("MC부족최종", 0))
                bridge_display = False  # 어센틱은 브릿지 미표시
            else:
                current_week_target = safe_float(row.get("주차목표", 0))
                current_week_shortage = safe_float(row.get("주차부족", 0))
                mc_target = safe_float(row.get("MC+구간", 0))
                mc_shortage = safe_float(row.get("MC+부족최종", 0))
                bridge_display = True  # 비어센틱은 브릿지 표시
            
            # UI 표시
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="info-box">
                    <b>👤 설계사명:</b> {designer_name}<br>
                    <b>🏢 지점명:</b> {branch_name}
                </div>
                """, unsafe_allow_html=True)
                
                # 3월 누계 성과
                march_performance = safe_float(row.get("3월실적", 0))
                st.markdown(f"""
                <div class="performance-box">
                    <b>📈 3월 누계 성과</b><br>
                    {format_currency(march_performance)}
                </div>
                """, unsafe_allow_html=True)
                
                # 주차별 성과
                st.markdown("**📊 주차별 성과**")
                weeks_data = []
                current_week = get_current_week()
                for week in range(1, 6):
                    week_val = safe_float(row.get(f"{week}주차", 0))
                    is_current = "◀" if week == current_week else " "
                    weeks_data.append(f"{is_current} {week}주차: {format_currency(week_val)}")
                st.markdown("\n".join(weeks_data))
                
                # 현재 주차 목표 및 부족
                st.markdown("**💰 현재주차 목표 & 부족**")
                st.markdown(f"""
                <div class="performance-box">
                    목표: <b>{format_currency(current_week_target)}</b><br>
                    부족: <b>{format_currency(current_week_shortage)}</b>
                </div>
                """, unsafe_allow_html=True)
                
                # 브릿지 (비어센틱만 표시)
                if bridge_display:
                    st.markdown("**🌉 브릿지 성과**")
                    bridge_target = safe_float(row.get("브릿지 도전구간", 0))
                    bridge_shortage = safe_float(row.get("브릿지 부족", 0))
                    render_mc_box("브릿지", bridge_target, bridge_shortage, "bridge")
                
                # MC / MC+ 성과
                st.markdown("**💰 성과**")
                if is_authentic and not is_partner_channel:
                    render_mc_box("MC", mc_target, mc_shortage, "mc")
                    mc_plus_target = safe_float(row.get("MC+구간", 0))
                    mc_plus_shortage = safe_float(row.get("MC+부족최종", 0))
                    render_mc_box("MC+", mc_plus_target, mc_plus_shortage, "mc-plus")
                else:
                    render_mc_box("MC+", mc_target, mc_shortage, "mc-plus")
            
            with col2:
                st.markdown("**📄 안내장**")
                image_id = get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel)
                leaflet_img = load_leaflet_template_from_drive(image_id)
                if leaflet_img:
                    st.image(leaflet_img, use_column_width=True)
                    buf = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    leaflet_img.save(buf)
                    buf.close()
                    with open(buf.name, "rb") as f:
                        st.download_button(
                            label="📥 안내장 다운로드",
                            data=f.read(),
                            file_name=f"{branch_name}_안내장.jpg",
                            mime="image/jpeg"
                        )
                else:
                    st.info("안내장 이미지가 없습니다.")
else:
    st.info("🔍 좌측 사이드바에서 매니저명과 설계사 코드를 입력 후 검색해주세요.")
