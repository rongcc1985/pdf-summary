import streamlit as st
from pypdf import PdfReader
import requests

import os
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

st.title("PDF 200字总结工具")

uploaded_file = st.file_uploader("上传 PDF 文件", type=["pdf"])

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    if st.button("生成200字总结"):
        prompt = f"""
请阅读以下内容，并生成一段不超过200字的中文摘要：
{text}
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        summary = result["choices"][0]["message"]["content"]
        st.subheader("摘要结果：")
        st.write(summary)

