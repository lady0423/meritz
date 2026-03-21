if search_clicked:
    if not manager_name or not agent_code:
        st.error("⚠️ 매니저명과 설계사 코드를 모두 입력해주세요.")
    else:
        filtered = df[(df["매니저"].astype(str).str.strip() == manager_name.strip()) &
                      (df["현재대리점설계사조직코드"].astype(str).str.strip() == agent_code.strip())]
        
        if len(filtered) == 0:
            st.error(f"❌ 데이터를 찾을 수 없습니다: {manager_name} / {agent_code}")
        else:
            # ===== 디버깅 정보 출력 =====
            st.write("=== 디버깅 정보 ===")
            st.write(f"전체 컬럼명: {df.columns.tolist()}")
            
            row = filtered.iloc[0]
            st.write(f"어센틱구분: {row.get('어센틱구분', 'NOT FOUND')}")
            st.write(f"어센틱주차목표: {row.get('어센틱주차목표', 'NOT FOUND')}")
            st.write(f"어센틱주차부족최종: {row.get('어센틱주차부족최종', 'NOT FOUND')}")
            st.write(f"주차목표: {row.get('주차목표', 'NOT FOUND')}")
            st.write(f"주차부족: {row.get('주차부족', 'NOT FOUND')}")
            st.write(f"MC도전구간: {row.get('MC도전구간', 'NOT FOUND')}")
            st.write(f"MC부족최종: {row.get('MC부족최종', 'NOT FOUND')}")
            st.write(f"MC+구간: {row.get('MC+구간', 'NOT FOUND')}")
            st.write(f"MC+부족최종: {row.get('MC+부족최종', 'NOT FOUND')}")
            st.write(f"브릿지 도전구간: {row.get('브릿지 도전구간', 'NOT FOUND')}")
            st.write(f"브릿지 부족: {row.get('브릿지 부족', 'NOT FOUND')}")
