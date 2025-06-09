def levenshtein_dist(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # deleção
                                   dp[i][j-1],    # inserção
                                   dp[i-1][j-1])  # substituição
    return dp[m][n]

def placas_com_levenshtein(alvo, lista, max_dist=1):
    candidatas = []
    for placa in lista:
        dist = levenshtein_dist(alvo, placa)
        if dist <= max_dist:
            candidatas.append((placa, dist))
    # Ordena por distância crescente (mais parecido primeiro)
    candidatas.sort(key=lambda x: x[1])
    return candidatas

alvo = "QNAGB79"
lista = ["QNA4B79", "QNA9B79", "QNAGB78", "XYZ1234"]

resultado = placas_com_levenshtein(alvo, lista)
for placa, dist in resultado:
    print(f"{placa} -> distância: {dist}")
