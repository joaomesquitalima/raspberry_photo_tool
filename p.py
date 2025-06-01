from difflib import get_close_matches

def placa_flex(entrada, lista_candidatos, threshold=0.5):
    matches = get_close_matches(entrada, lista_candidatos, n=1, cutoff=threshold)
    return matches[0] if matches else None

# Exemplo
entrada_ocr = 'ph29e0'
possiveis = ['phz9e61', 'abc123', 'teste456']
resultado = placa_flex(entrada_ocr, possiveis)

print("Melhor correspondência:", resultado)
