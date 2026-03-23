import streamlit as st
import pandas as pd
import datetime
import pytz
import re
import os
import tempfile
from PIL import Image
import gdown

GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

LEAFLET_TEMPLATE_IDS = {
    "메가": "1N0Aq60bQnPjg7o4GFv19lbqv3pUc57H8",
    "토스": "1Xn_hB6Xl6fojhcgyF2zVlpYtyQst5ann",
    "메타리치": "13MXbTMcaq0E9ugf9V4Yh1wGfNcavQSvX",
    "메타비": "1vLvV7D0qn4cpKSb5gVVnWMXMQnPj_bLI",
    "비플라이": "1ItCJ0l_UT-qNPAVPNHLFLJrDe0u7Hvlv",
    "리치": "1LwKLLs0_DU7w5YXdlR32hvGXLVZT9EVM",
    "라온": "1i6b4Bv5GG6qKVu4Zo6LZWUxPAUKkVYU6",
    "로또": "1cfI0l6NNOKFUr9xFqKjQVYvnlLjSdQ0D",
    "디오": "1qnMLg8mVE0oqT0Q7OeGYBbBVQN2YE_ll",
    "마일": "1VO-3Kj_TI7nGz2ORDXfZYIvwzDFn6XpA",
    "none": "19ZnaS2s4X8JKv27NW9FFuMUVh32i3hc0",
}

st.set_page_config(page_title="메리츠 실적현황", layout="wide")

# ========== Dark Theme CSS ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700&display=swap');

* { font-family: 'Pretendard', sans-serif; }
body { background-color: #0f0f0f; color: #ffffff; }
.stApp { background-color: #0f0f0f; }

[data-testid="stMetric"] { background-color: #1a1a1a; padding: 20px; border-radius: 10px; }

.info-box { background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-left: 5px solid #ffa500; padding: 20px; border-radius: 8px; margin-bottom: 15px; }
.cumulative-box { background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-left: 5px solid #ffdc00; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.weekly-box { background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-left: 5px solid #66ccff; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.target-box { background: linear-gradient(135deg, #1a1a1a 0%, #131313 100%); border-left: 5px solid #ff6b6b; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.bridge-box { background: linear-gradient(135deg, #2a1a1a 0%, #1a1313 100%); border-left: 5px solid #ff8c42; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.mc-box { background: linear-gradient(135deg, #1a2a1a 0%, #131a13 100%); border-left: 5px solid #66ff66; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
.mc-plus-box { background: linear-gradient(135deg, #1a1a2a 0%, #131313 100%); border-left: 5px solid #66ccff; padding: 15px; border-radius: 8px; margin-bottom: 10px; }

input, textarea { background-color: #1a1a1a !important; color: #ffffff !important; border: 1px solid #333 !important; }
input:-webkit-autofill { -webkit-box-shadow: 0 0 0 1000px #1a1a1a inset !important; -webkit-text-fill-color: #ffffff !important; }
input:-webkit-autofill::first-line { font-family: 'Pretendard' !important; }

.stButton > button { background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); color: #ffffff; border: 1px solid #444; }
.stButton > button:hover { background: linear-gradient(135deg, #3a3a3a 0%, #2a2a2a 100%); }

.stSelectbox { background-color: #1a1a1a; }
[data-baseweb="select"] { background-color: #1a1a1a; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #0f0f0f; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }

.duplicate-selector { background-color: #1a1a1a; border: 1px solid #444; color: #ffffff; padding: 10px; margin: 5px 0; border-radius: 5px; cursor: pointer; }
.duplicate-selector:hover { background-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ========== Helper Functions ==========
def safe_float(value):
    try:
        return float(value) if value else 0.0
    except:
        return 0.0

def format_display(value):
    try:
        num = float(value)
        return f"{num:,.0f}" if num else "0"
    except:
        return str(value)

def get_current_week():
    today = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    day_of_month = today.day
    if day_of_month <= 7:
        return 1
    elif day_of_month <= 14:
        return 2
    elif day_of_month <= 21:
        return 3
    elif day_of_month <= 28:
        return 4
    else:
        return 5

def get_image_id_by_authentic_and_partner(is_authentic, is_partner, agency_name):
    if agency_name in LEAFLET_TEMPLATE_IDS:
        return LEAFLET_TEMPLATE_IDS[agency_name]
    return LEAFLET_TEMPLATE_IDS.get("none", "19ZnaS2s4X8JKv27NW9FFuMUVh32i3hc0")

def extract_branch_number(branch_name):
    match = re.search(r'\d+', branch_name)
    return int(match.group()) if match else 0

@st.cache_data(ttl=300)
def load_data_from_google_sheets():
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=0"
    df = pd.read_csv(url)
    return df

@st.cache_data(ttl=300)
def load_leaflet_template_from_drive(file_id):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "leaflet.png")
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=True)
            return Image.open(output_path)
    except Exception as e:
        st.error(f"리플렛 이미지 로드 실패: {e}")
        return None

def load_logo():
    if os.path.exists("meritz.png"):
        return Image.open("meritz.png")
    return None

def render_mc_box(challenge, shortage, is_auth=False, is_mc_plus=False):
    challenge_val = safe_float(challenge)
    shortage_val = safe_float(shortage)
    
    css_class = "mc-plus-box" if is_mc_plus else "mc-box"
    title = "MC PLUS+" if is_mc_plus else "MC"
    
    if challenge_val >= challenge_val * 0.8:
        status_color = "#66ff66"
        status_text = "달성"
    elif challenge_val >= challenge_val * 0.6:
        status_color = "#ffdc00"
        status_text = "진행중"
    else:
        status_color = "#ff6b6b"
        status_text = "미달"
    
    return f"""
    <div class="{css_class}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div><span style="color:#aaa; font-size:12px;">{title}</span></div>
            <div style="color:{status_color}; font-weight:bold;">{status_text}</div>
        </div>
        <div style="margin-top:10px; font-size:16px; font-weight:bold;">
            {format_display(challenge_val)} / {format_display(challenge_val * 1.2)}
        </div>
        <div style="margin-top:5px; font-size:12px; color:#aaa;">
            부족: {format_display(shortage_val)}
        </div>
    </div>
    """

def display_result(row):
    st.markdown("<p style='color:#fff;font-weight:600;margin-bottom:20px;'>💡 대리점 시상안을 보고 달성 시상금을 확인하세요</p>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # 기본 정보
        st.markdown(f"""
        <div class="info-box">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div><span style="color:#aaa; font-size:12px;">지점</span></div>
                <div style="color:#ffa500; font-weight:bold;">{row.get('지점명', 'N/A')}</div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div><span style="color:#aaa; font-size:12px;">매니저</span></div>
                <div style="color:#fff; font-weight:bold;">{row.get('매니저', 'N/A')}</div>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <div><span style="color:#aaa; font-size:12px;">설계사</span></div>
                <div style="color:#fff; font-weight:bold;">{row.get('설계사명', 'N/A')} ({row.get('현재대리점설계사조직코드', 'N/A')})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 누계 (3월만 노란색)
        st.markdown(f"""
        <div class="cumulative-box">
            <div style="color:#ffdc00; font-weight:bold; margin-bottom:5px;">3월 누계실적</div>
            <div style="font-size:24px; font-weight:bold; color:#ffdc00;">{format_display(row.get('3월누계', 0))}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 주차별 실적
        current_week = get_current_week()
        for week in range(1, 6):
            week_key = f"{'1주' if week == 1 else '2주' if week == 2 else '3주' if week == 3 else '4주' if week == 4 else '5주'}_실적"
            week_value = format_display(row.get(week_key, 0))
            
            highlight = "border-left: 5px solid #ffdc00;" if week == current_week else "border-left: 5px solid #66ccff;"
            highlight_color = "#ffdc00" if week == current_week else "#66ccff"
            
            st.markdown(f"""
            <div class="weekly-box" style="{highlight}">
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#aaa;">{week}주</span>
                    <span style="color:{highlight_color}; font-weight:bold;">{week_value}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 목표/부족
        current_week_target = format_display(row.get(f"{'1주' if current_week == 1 else '2주' if current_week == 2 else '3주' if current_week == 3 else '4주' if current_week == 4 else '5주'}_목표", 0))
        shortage = safe_float(row.get('부족', 0))
        
        st.markdown(f"""
        <div class="target-box">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span style="color:#aaa;">현주 목표</span>
                <span style="color:#ff6b6b; font-weight:bold;">{current_week_target}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="color:#aaa;">부족</span>
                <span style="color:#ff6b6b; font-weight:bold;">{format_display(shortage)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bridge (설계사 코드가 '7'로 시작하면 비인증)
        agent_code = str(row.get('현재대리점설계사조직코드', ''))
        is_authentic = not agent_code.startswith('7')
        
        if not is_authentic:
            st.markdown(f"""
            <div class="bridge-box">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="color:#aaa;">Bridge 목표</span>
                    <span style="color:#ff8c42; font-weight:bold;">{format_display(row.get('Bridge목표', 0))}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#aaa;">Bridge 실적</span>
                    <span style="color:#ff8c42; font-weight:bold;">{format_display(row.get('Bridge실적', 0))}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # MC
        st.markdown(render_mc_box(row.get('MC목표', 0), row.get('MC부족', 0), is_authentic=is_authentic, is_mc_plus=False), unsafe_allow_html=True)
        
        # MC PLUS+
        st.markdown(render_mc_box(row.get('MCPLUS목표', 0), row.get('MCPLUS부족', 0), is_authentic=is_authentic, is_mc_plus=True), unsafe_allow_html=True)
    
    with col_right:
        # 리플렛 이미지
        agency_name = row.get('대리점명', 'none')
        image_id = get_image_id_by_authentic_and_partner(is_authentic, False, agency_name)
        leaflet_img = load_leaflet_template_from_drive(image_id)
        
        if leaflet_img:
            st.image(leaflet_img, use_column_width=True)
            
            # 다운로드 버튼
            import io
            buf = io.BytesIO()
            leaflet_img.save(buf, format="PNG")
            buf.seek(0)
            
            st.download_button(
                label="📥 리플렛 다운로드",
                data=buf.getvalue(),
                file_name=f"{agency_name}_리플렛.png",
                mime="image/png"
            )

# ========== Initialize Session State ==========
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None

# ========== Main App ==========
logo = load_logo()
if logo:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(logo, width=80)
    with col_title:
        st.markdown("<h1 style='color:#ffa500; margin:0; padding-top:15px;'>메리츠 설계사 성과 조회</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='color:#ffa500;'>메리츠 설계사 성과 조회</h1>", unsafe_allow_html=True)

st.markdown("---")

# 데이터 로드
df = load_data_from_google_sheets()

# 지점명 정렬
df_sorted = df.sort_values(by='지점명', key=lambda x: x.apply(extract_branch_number))
branches = sorted(df['지점명'].unique(), key=extract_branch_number)
default_branch = "GA4-2지점" if "GA4-2지점" in branches else branches[0]

# 검색 입력
col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    selected_branch = st.selectbox("1️⃣ 지점명", branches, index=branches.index(default_branch) if default_branch in branches else 0)

with col2:
    manager_name = st.text_input("2️⃣ 매니저명", placeholder="예: 박메리", key="manager")

with col3:
    agent_name = st.text_input("3️⃣ 설계사명", placeholder="예: 홍길동", key="agent")

# 검색 버튼
search_col1, search_col2, search_col3 = st.columns([1, 1, 1])
with search_col2:
    search_clicked = st.button("🔍 검색", use_container_width=True)

# ========== 검색 로직 ==========
if search_clicked:
    if not manager_name or not agent_name:
        st.error("⚠️ 매니저명과 설계사명을 모두 입력해주세요.")
    else:
        # 필터링
        filtered = df[(df["지점명"].astype(str).str.strip() == selected_branch.strip()) &
                      (df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["설계사명"].astype(str).str.strip() == agent_name.strip())]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {selected_branch} / {manager_name} / {agent_name}")
            st.session_state.search_performed = False
        elif len(filtered) == 1:
            st.session_state.search_performed = True
            st.session_state.selected_row = filtered.iloc[0]
        else:
            # 동명이인 처리
            st.markdown("<p style='color:#fff;font-weight:600;margin-top:20px;font-size:14px;'>동명이인이 있습니다. 선택해주세요:</p>", unsafe_allow_html=True)
            for idx, (_, agent_row) in enumerate(filtered.iterrows()):
                agent_display = f"{agent_row.get('지사명','N/A')} - {agent_row.get('설계사명','N/A')} ({agent_row.get('현재대리점설계사조직코드','N/A')})"
                if st.button(agent_display, key=f"agent_{idx}", use_container_width=True):
                    st.session_state.search_performed = True
                    st.session_state.selected_row = agent_row

# ========== 결과 표시 ==========
if st.session_state.search_performed and st.session_state.selected_row is not None:
    row = st.session_state.selected_row
    display_result(row)
    
    # 초기화 버튼
    if st.button("🔄 초기화", use_container_width=False):
        st.session_state.search_performed = False
        st.session_state.selected_row = None
        st.rerun()
else:
    if not search_clicked:
        st.markdown("""
        <div style='text-align:center;margin-top:60px;padding:40px;background:linear-gradient(135deg,#1a1a1a 0%,#131313 100%);border-radius:10px;border-left:5px solid #555;'>
        <p style='color:#fff;font-weight:600;font-size:16px;'>🔒 매니저명과 설계사명을 입력하고 검색 버튼을 클릭하세요.</p>
        </div>
        """, unsafe_allow_html=True)
