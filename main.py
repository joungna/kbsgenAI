import streamlit as st
from openai import OpenAI
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.image import imread
from io import BytesIO

from dotenv import load_dotenv
import os
from openai import OpenAI

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv('OPENAI_API_KEY')

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

st.title("이미지 생성 및 편집 도구")

# 메뉴 선택
menu = st.sidebar.selectbox("메뉴 선택", ["이미지 생성", "이미지 편집", "이미지 변형"])

if menu == "이미지 생성":
    st.header("이미지 생성")
    
    prompt = st.text_input("이미지 설명 입력:", "경복궁 야경")
    size = st.selectbox("이미지 크기 선택:", ["1024x1024", "1792x1024"])
    quality = st.selectbox("이미지 품질 선택:", ["standard", "hd"])
    
    if st.button("이미지 생성"):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )
        image_url = response.data[0].url
        st.image(image_url, caption="생성된 이미지")
        st.write(f"이미지 URL: {image_url}")

elif menu == "이미지 편집":
    st.header("이미지 편집")
    
    uploaded_file = st.file_uploader("원본 이미지 업로드", type=["png", "jpg", "jpeg"])
    mask_file = st.file_uploader("마스킹 이미지 업로드", type=["png"])
    edit_prompt = st.text_input("편집 설명 입력:", "add a Christmas tree")
    
    if st.button("이미지 편집"):
        if uploaded_file is not None and mask_file is not None:
            response = client.images.edit(
                model="dall-e-2",
                image=uploaded_file,
                mask=mask_file,
                prompt=edit_prompt,
                n=1,
                size="1024x1024",
            )
            edited_image_url = response.data[0].url
            st.image(edited_image_url, caption="편집된 이미지")
            st.write(f"편집된 이미지 URL: {edited_image_url}")
        else:
            st.error("원본 이미지와 마스킹 이미지를 모두 업로드해주세요.")

elif menu == "이미지 변형":
    st.header("이미지 변형")
    
    uploaded_file = st.file_uploader("기준 이미지 업로드", type=["png", "jpg", "jpeg"])
    number_of_variations = st.slider("생성할 변형 이미지 개수", 1, 5, 2)
    image_size = st.selectbox("이미지 크기 선택:", ["512x512", "1024x1024"])
    
    if st.button("이미지 변형"):
        if uploaded_file is not None:
            response = client.images.create_variation(
                image=uploaded_file,
                n=number_of_variations,
                size=image_size,
            )
            st.write("변형된 이미지들:")
            fig, ax = plt.subplots(1, number_of_variations, figsize=(8 * number_of_variations, 8))
            for i in range(number_of_variations):
                img_url = response.data[i].url
                response_img = urllib.request.urlopen(img_url)
                img = imread(BytesIO(response_img.read()))
                ax[i].imshow(img)
                ax[i].axis("off")
                ax[i].set_title(f"Variation {i+1}")
            st.pyplot(fig)
        else:
            st.error("기준 이미지를 업로드해주세요.")
