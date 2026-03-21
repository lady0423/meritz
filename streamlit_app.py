# 검색 부분만 수정
if search_clicked:
    if not manager_name or not agent_code:
        st.error("⚠️ 매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        filtered = df[(df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {manager_name} / {agent_code}")
        else:
            row = filtered.iloc[0]
            
            # 컬럼명 공백 제거
            df.columns = df.columns.str.strip()
            row = filtered.iloc[0]
            
            agent_name = str(row["설계사명"]).strip()
            branch = str(row["지사명"]).strip()
            agency_name = str(row["대리점"]).strip()
            
            # Y열 어센틱구분 확인
            is_authentic = safe_float(row["어센틱구분"]) == 1
            
            # 파트너채널 확인
            is_partner_channel = "파트너채널" in branch
            
            col_left, col_right = st.columns([1.5, 1])
            
            with col_left:
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📋 기본 정보</h3>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='info-box'>
                <strong>설계사명:</strong> {agent_name}<br>
                <strong>지사:</strong> {branch}
                </div>
                """, unsafe_allow_html=True)
                
                cumulative = safe_float(row["3월실적"])
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📈 3월 누계 실적</h3>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='cumulative-box'>
                {format_currency(cumulative)}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>📅 주차별 실적</h3>", unsafe_allow_html=True)
                
                week_columns = ["1주차", "2주차", "3주차", "4주차", "5주차"]
                for idx, week_col in enumerate(week_columns, 1):
                    week_value = safe_float(row[week_col])
                    is_current = (idx == current_week)
                    
                    if is_current:
                        st.markdown(f"""
                        <div class='weekly-row current'>
                        <strong>{week_col}</strong> <span style='color: #ffcc00; font-size: 20px;'>⭐</span> <strong style='color: #ffcc00;'>{format_currency(week_value)}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class='weekly-row'>
                        <strong>{week_col}</strong> <strong style='color: #66cc66;'>{format_currency(week_value)}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                
                # ============ 핵심 수정 ============
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🎯 현재주차 목표</h3>", unsafe_allow_html=True)
                
                if is_authentic and not is_partner_channel:
                    # Y=1 어센틱
                    weekly_target = safe_float(row["어센틱주차목표"])
                    weekly_shortage = safe_float(row["어센틱주차부족최종"])
                else:
                    # Y=0 기타
                    weekly_target = safe_float(row["주차목표"])
                    weekly_shortage = safe_float(row["주차부족"])
                
                st.markdown(f"""
                <div class='target-box'>
                <strong>목표:</strong> {format_currency(weekly_target)}<br>
                <strong>부족금액:</strong> {format_currency(weekly_shortage)}
                </div>
                """, unsafe_allow_html=True)
                
                # 브릿지는 Y=0일 때만
                if not is_authentic:
                    st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🌉 브릿지 성과</h3>", unsafe_allow_html=True)
                    bridge_achievement = safe_float(row["브릿지 실적"])
                    bridge_target = safe_float(row["브릿지 도전구간"])
                    bridge_shortage = safe_float(row["브릿지 부족"])
                    
                    st.markdown(f"""
                    <div class='bridge-box'>
                    <strong>진척:</strong> {format_currency(bridge_achievement)}<br>
                    <strong>목표:</strong> {format_currency(bridge_target)}<br>
                    <strong>부족금액:</strong> {format_currency(bridge_shortage)}
                    </div>
                    """, unsafe_allow_html=True)
                
                # MC와 MC+
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>💰 성과</h3>", unsafe_allow_html=True)
                
                if is_authentic and not is_partner_channel:
                    # Y=1: MC + MC+
                    mc_challenge = safe_float(row["MC도전구간"])
                    mc_shortage = safe_float(row["MC부족최종"])
                    
                    render_mc_box(mc_challenge, mc_shortage, mc_shortage, is_mc_plus=False)
                    
                    mc_plus_challenge = safe_float(row["MC+구간"])
                    mc_plus_shortage = safe_float(row["MC+부족최종"])
                    
                    render_mc_box(mc_plus_challenge, mc_plus_shortage, mc_plus_shortage, is_mc_plus=True)
                else:
                    # Y=0: MC+만
                    mc_plus_challenge = safe_float(row["MC+구간"])
                    mc_plus_shortage = safe_float(row["MC+부족최종"])
                    
                    render_mc_box(mc_plus_challenge, mc_plus_shortage, mc_plus_shortage, is_mc_plus=True)
            
            with col_right:
                st.markdown("<h3 style='color: #ff8a99; font-size: 18px;'>🎁 대리점 리플렛</h3>", unsafe_allow_html=True)
                image_id = get_image_id_by_authentic_and_partner(is_authentic, is_partner_channel, agency_name)
                image = load_leaflet_template_from_drive(image_id)
                
                if image:
                    st.image(image, use_container_width=True)
                    
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
            
            st.markdown("<hr style='border: 1px solid #c41e3a; margin: 30px 0;'>", unsafe_allow_html=True)
            
            col_reset = st.columns(1)[0]
            with col_reset:
                if st.button("🔄 초기화", use_container_width=True):
                    st.rerun()
