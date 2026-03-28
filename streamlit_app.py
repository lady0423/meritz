import streamlit as st
import pandas as pd
import datetime
import pytz
from PIL import Image
import gdown
import tempfile
import os
import streamlit.components.v1 as components

GOOGLE_SHEET_ID = "1NSm_gy0a_QbWXquI2efdM93BjBuHn_sYLpU0NybL5_8"

LEAFLET_TEMPLATE_IDS = {
    "메가": "1N0Aq60bQnPjg7o4GFv19lbqv3pUc57H8",
    "토스": "1Xn_hB6Xl6fojhcgyF2zVlpYtyQst5ann",
    "지금융": "1b4BIQeFKooVdC-pt0z87gVZSuYTzpY8l",
    "엠금융": "1ukqgpfA4VwELcaybWN_8MGWc8ufbLwAC",
    "스카이블루에셋": "1xPOw05Kjk0hNIeIIJ1iJE4NFVv1_yvU5",
    "유퍼스트": "1X7jZLVwEYIScZqEp_9O-UHX1kK2rPhQ3",
    "케이지에이에셋": "1faWuhu3haJ3-bjkhK3Xwlp5x60Yj063W",
    "피플라이프": "1oShjwYdKsjUvVkAMUmxAbgrmTA_v9Wna",
    "더금융": "1DeUpP_czQzEpa2CTiWyvcg_42e0FT-_Y",
    "더좋은보험": "1OLsK7oilx3OacZSw8f1VZP3pKBvYsLRj",
    "프라임에셋": "1iZie57BZYUNguiiuympKd4wsg_kkZxVt",
    "에이플러스": "1KYkiPglCCgKZ59HGSebkpKjPanr-os1b",
    "지에이코리아": "1xsc5JVGxyercM0553s2Cdx5vw8PbjccS",
    "메타리치": "13MXbTMcaq0E9ugf9V4Yh1wGfNcavQSvX",
    "글로벌금융": "1rLX4jeoFvzgQCEEBaMLYWp5eSs_XdNNE",
    "인카금융": "15l_dvr73h5RwdrEEi2GP4lbVReMyj8KJ",
    "아너스": "1DrMIR4hDRcXuI3l6Ue-l4aCfP0aEP0JS",
    "굿리치": "1xF8N3LCMECplAurB9sVpmlzzmUdcHh2_",
    "신한금융": "1XAAncz-bWC4scblwtO7sLxsprqpcmu7_",
    "어센틱": "1pCtQjJQ_Vb_FWxhaicGBT0GWHwiVJJ1-",
    "none": "19ZnaS2s4X8JKv27NW9FFuMUVh32i3hc0"
}

PASSWORD = "2233"
st.set_page_config(page_title="메리츠 실적현황", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f7fafc; }
    .stTextInput>div>div>input { border-radius: 8px; border: 2px solid #cbd5e0; padding: 10px; font-size: 16px; }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 8px;
        padding: 12px 24px; font-size: 16px; font-weight: 600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: all 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 12px; margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); color: white;
    }
    .mc-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px; border-radius: 10px; margin: 8px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1); color: white; font-size: 14px;
    }
    .bridge-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px; border-radius: 10px; margin: 8px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1); color: white; font-size: 14px;
    }
    .weekly-box {
        background: white; padding: 12px; border-radius: 8px;
        margin: 6px 0; border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .current-week { background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); font-weight: 700; }
</style>
""", unsafe_allow_html=True)

def safe_float(v):
    if pd.isna(v) or v in ["", None]:
        return 0.0
    try:
        s = str(v).strip().replace(",", "")
        if "만원" in s:
            return float(s.replace("만원", "")) * 10000
        return float(s)
    except:
        return 0.0

def format_display(v):
    s = str(v).strip()
    if s in ["", "nan"]:
        return "₩ 0"
    try:
        if "만원" in s:
            num = float(s.replace("만원", "")) * 10000
            return f"₩ {num:,.0f}"
        return f"₩ {float(s.replace(',', '')):,.0f}"
    except:
        return s

def normalize_phone_number(p):
    if pd.isna(p):
        return ""
    return str(p).replace("-", "").replace(" ", "").strip()

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

@st.cache_data(ttl=300)
def load_contact_data_from_google_sheets():
    url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid=363789500"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"전화번호 데이터 로드 실패: {e}")
        return None

def render_mc_box(mc_challenge, mc_shortage, is_authentic=False, is_mc_plus=False, mc_target_value=1):
    if not is_mc_plus and (mc_target_value == 0 or mc_target_value == 2):
        st.markdown(f"""
        <div class='mc-box'>
        <strong>도전구간 →</strong> 대상아님<br>
        <strong>부족금액 →</strong> ₩ 0<br>
        <strong>상태 →</strong> <span style='color: #ffd700; font-weight: 700;'>이번달 20만원 도전</span>
        </div>
        """, unsafe_allow_html=True)
        return

    challenge_val = safe_float(mc_challenge)
    shortage_val = safe_float(mc_shortage)

    if shortage_val <= 0:
        if is_mc_plus:
            status_text = "<span style='color: #ffd700; font-weight: 700;'>🎉 MC+ 달성!</span>"
        else:
            status_text = "<span style='color: #90ee90; font-weight: 700;'>🎉 MC 달성!</span>"
    else:
        status_msg = "MC+ 도전 중..." if is_mc_plus else ("어센틱 도전 중..." if is_authentic else "브릿지 도전 중...")
        status_text = f"<span style='color: #ffeb3b; font-weight: 700;'>{status_msg}</span>"

    st.markdown(f"""
    <div class='{"mc-box" if not is_mc_plus else "bridge-box"}'>
    <strong>도전구간 →</strong> {format_display(challenge_val)}<br>
    <strong>부족금액 →</strong> {format_display(shortage_val)}<br>
    <strong>상태 →</strong> {status_text}
    </div>
    """, unsafe_allow_html=True)

def download_leaflet_template(template_id, dest_path):
    url = f"https://drive.google.com/uc?id={template_id}"
    try:
        gdown.download(url, dest_path, quiet=False)
        return True
    except Exception as e:
        st.error(f"리플렛 다운로드 실패: {e}")
        return False

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'show_duplicates' not in st.session_state:
    st.session_state.show_duplicates = False
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
if 'contact_search_performed' not in st.session_state:
    st.session_state.contact_search_performed = False
if 'contact_selected_row' not in st.session_state:
    st.session_state.contact_selected_row = None
if 'contact_show_duplicates' not in st.session_state:
    st.session_state.contact_show_duplicates = False
if 'contact_filtered_data' not in st.session_state:
    st.session_state.contact_filtered_data = None

if not st.session_state.authenticated:
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        try:
            logo = Image.open("logo.png")
            st.image(logo, width=120)
        except:
            st.markdown("### 🏢")
    with col_title:
        st.markdown("<h1 style='color: #2d3748; margin-top: 20px;'>메리츠 실적현황 시스템</h1>", unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
            <h2 style='text-align: center; color: #667eea; margin-bottom: 30px;'>🔐 로그인</h2>
        """, unsafe_allow_html=True)

        password_input = st.text_input(
            "비밀번호를 입력하세요",
            type="password",
            placeholder="비밀번호",
            label_visibility="collapsed"
        )

        if st.button("로그인", use_container_width=True):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ 비밀번호가 올바르지 않습니다.")

        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=80)
    except:
        st.markdown("### 🏢")
with col_title:
    st.markdown("<h1 style='color: #2d3748;'>메리츠 실적현황 시스템</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 실적조회", "📞 전화번호 조회"])

with tab1:
    df = load_data_from_google_sheets()
    if df is None:
        st.error("❌ 데이터를 불러올 수 없습니다.")
        st.stop()

    seoul_tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(seoul_tz)
    
    if now.day <= 7:
        current_week = 1
    elif now.day <= 14:
        current_week = 2
    elif now.day <= 21:
        current_week = 3
    elif now.day <= 28:
        current_week = 4
    else:
        current_week = 5

    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "검색",
            placeholder="설계사명 또는 코드를 입력하세요 (예: 홍길동, A12345)",
            label_visibility="collapsed",
            key="search_input"
        )
    with col2:
        search_clicked = st.button("🔍 검색", use_container_width=True, key="search_button")

    if search_clicked and search_query.strip():
        query = search_query.strip()
        filtered = df[
            df['설계사명'].astype(str).str.contains(query, case=False, na=False) |
            df['설계사코드'].astype(str).str.contains(query, case=False, na=False)
        ]

        if len(filtered) == 0:
            st.warning("⚠️ 검색 결과가 없습니다.")
            st.session_state.search_performed = False
            st.session_state.selected_row = None
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
        elif len(filtered) == 1:
            st.session_state.selected_row = filtered.iloc[0]
            st.session_state.search_performed = True
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
        else:
            st.session_state.show_duplicates = True
            st.session_state.filtered_data = filtered
            st.session_state.search_performed = False
            st.session_state.selected_row = None

    if st.session_state.show_duplicates and st.session_state.filtered_data is not None:
        st.markdown("<p style='color: #4a5568; font-weight: 600; margin-top: 12px; font-size: 14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>", unsafe_allow_html=True)
        for idx, (row_idx, result_row) in enumerate(st.session_state.filtered_data.iterrows()):
            office_name = str(result_row.get('지점명', 'N/A')).strip()
            branch_name = str(result_row.get('지사', 'N/A')).strip()
            agent_name = str(result_row.get('설계사명', 'N/A')).strip()
            display_text = f"{office_name} | {branch_name} | {agent_name}"

            if st.button(display_text, key=f"select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.selected_row = result_row
                st.session_state.search_performed = True
                st.session_state.show_duplicates = False
                st.session_state.filtered_data = None
                st.rerun()

    if st.session_state.search_performed and st.session_state.selected_row is not None:
        row = st.session_state.selected_row
        agency_branch = str(row.get('지사', 'N/A')).strip()
        agent_name_display = str(row.get('설계사명', 'N/A')).strip()
        agent_code = str(row.get('설계사코드', 'N/A')).strip()
        cumulative = row["누계"]

        st.markdown(f"""
        <div class='info-box'>
        <h2 style='margin: 0; color: white;'>👤 {agent_name_display}</h2>
        <p style='margin: 5px 0 0 0; font-size: 16px;'>{agency_branch} | 코드: {agent_code}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #4a5568; margin-top: 20px;'>📈 3월 누계 실적</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-box'><h2 style='margin:0; color: white;'>{format_display(cumulative)}</h2></div>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("<h3 style='color: #4a5568;'>📅 주차별 실적</h3>", unsafe_allow_html=True)
            week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
            for week_num, week_col in enumerate(week_columns, 1):
                week_value = row[week_col]
                current_mark = " ⭐" if week_num == current_week else ""
                box_class = "weekly-box current-week" if week_num == current_week else "weekly-box"
                st.markdown(f"""
                <div class='{box_class}'>
                <strong>{week_col}{current_mark}</strong> → {format_display(week_value)}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<h3 style='color: #48bb78; margin-top: 20px;'>⭐ 현재주차 목표</h3>", unsafe_allow_html=True)

            try:
                is_authentic = safe_float(df.iloc[row.name, 26]) == 1
            except:
                is_authentic = False

            if is_authentic:
                weekly_target = row.get("어센틱주차목표", "0")
                weekly_shortage = row.get("어센틱주차부족", "0")
            else:
                weekly_target = row.get("주차목표", "0")
                weekly_shortage = row.get("주차부족최종", "0")

            target_val = safe_float(weekly_target)
            shortage_val = safe_float(weekly_shortage)

            if shortage_val <= 0:
                status_text = "<span style='color: #38a169; font-weight: 700;'>✅ 목표 달성!</span>"
            else:
                status_text = "<span style='color: #ed8936; font-weight: 700;'>📌 목표 도전 중</span>"

            st.markdown(f"""
            <div class='info-box'>
            <strong>목표 →</strong> {format_display(target_val)}<br>
            <strong>부족금액 →</strong> {format_display(shortage_val)}<br>
            <strong>상태 →</strong> {status_text}
            </div>
            """, unsafe_allow_html=True)

            if is_authentic:
                st.markdown("<h3 style='color: #e53e3e;'>💰 MC 성과</h3>", unsafe_allow_html=True)
                mc_challenge = row.get("MC도전구간", 0)
                mc_shortage = row.get("MC부족최종", 0)
                try:
                    mc_target_value = safe_float(df.iloc[row.name, 27])
                except:
                    mc_target_value = 1
                render_mc_box(mc_challenge, mc_shortage, is_authentic=True, mc_target_value=mc_target_value)
            else:
                st.markdown("<h3 style='color: #3182ce;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
                bridge_target = row["브릿지 도전구간"]
                bridge_shortage = row["브릿지부족최종"]
                render_mc_box(bridge_target, bridge_shortage, is_authentic=False)

            st.markdown("<h3 style='color: #805ad5;'>💰 MC PLUS+ 성과</h3>", unsafe_allow_html=True)
            mc_plus_challenge = row["MC+구간"]
            mc_plus_shortage = row["MC+부족최종"]
            render_mc_box(mc_plus_challenge, mc_plus_shortage, is_authentic=is_authentic, is_mc_plus=True)

            # 📱 카카오톡 발송 섹션
            st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #4a5568;'>📱 카카오톡 발송</h3>", unsafe_allow_html=True)

            # MC 또는 브릿지 정보 생성
            if is_authentic:
                try:
                    mc_target_value = safe_float(df.iloc[row.name, 27])
                except:
                    mc_target_value = 1
                if mc_target_value in (0, 2):
                    mc_info = """💰 MC 성과
 • 도전구간: 대상아님
 • 부족금액: ₩ 0
 • 상태: 이번달 20만원 도전"""
                else:
                    mc_challenge = row.get("MC도전구간", 0)
                    mc_shortage = row.get("MC부족최종", 0)
                    mc_info = f"""💰 MC 성과
 • 도전구간: {format_display(mc_challenge)}
 • 부족금액: {format_display(mc_shortage)}"""
            else:
                bridge_target = row["브릿지 도전구간"]
                bridge_shortage = row["브릿지부족최종"]
                mc_info = f"""🌉 브릿지 성과
 • 목표: {format_display(bridge_target)}
 • 부족금액: {format_display(bridge_shortage)}"""

            # 주차별 실적 텍스트
            week_text = ""
            for idx, week_col in enumerate(["1주차","2주차","3주차","4주차","5주차"], 1):
                if idx > current_week:
                    break
                week_value = row[week_col]
                mark = " ⭐" if idx == current_week else ""
                week_text += f" • {week_col}: {format_display(week_value)}{mark}\n"

            # 현재 주차 목표
            if is_authentic:
                weekly_target = row.get("어센틱주차목표", "0")
                weekly_shortage = row.get("어센틱주차부족", "0")
            else:
                weekly_target = row.get("주차목표", "0")
                weekly_shortage = row.get("주차부족최종", "0")

            # 카카오톡 메시지 생성
            kakao_message = f"""📊메리츠 3월 실적 현황
{agency_branch} {agent_name_display}팀장님!

📈 3월 누계 실적
 {format_display(cumulative)}

📅 주차별 실적
{week_text}
⭐ 현재주차 목표
 • 목표: {format_display(weekly_target)}
 • 부족금액: {format_display(weekly_shortage)}

{mc_info}

💰 MC PLUS+ 성과
 • 도전구간: {format_display(mc_plus_challenge)}
 • 부족금액: {format_display(mc_plus_shortage)}

💡 시상관련 궁금하신게 있다면 문의주세요~
이번주도 화이팅입니다!"""

            # 미리보기
            st.text_area("메시지 미리보기", value=kakao_message, height=350, label_visibility="collapsed", key="kakao_preview")

            # 복사하기 버튼 (JavaScript 기반)
            col_copy1, col_copy2 = st.columns([1, 1])
            
            with col_copy1:
                kakao_message_escaped = kakao_message.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"')
                copy_button_html = f"""
                <script>
                function copyKakaoMessage() {{
                    const text = `{kakao_message_escaped}`;
                    navigator.clipboard.writeText(text).then(
                        function() {{
                            alert('✅ 클립보드에 복사되었습니다!\\n카톡에 붙여넣기(Ctrl+V) 하세요!');
                        }},
                        function() {{
                            alert('❌ 복사에 실패했습니다. 다시 시도해주세요.');
                        }}
                    );
                }}
                </script>
                <button onclick="copyKakaoMessage()" style="width: 100%; padding: 10px 20px; background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%); color: white; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    📋 메시지 복사하기
                </button>
                """
                components.html(copy_button_html, height=60)

            with col_copy2:
                st.download_button(
                    label="💾 텍스트 파일로 저장",
                    data=kakao_message,
                    file_name=f"{agent_name_display}_{agency_branch}_실적현황.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        with col_right:
            st.markdown("<h3 style='color: #4a5568;'>📄 리플렛 다운로드</h3>", unsafe_allow_html=True)

            leaflet_agencies = ["메가", "토스", "지금융", "엠금융", "스카이블루에셋", "유퍼스트", 
                              "케이지에이에셋", "피플라이프", "더금융", "더좋은보험", "프라임에셋",
                              "에이플러스", "지에이코리아", "메타리치", "글로벌금융", "인카금융",
                              "아너스", "굿리치", "신한금융", "어센틱"]

            agency_name_raw = str(row.get('지점명', '')).strip()
            matched_template = "none"

            for keyword in leaflet_agencies:
                if keyword in agency_name_raw:
                    matched_template = keyword
                    break

            selected_template = st.selectbox(
                "리플렛 템플릿 선택",
                options=["자동 감지"] + leaflet_agencies + ["기본 템플릿"],
                index=0,
                key="leaflet_select"
            )

            if selected_template == "자동 감지":
                final_template = matched_template
            elif selected_template == "기본 템플릿":
                final_template = "none"
            else:
                final_template = selected_template

            template_id = LEAFLET_TEMPLATE_IDS.get(final_template, LEAFLET_TEMPLATE_IDS["none"])

            st.info(f"🎯 선택된 템플릿: **{final_template}**")

            if st.button("📥 리플렛 다운로드", use_container_width=True, key="download_leaflet"):
                temp_dir = tempfile.gettempdir()
                dest_file = os.path.join(temp_dir, f"leaflet_{final_template}.jpg")

                with st.spinner("리플렛 다운로드 중..."):
                    if download_leaflet_template(template_id, dest_file):
                        try:
                            with open(dest_file, "rb") as file:
                                st.download_button(
                                    label=f"💾 {final_template} 리플렛 저장",
                                    data=file,
                                    file_name=f"리플렛_{final_template}_{agent_name_display}.jpg",
                                    mime="image/jpeg",
                                    use_container_width=True
                                )
                            st.success("✅ 리플렛 다운로드 완료!")
                        except Exception as e:
                            st.error(f"❌ 파일 읽기 실패: {e}")
                    else:
                        st.error("❌ 리플렛 다운로드에 실패했습니다.")

        st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 20px 0;'>", unsafe_allow_html=True)

        if st.button("🔄 초기화", use_container_width=True, key="reset_search"):
            st.session_state.search_performed = False
            st.session_state.selected_row = None
            st.session_state.show_duplicates = False
            st.session_state.filtered_data = None
            st.rerun()

with tab2:
    st.markdown("<h2 style='color: #4a5568;'>📞 전화번호 조회</h2>", unsafe_allow_html=True)

    contact_df = load_contact_data_from_google_sheets()
    performance_df = load_data_from_google_sheets()

    if contact_df is None or performance_df is None:
        st.error("❌ 데이터를 불러올 수 없습니다.")
        st.stop()

    contact_df['휴대전화_normalized'] = contact_df['휴대전화'].apply(normalize_phone_number)

    col1, col2 = st.columns([3, 1])
    with col1:
        contact_search = st.text_input(
            "검색",
            placeholder="예: 01012345678, 1234567, 123-4567, 홍길동",
            label_visibility="collapsed",
            key="contact_search"
        )
    with col2:
        contact_search_clicked = st.button("🔍 검색", use_container_width=True, key="contact_search_btn")

    if contact_search_clicked and contact_search.strip():
        query = contact_search.strip()
        normalized_query = normalize_phone_number(query)

        if normalized_query.isdigit():
            filtered_contacts = contact_df[
                contact_df['휴대전화_normalized'].str.contains(normalized_query, na=False)
            ]
        else:
            filtered_contacts = contact_df[
                contact_df['설계사명'].astype(str).str.contains(query, case=False, na=False)
            ]

        if len(filtered_contacts) == 0:
            st.warning("⚠️ 검색 결과가 없습니다.")
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
        elif len(filtered_contacts) == 1:
            st.session_state.contact_selected_row = filtered_contacts.iloc[0]
            st.session_state.contact_search_performed = True
            st.session_state.contact_show_duplicates = False
            st.session_state.contact_filtered_data = None
        else:
            st.session_state.contact_show_duplicates = True
            st.session_state.contact_filtered_data = filtered_contacts
            st.session_state.contact_search_performed = False
            st.session_state.contact_selected_row = None

    if st.session_state.contact_show_duplicates and st.session_state.contact_filtered_data is not None:
        st.markdown("<p style='color: #4a5568; font-weight: 600; margin-top: 12px; font-size: 14px;'>검색 결과가 여러 개입니다. 선택해주세요:</p>", unsafe_allow_html=True)
        
        # 지점 순서대로 정렬
        sorted_contacts = st.session_state.contact_filtered_data.sort_values(by='지점', ascending=True)
        
        for idx, (row_idx, contact_row) in enumerate(sorted_contacts.iterrows()):
            contact_office = str(contact_row.get('지점', 'N/A')).strip()
            contact_branch = str(contact_row.get('지사', 'N/A')).strip()
            contact_name = str(contact_row.get('설계사명', 'N/A')).strip()
            contact_display = f"{contact_office} | {contact_branch} | {contact_name}"

            if st.button(contact_display, key=f"contact_select_{row_idx}_{idx}", use_container_width=True):
                st.session_state.contact_selected_row = contact_row
                st.session_state.contact_search_performed = True
                st.session_state.contact_show_duplicates = False
                st.session_state.contact_filtered_data = None
                st.rerun()

    if st.session_state.contact_search_performed and st.session_state.contact_selected_row is not None:
        contact_row = st.session_state.contact_selected_row

        contact_office = str(contact_row.get('지점', 'N/A')).strip()
        contact_branch = str(contact_row.get('지사', 'N/A')).strip()
        contact_name = str(contact_row.get('설계사명', 'N/A')).strip()
        contact_phone = str(contact_row.get('휴대전화', 'N/A')).strip()
        contact_code = str(contact_row.get('코드', 'N/A')).strip()

        st.markdown(f"""
        <div class='info-box'>
        <h2 style='margin: 0; color: white;'>👤 {contact_name}</h2>
        <p style='margin: 5px 0 0 0; font-size: 16px;'>{contact_office} | {contact_branch}</p>
        <p style='margin: 5px 0 0 0; font-size: 16px;'>코드: {contact_code}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #4a5568; margin-top: 20px;'>📱 연락처 정보</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <p style='font-size: 18px; margin: 0;'><strong>휴대전화:</strong> {contact_phone}</p>
        </div>
        """, unsafe_allow_html=True)

        performance_match = performance_df[performance_df['설계사코드'].astype(str) == contact_code]

        if not performance_match.empty:
            perf_row = performance_match.iloc[0]
            cumulative_perf = perf_row["누계"]

            st.markdown("<h3 style='color: #4a5568; margin-top: 20px;'>📊 실적 정보</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
            <h3 style='margin: 0; color: white;'>3월 누계 실적</h3>
            <h2 style='margin: 5px 0 0 0; color: white;'>{format_display(cumulative_perf)}</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("📊 실적 정보를 찾을 수 없습니다.")

        vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact_name}
TEL;TYPE=CELL:{contact_phone}
ORG:{contact_office};{contact_branch}
NOTE:코드: {contact_code}
END:VCARD"""

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📇 연락처 저장 (vCard)",
                data=vcard_content,
                file_name=f"{contact_name}_연락처.vcf",
                mime="text/vcard",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 초기화", use_container_width=True, key="reset_contact"):
                st.session_state.contact_search_performed = False
                st.session_state.contact_selected_row = None
                st.session_state.contact_show_duplicates = False
                st.session_state.contact_filtered_data = None
                st.rerun()
