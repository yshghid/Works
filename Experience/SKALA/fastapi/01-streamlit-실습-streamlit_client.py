import streamlit as st
import requests
import os

# 경로 설정
os.chdir("/Users/yshmbid/Documents/home/github/SQL")

st.title("Design 등록 클라이언트")

# 입력 박스
description = st.text_area("설계안 입력", "")

if st.button("등록하기"):
    if description.strip() == "":
        st.warning("설계안을 입력해주세요.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/register_design",
                json={"description": description}
            )
            if response.status_code == 200:
                st.success(response.json())
            else:
                st.error(response.json())
        except Exception as e:
            st.error(f"서버 연결 실패: {e}")