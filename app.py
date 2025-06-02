import streamlit as st
from PIL import Image
import easyocr
import numpy as np
from difflib import get_close_matches
import cv2
import re

def placa_flex(entrada, lista_candidatos, threshold=0.2):
    matches = get_close_matches(entrada, lista_candidatos, n=1, cutoff=threshold)
    return matches[0] if matches else None

def preprocess_image(pil_image):
    image_np = np.array(pil_image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    equalized = cv2.equalizeHist(gray)
    filtered = cv2.bilateralFilter(equalized, 11, 17, 17)
    return filtered

st.set_page_config(layout="wide")
st.title("🚗 OCR de Placas - Portaria Inteligente")

reader = easyocr.Reader(['pt', 'en'])

uploaded_file = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    melhor = preprocess_image(image)

    with st.spinner("🔍 Lendo texto da imagem..."):
        image_np = np.array(melhor)
        results = reader.readtext(image_np)

    placas = []
    for bbox, text, prob in results:
        clean_text = text.strip().replace(" ", "").upper()
        if len(text) > 4:
            placas.append((text, prob))

    if placas:
        entrada_ocr, prob = placas[0]
        possiveis = ['phz9e61', 'phe3129', 'teste456']
        resultado = placa_flex(entrada_ocr, possiveis)

        # 👉 Duas colunas: esquerda (imagem e OCR), direita (informações do colaborador)
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption='Imagem enviada', use_column_width=True)
            st.markdown(f"<p style='font-size:28px;'><strong>🔹 Placa detectada:</strong> {resultado} <br><strong>Confiança:</strong> {prob:.2f}</p>", unsafe_allow_html=True)

        with col2:

            st.markdown(
        """
        <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; text-align: center;'>
            <h2>👤 Informações do Colaborador</h2>
            <p style='font-size: 22px;'><strong>Placa:</strong> """ + resultado + """</p>
            <p style='font-size: 22px;'><strong>Nome:</strong> Erodilson Oliveira</p>
            <p style='font-size: 22px;'><strong>RA:</strong> 123456</p>
            <p style='font-size: 22px;'><strong>Veículo:</strong> Chevrolet Onix</p>
            <p style='font-size: 22px;'><strong>Cor:</strong> Azul</p>
        </div>
        """,
        unsafe_allow_html=True)

            
    else:
        st.warning("Nenhum texto relevante foi encontrado na imagem.")
