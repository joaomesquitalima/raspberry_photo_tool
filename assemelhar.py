import difflib

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

# Teste
alvo = "POX4G21_"
lista = ["QNA4B79",'QNA9079','DQE2H66']

mais_proxima = string_mais_semelhante(alvo, lista)
print(f"A string mais parecida com '{alvo}' é '{mais_proxima}'")
