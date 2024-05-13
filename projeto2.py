"""
2º Projeto

Nome: David Antunes
Número de aluno: 107061
Contacto: david.f.antunes@tecnico.ulisboa.pt
"""


def cria_gerador(b, s):
    """
    int x int ---> gerador
    Recebe um inteiro correspondente ao número de bits e outro correspondente à seed ou estado inicial e devolve o
    gerador correspondente.
    """
    if not isinstance(b, int) or b not in (32, 64) or not isinstance(s, int) or s < 1 or s > 2 ** b:  # verifica se o
        # número de bits é 32 ou 64 e se a seed não ultrapassa o valor máximo para o respetivo número de bits
        raise ValueError("cria_gerador: argumentos invalidos")
    return {"bits": b, "seed": s}


def cria_copia_gerador(g):
    """
    gerador ---> gerador
    Recebe um gerador e devolve uma cópia nova do gerador.
    """
    if not isinstance(g, dict) or len(g) != 2 or g["bits"] not in (32, 64) or not isinstance(g["bits"], int):
        raise ValueError("cria_gerador: argumentos invalidos")
    if not isinstance(g["seed"], int) or g["seed"] < 1 or g["seed"] > 2 ** g["bits"]:
        raise ValueError("cria_gerador: argumentos invalidos")
    return g.copy()


def obtem_estado(g):
    """
    gerador ---> int
    Recebe um gerador e devolve o seu estado atual sem o alterar.
    """
    return g["seed"]


def define_estado(g, s):
    """
    gerador x int ---> int
    Define o novo estado de g como sendo s e devolve s.
    """
    g["seed"] = s
    return s


def atualiza_estado(g):
    """
    gerador ---> int
    Atualiza o estado do gerador g de acordo com o algoritmo xorshift de geração de números pseudoaleatórios, e
    devolve-o.
    """
    if g["bits"] == 32:  # sequência de operações xorshift do gerador de 32 bits
        g["seed"] ^= (g["seed"] << 13) & 0xFFFFFFFF
        g["seed"] ^= (g["seed"] >> 17) & 0xFFFFFFFF
        g["seed"] ^= (g["seed"] << 5) & 0xFFFFFFFF
    else:  # sequência de operações xorshift do gerador de 64 bits
        g["seed"] ^= (g["seed"] << 13) & 0xFFFFFFFFFFFFFFFF
        g["seed"] ^= (g["seed"] >> 7) & 0xFFFFFFFFFFFFFFFF
        g["seed"] ^= (g["seed"] << 17) & 0xFFFFFFFFFFFFFFFF
    return g["seed"]


def eh_gerador(arg):
    """
    universal ---> booleano
    Devolve True caso o seu argumento seja um TAD gerador e False caso contrário.
    """
    return isinstance(arg, dict) and len(arg) == 2 and arg["bits"] in (32, 64) and isinstance(arg["seed"], int) \
           and arg["seed"] > 0 and arg["seed"] < 2 ** arg["bits"]


def geradores_iguais(g1, g2):
    """
    gerador x gerador ---> booleano
    Devolve True apenas se g1 e g2 são geradores e são iguais.
    """
    return eh_gerador(g1) and eh_gerador(g2) and g1["bits"] == g2["bits"] and g1["seed"] == g2["seed"]


def gerador_para_str(g):
    """
    gerador ---> str
    Recebe um gerador e devolve uma string do tipo "xorshiftbits(s=seed)", onde bits é substituído pelo número de bits e
    seed pela seed do gerador.
    """
    return "xorshift" + str(g["bits"]) + "(s=" + str(g["seed"]) + ")"


def gera_numero_aleatorio(g, n):
    """
    gerador x int ---> int
    Atualiza o estado do gerador g e devolve um número aleatório no intervalo [1, n] obtido a partir do novo estado s de
    g como 1 + s % n.
    """
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n


def gera_carater_aleatorio(g, c):
    """
    gerador x str ---> str
    Atualiza o estado do gerador g e devolve um carater aleatório no intervalo entre "A" e o caráter maiúsculo c. Este é
    obtido a partir do novo estado s de g como o caráter na posição s % l da cadeia de carateres de tamanho l formada
    por todos os carateres entre "A" e c.
    """
    atualiza_estado(g)
    lista = [chr(i) for i in range(65, ord(c) + 1)]  # lista com todas as letras do alfabeto
    return lista[obtem_estado(g) % len(lista)]


def cria_coordenada(col, lin):
    """
    str x int ---> coordenada
    Recebe os valores correspondentes à coluna col e linha lin e devolve a coordenada correspondente.
    """
    alfabeto = [chr(i) for i in range(65, 91)]
    if col not in alfabeto or not isinstance(lin, int) or lin < 1 or lin > 99:
        raise ValueError("cria_coordenada: argumentos invalidos")
    return (col, lin)


def obtem_coluna(c):
    """
    coordenada ---> str
    Devolve a coluna col da coordenada c.
    """
    return c[0]


def obtem_linha(c):
    """
    coordenada ---> int
    Devolve a coluna lin da coordenada c.
    """
    return c[1]


def eh_coordenada(arg):
    """
    universal ---> booleano
    Devolve True caso o seu argumento seja um TAD coordenada e False caso contrário.
    """
    alfabeto = [chr(i) for i in range(65, 91)]
    numeros = [i for i in range(1, 100)]
    return isinstance(arg, tuple) and len(arg) == 2 and arg[0] in alfabeto and arg[1] in numeros


def coordenadas_iguais(c1, c2):
    """
    coordenada x coordenada ---> booleano
    Devolve True apenas se c1 e c2 são coordenadas e são iguais.
    """
    return eh_coordenada(c1) and eh_coordenada(c2) and c1[0] == c2[0] and c1[1] == c2[1]


def coordenada_para_str(c):
    """
    coordenada ---> str
    Recebe uma coordenada e devolve uma string composta pela letra que corresponde à coluna da coordenada seguida pelo
    número que corresponde à linha da coordenada. Se o número só tiver um dígito acrescenta-se um zero (por exemplo 9
    fica 09).
    """
    if c[1] < 10:  # se a linha corresponder a um número de um algarismo esse número aparece depois de um zero
        return c[0] + "0" + str(c[1])
    return c[0] + str(c[1])


def str_para_coordenada(s):
    """
    str ---> coordenada
    Devolve a coordenada reapresentada pelo seu argumento.
    """
    return cria_coordenada(s[0], int(s[1:]))


def obtem_coordenadas_vizinhas(c):
    """
    coordenada ---> tuplo
    Devolve um tuplo com as coordenadas vizinhas à coordenada c, começando pela coordenada na diagonal acima-esquerda de
    c e seguindo no sentido horário.
    """
    vizinhas_possiveis = [(chr(ord(obtem_coluna(c)) - 1), obtem_linha(c) - 1),  # coluna à esquerda, linha acima
                          (obtem_coluna(c), obtem_linha(c) - 1),  # mesma coluna, linha acima
                          (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c) - 1),  # coluna à direita, linha acima
                          (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c)),  # coluna à direita, mesma linha
                          (chr(ord(obtem_coluna(c)) + 1), obtem_linha(c) + 1),  # coluna à direita, linha abaixo
                          (obtem_coluna(c), obtem_linha(c) + 1),  # mesma coluna, linha abaixo
                          (chr(ord(obtem_coluna(c)) - 1), obtem_linha(c) + 1),  # coluna à esquerda, linha abaixo
                          (chr(ord(obtem_coluna(c)) - 1), obtem_linha(c))]  # coluna à esquerda, mesma linha
    res = ()
    for i in vizinhas_possiveis:
        if "A" <= i[0] <= "Z" and 1 <= i[1] <= 99:  # verifica se a vizinha existe, ou seja se a coluna está entre A e Z
            # e a linha entre 1 e 99
            res += (cria_coordenada(i[0], i[1]),)  # cria a coordenada e adiciona-a ao tuplo final
    return tuple(res)


def obtem_coordenada_aleatoria(c, g):
    """
    coordenada x gerador ---> coordenada
    Recebe uma coordenada c e um TAD gerador g, e devolve uma coordenada gerada aleatoriamente em que c define a maior
    coluna e maior linha possíveis.
    """
    col = gera_carater_aleatorio(g, obtem_coluna(c))
    lin = gera_numero_aleatorio(g, obtem_linha(c))
    return cria_coordenada(col, lin)


def cria_parcela():
    """
    {} ---> parcela
    Devolve uma parcela tapada sem mina escondida.
    """
    return {"estado": "tapada", "mina": False}


def cria_copia_parcela(p):
    """
    parcela ---> parcela
    Recebe uma parcela e devolve uma nova cópia dessa parcela.
    """
    if not isinstance(p, dict) or len(p) != 2 or p["estado"] not in ("tapada", "limpa", "marcada"):
        raise ValueError("cria_copia_parcela: argumentos invalidos")
    if p["mina"] not in (True, False):
        raise ValueError("cria_copia_parcela: argumentos invalidos")
    return p.copy()


def limpa_parcela(p):
    """
    parcela ---> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para limpa, e devolve a própria parcela.
    """
    p["estado"] = "limpa"
    return p


def marca_parcela(p):
    """
    parcela ---> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para marcada, e devolve a própria parcela.
    """
    p["estado"] = "marcada"
    return p


def desmarca_parcela(p):
    """
    parcela ---> parcela
    Modifica destrutivamente a parcela p modificando o seu estado para tapada, e devolve a própria parcela.
    """
    p["estado"] = "tapada"
    return p


def esconde_mina(p):
    """
    parcela ---> parcela
    Modifica destrutivamente a parcela p escondendo uma mina na parcela, e devolve a própria parcela.
    """
    p["mina"] = True
    return p


def eh_parcela(arg):
    """
    universal ---> booleano
    Devolve True caso o seu argumento seja um TAD parcela e False caso contrário
    """
    return isinstance(arg, dict) and len(arg) == 2 and arg["estado"] in ("tapada", "limpa", "marcada") and arg["mina"] \
           in (True, False)


def eh_parcela_tapada(p):
    """
    parcela ---> booleano
    Devolve True caso a parcela p se encontre tapada e False caso contrário.
    """
    return p["estado"] == "tapada"


def eh_parcela_marcada(p):
    """
    parcela ---> booleano
    Devolve True caso a parcela p se encontre marcada e False caso contrário.
    """
    return p["estado"] == "marcada"


def eh_parcela_limpa(p):
    """
    parcela ---> booleano
    Devolve True caso a parcela p se encontre limpa e False caso contrário.
    """
    return p["estado"] == "limpa"


def eh_parcela_minada(p):
    """
    parcela ---> booleano
    Devolve True caso a parcela p esconda uma mina e False caso contrário.
    """
    return p["mina"] is True


def parcelas_iguais(p1, p2):
    """
    parcela x parcela ---> booleano
    Devolve True apenas se p1 e p2 são parcelas e são iguais.
    """
    return eh_parcela(p1) and eh_parcela(p2) and p1["estado"] == p2["estado"] and p1["mina"] == p2["mina"]


def parcela_para_str(p):
    """
    parcela ---> booleano
    Devolve a cadeia de caracteres que representa a parcela em função do seu estado: parcelas tapadas ("#"), parcelas
    marcadas ("@"), parcelas limpas sem mina ("?") e parcelas limpas com mina ("X").
    """
    if eh_parcela_tapada(p):
        return "#"
    elif eh_parcela_marcada(p):
        return "@"
    elif eh_parcela_limpa(p) and not eh_parcela_minada(p):
        return "?"
    elif eh_parcela_limpa(p) and eh_parcela_minada(p):
        return "X"


def alterna_bandeira(p):
    """
    parcela ---> booleano
    Recebe uma parcela p e modifica-a destrutivamente da seguinte forma: desmarca se estiver marcada e marca se estiver
    tapada, devolvendo True. Em qualquer outro caso, não modifica a parcela e devolve False.
    """
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    else:
        return False


def cria_campo(c, l):
    """
    str x int ---> campo
    Recebe uma cadeia de carateres e um inteiro correspondente à última coluna e à última linha de um campo de minas, e
    devolve o campo do tamanho pretendido formado por parcelas tapadas sem minas.
    """
    if c not in [chr(n) for n in range(65, 91)] or not isinstance(l, int) or l < 1 or l > 99:
        raise ValueError("cria_campo: argumentos invalidos")
    campo = {}
    for linha in range(1, l + 1):
        for coluna in range(65, ord(c) + 1):
            campo[coordenada_para_str(cria_coordenada(chr(coluna), linha))] = cria_parcela()
    return campo  # campo é um dicionário onde as chaves são coordenadas em formato de string e os valores são parcelas


def cria_copia_campo(m):
    """
    campo ---> campo
    Recebe um campo e devolve uma nova cópia do campo.
    """
    return cria_campo(obtem_ultima_coluna(m), obtem_ultima_linha(m))


def obtem_ultima_coluna(m):
    """
    campo ---> str
    Recebe um campo e devolve a string que corresponde à sua última coluna.
    """
    ultima_coluna = "A"
    for coordenada in m.keys():
        if coordenada[0] > ultima_coluna:  # sempre que uma coluna seja maior que a ultima_coluna esta é atualizada
            ultima_coluna = coordenada[0]
    return ultima_coluna


def obtem_ultima_linha(m):
    """
    campo ---> int
    Recebe um campo e devolve o inteiro que corresponde à sua última linha.
    """
    ultima_linha = 1
    for coordenada in m.keys():
        if int(coordenada[1:]) > ultima_linha:  # sempre que uma linha seja maior que a ultima_linha esta é atualizada
            ultima_linha = int(coordenada[1:])
    return ultima_linha


def obtem_parcela(m, c):
    """
    campo x coordenada ---> parcela
    Devolve a parcela do campo m que se encontra na coordenada c.
    """
    return m[coordenada_para_str(c)]


def obtem_coordenadas(m, s):
    """
    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de esquerda à direita e de cima a baixo das
    parcelas dependendo do valor de s: "limpas" para as parcelas limpas, "tapadas" para as parcelas tapadas, "marcadas"
    para as parcelas marcadas, e "minadas" para as parcelas que escondem minas.
    """
    res = ()
    for coordenada in m.keys():
        if s == "minadas" and eh_parcela_minada(m[coordenada]):
            res += (str_para_coordenada(coordenada),)
        elif s == "limpas" and eh_parcela_limpa(m[coordenada]):
            res += (str_para_coordenada(coordenada),)
        elif s == "tapadas" and eh_parcela_tapada(m[coordenada]):
            res += (str_para_coordenada(coordenada),)
        elif s == "marcadas" and eh_parcela_marcada(m[coordenada]):
            res += (str_para_coordenada(coordenada),)
    return res


def obtem_numero_minas_vizinhas(m, c):
    """
    campo x coordenada ---> inteiro
    Devolve o número de parcelas vizinhas da parcela na coordenada c que escondem uma mina.
    """
    res = 0
    for coordenada in obtem_coordenadas_vizinhas(c):
        if coordenada_para_str(coordenada) in m.keys() and eh_parcela_minada(m[coordenada_para_str(coordenada)]):
            res += 1
    return res


def eh_campo(arg):
    """
    universal ---> booleano
    Devolve True caso o seu argumento seja um TAD campo e False caso contrário.
    """
    if not isinstance(arg, dict):
        return False
    if len(arg) == 0:
        return False
    for i in arg.keys():
        if not isinstance(i, str) or len(i) != 3 or i[0] not in [chr(n) for n in range(65, 91)]:
            return False
        if not (("0" <= i[1] <= "9" and "0" <= i[2] <= "9") and i[1:] != "00"):
            return False
        if not eh_coordenada(str_para_coordenada(i)) or not eh_parcela(arg[i]):
            return False
        if len(arg) != (ord(obtem_ultima_coluna(arg)) - 64) * obtem_ultima_linha(arg):
            return False
    return True


def eh_coordenada_do_campo(m, c):
    """
    campo x coordenada ---> booleano
    devolve True se c é uma coordenada válida dentro do campo m.
    """
    return coordenada_para_str(c) in m.keys()


def campos_iguais(m1, m2):
    """
    campo x campo ---> booleano
    Devolve True apenas se m1 e m2 forem campos e forem iguais.
    """
    if not eh_campo(m1) or not eh_campo(m2):
        return False
    if len(m1) != len(m2):
        return False
    for i in m1.keys():
        if i not in m2.keys():
            return False
        if not parcelas_iguais(m1[i], m2[i]):
            return False
    return True


def campo_para_str(m):
    """
    campo ---> str
    Devolve uma string que representa o campo de minas.
    """
    res = "   " + "".join([chr(i) for i in range(65, ord(obtem_ultima_coluna(m)) + 1)]) + "\n"  # primeira linha do
    # campo, constituída pelas letras que identificam cada coluna
    res += "  " + "+" + "-" * ((ord(obtem_ultima_coluna(m))) - 64) + "+\n01|"  # limite superior do campo
    num = 1  # linha inicial
    for coordenada in m.keys():
        if int(coordenada[1:]) != num:  # mudança de linha
            num += 1
            res += "|\n" + coordenada[1:] + "|"
        if eh_parcela_limpa(m[coordenada]) and not eh_parcela_minada(m[coordenada]):  # se a parcela for limpa sem mina
            if obtem_numero_minas_vizinhas(m, str_para_coordenada(coordenada)) == 0:  # se não tiver minas vizinhas
                res += " "  # a parcela é representada por um espaço vazio
            else:
                res += str(obtem_numero_minas_vizinhas(m, str_para_coordenada(coordenada)))  # se tiver minas vizinhas é
                # representada pelo seu número
        else:
            res += parcela_para_str(m[coordenada])
    res += "|\n  +" + "-" * ((ord(obtem_ultima_coluna(m))) - 64) + "+"  # limite inferior do campo
    return res


def coloca_minas(m, c, g, n):
    """
    campo x coordenada x gerador x inteiro ---> campo
    Modifica destrutivamente o campo m escondendo n minas em parcelas dentro do campo.
    """
    i = 0
    while i < n:
        coordenada = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m)), g)
        if coordenada != c and coordenada not in obtem_coordenadas_vizinhas(c) \
                and eh_parcela_minada(obtem_parcela(m, coordenada)) is False:
            esconde_mina(obtem_parcela(m, coordenada))
            i += 1
    return m


def limpa_campo(m, c):
    """
    campo x coordenada ---> campo
    Modifica destrutivamente o campo limpando a parcela na coordenada c, devolvendo-o. Se não houver nenhuma mina
    vizinha escondida, limpa todas as parcelas vizinhas tapadas. Caso a parcela se encontre já limpa, a operação não tem
    efeito.
    """
    limpa_parcela(obtem_parcela(m, c))  # a coordenada escolhida é sempre limpa
    if eh_parcela_minada(obtem_parcela(m, c)) or obtem_numero_minas_vizinhas(m, c) != 0:  # caso terminal
        return m
    else:
        for i in obtem_coordenadas_vizinhas(c):
            if eh_coordenada_do_campo(m, i) and not eh_parcela_limpa(obtem_parcela(m, i)) \
                    and not eh_parcela_marcada(obtem_parcela(m, i)):
                m = limpa_campo(m, i)  # atualiza o campo chamando novamente a função para cada uma das vizinhas
        return m


def jogo_ganho(m):
    """
    campo ---> booleano
    Recebe um campo do jogo das minas e devolve True se todas as parcelas sem minas se encontram limpas, ou False caso
    contrário.
    """
    for c in obtem_coordenadas(m, "tapadas"):
        if not eh_parcela_minada(obtem_parcela(m, c)):
            return False
    for c in obtem_coordenadas(m, "marcadas"):
        if not eh_parcela_minada(obtem_parcela(m, c)):
            return False
    return True


def turno_jogador(m):
    """
    campo ---> booleano
    Recebe um campo e deixa o jogador escolher uma ação (limpar ou marcar) e uma coordenada. Se o jogador limpar uma
    parcela minada devolve False, caso contrário devolve True.
    """
    acao = input("Escolha uma ação, [L]impar ou [M]arcar:")
    while acao not in ("L", "M"):
        acao = input("Escolha uma ação, [L]impar ou [M]arcar:")  # repete a mensagem até o input ser válido
    c = input("Escolha uma coordenada:")
    while len(c) != 3 or c[0] not in [chr(i) for i in range(65, 91)] \
            or not (("1" <= c[1] <= "9" and "0" <= c[2] <= "9") or ("0" <= c[1] <= "9" and "1" <= c[2] <= "9")) \
            or not eh_coordenada_do_campo(m, str_para_coordenada(c)):
        c = input("Escolha uma coordenada:")  # repete a mensagem até o input ser válido
    if acao == "L":
        limpa_campo(m, str_para_coordenada(c))
        if eh_parcela_minada(obtem_parcela(m, str_para_coordenada(c))):
            return False
    else:
        alterna_bandeira(obtem_parcela(m, str_para_coordenada(c)))
    return True


def minas(c, l, n, d, s):
    """
    minas(c, l, n, d, s)  é a função principal que permite jogar ao jogo das minas. A função recebe uma cadeia de
    carateres e 4 valores inteiros correspondentes, respetivamente, a: última coluna c; última linha l; número de
    parcelas com minas n; dimensão do gerador de números d; e estado inicial ou seed s para a geração de números
    aleatórios. A função devolve True se o jogador conseguir ganhar o jogo, ou False caso contrário.
    """
    if c not in [chr(i) for i in range(65, 91)] or l not in range(1, 100) or not isinstance(n, int) or n < 1 \
            or n >= (((ord(c) - 64) * l) - 9) \
            or not ((d == 32 and s in range(1, 2**32)) or (d == 64 and s in range(1, 2**64))):
        raise ValueError("minas: argumentos invalidos")
    g = cria_gerador(d, s)
    m = cria_campo(c, l)
    print("   [Bandeiras " + str(len(obtem_coordenadas(m, "marcadas"))) + "/" + str(n) + "]")  # contagem de bandeiras
    print(campo_para_str(m))
    coord = input("Escolha uma coordenada:")
    while len(coord) != 3 or coord[0] not in [chr(i) for i in range(65, 91)] \
            or not (("1" <= coord[1] <= "9" and "0" <= coord[2] <= "9")
                    or ("0" <= coord[1] <= "9" and "1" <= coord[2] <= "9")) \
            or not eh_coordenada_do_campo(m, str_para_coordenada(coord)):
        coord = input("Escolha uma coordenada:")
    m = coloca_minas(m, str_para_coordenada(coord), g, n)  # as minas são colocadas
    m = limpa_campo(m, str_para_coordenada(coord))  # a primeira parcela é limpa
    while not jogo_ganho(m):
        print("   [Bandeiras " + str(len(obtem_coordenadas(m, "marcadas"))) + "/" + str(n) + "]")
        print(campo_para_str(m))
        var = turno_jogador(m)
        if not var:  # se uma parcela com mina for limpa
            print("   [Bandeiras " + str(len(obtem_coordenadas(m, "marcadas"))) + "/" + str(n) + "]")
            print(campo_para_str(m))
            print("BOOOOOOOM!!!")  # mensagem de derrota
            return False  # fim do jogo (derrota)
    print("   [Bandeiras " + str(len(obtem_coordenadas(m, "marcadas"))) + "/" + str(n) + "]")
    print(campo_para_str(m))
    print("VITORIA!!!")  # mensagem de vitória
    return True  # fim do jogo (vitória)
