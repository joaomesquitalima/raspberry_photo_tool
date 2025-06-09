import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import difflib

def string_mais_semelhante(alvo, lista, limite=0.6):
    melhor = None
    melhor_score = 0
    for s in lista:
        score = difflib.SequenceMatcher(None, alvo, s).ratio()
        if score > melhor_score:
            melhor = s
            melhor_score = score
    if melhor_score >= limite:
        return melhor
    return None
# Configura o caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("Leitor de Placas com OCR")

uploaded_file = st.file_uploader("Envie uma imagem da placa", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Abre a imagem com PIL e converte para array OpenCV (BGR)
    image_pil = Image.open(uploaded_file).convert("RGB")
    imagem = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # Redimensiona para 800x600
    imagem = cv2.resize(imagem, (800, 600))

    # Conversão para tons de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplica blur para reduzir ruído
    blur = cv2.GaussianBlur(cinza, (5, 5), 0)

    # Binarização com Otsu
    _, binarizada = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Encontra contornos
    contornos, _ = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    placa = None
    for cnt in contornos:
        x, y, w, h = cv2.boundingRect(cnt)
        proporcao = w / float(h)
        if 2 < proporcao < 5 and w > 100 and h > 30:
            placa = imagem[y:y + h, x:x + w]
            cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    if placa is not None:
        # Prepara a imagem da placa para OCR
        placa_cinza = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)
        _, placa_bin = cv2.threshold(placa_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR
        texto = pytesseract.image_to_string(placa_bin, config='--psm 7')
        texto = [x for x in texto if x != " " and x != "."]
        word = ''.join(texto)

        st.subheader("Texto da placa:")
        st.success(word.strip())

        lista = ["QNA4B79",'QNA9079','DQE2H66']

        mais_proxima = string_mais_semelhante(word, lista)
        print("Texto da placa:", word.strip())
        print(mais_proxima)
        st.text(mais_proxima)

        st.image(placa_bin, caption="Placa", channels="GRAY")
    else:
        st.warning("Placa não encontrada.")

    # Exibição final
    # st.image(imagem, caption="Imagem com Detecção", channels="BGR", width=600)
    # st.image(binarizada, caption="Imagem Binarizada", channels="GRAY", width=600)
