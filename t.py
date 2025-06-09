import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


imagem = cv2.imread("placa.jpg")


imagem = cv2.resize(imagem, (800, 600))


cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplica um blur para reduzir ruído
blur = cv2.GaussianBlur(cinza, (5, 5), 0)

# Binariza a imagem (letras escuras em fundo claro)
_, binarizada = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Encontra contornos
contornos, _ = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Percorre os contornos e tenta achar uma placa (aproximação por retângulo)
placa = None
for cnt in contornos:
    x, y, w, h = cv2.boundingRect(cnt)
    proporcao = w / float(h)
    if 2 < proporcao < 5 and w > 100 and h > 30:
        placa = imagem[y:y+h, x:x+w]
        cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)
        break



if placa is not None:
    # Prepara a imagem da placa para OCR
    placa_cinza = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)
    _, placa_bin = cv2.threshold(placa_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    texto = pytesseract.image_to_string(placa_bin, config='--psm 7')
    texto = [x for x in texto if x != " "]
    word = ''
    for i in texto:
        word += i 
    print("Texto da placa:", word.strip())

    # Mostrar a imagem final
    cv2.imshow("Placa", placa_bin)
else:
    print("Placa não encontrada.")

cv2.imshow("Imagem com Detecção", imagem)
cv2.imshow("Imagem com Detecção", binarizada)
cv2.waitKey(0)
cv2.destroyAllWindows()
