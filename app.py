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

st.title("OCR com EasyOCR")

reader = easyocr.Reader(['pt', 'en'])

uploaded_file = st.file_uploader("Envie uma imagem", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    melhor = preprocess_image(image)
    st.image(image, caption='Imagem enviada', use_column_width=True)

    with st.spinner("Lendo texto..."):
        image_np = np.array(melhor)
        results = reader.readtext(image_np)

    st.subheader("Texto extraído:")
    placas = []
    for bbox, text, prob in results:
                
        clean_text = text.strip().replace(" ", "").upper()
        
        print(text)
        # if re.match(r'^[A-Z]{3}\d{1}[A-Z0-9]{1}\d{2}$', clean_text) or re.match(r'^[A-Z]{3}-?\d{4}$', clean_text):
        #     print(f"🔹 Placa: {text} (confiança: {prob:.2f})")
        if len(text) > 4:
            placas.append((text, prob))

    if placas:
        entrada_ocr, prob = placas[0]
        print("texto",entrada_ocr)
        possiveis = ['phz9e61', 'phe3129', 'teste456']
        resultado = placa_flex(entrada_ocr, possiveis)
        st.write(f"🔹 {resultado} (confiança: {prob:.2f})")

        info_ficticia = {
            "Placa": resultado,
            "Nome": "Erodilson Oliveira",
            "RA": "123456",
            "Veículo": "Chevrolet Onix",
            "Cor": "Azul"
        }

        st.subheader("Resultado da consulta:")
        for chave, valor in info_ficticia.items():
            st.write(f"**{chave}**: {valor}")
    else:
        st.warning("Nenhum texto relevante foi encontrado na imagem.")
