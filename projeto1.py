"""
1º Projeto

Nome: David Antunes
Número de aluno: 107061
Contacto: david.f.antunes@tecnico.ulisboa.pt
"""


def limpa_texto(cad_carateres):

    """
    cad. carateres ---> cad. carateres
    Recebe uma cadeia de carateres e remove os carateres brancos.
    """

    return " ".join(cad_carateres.split())  # separa todas as palavras e depois junta-as com um espaço entre elas,
    # removendo todos os carateres brancos a mais


def corta_texto(cad_carateres, inteiro):

    """
    cad. carateres x inteiro ---> cad. carateres x cad. carateres
    Recebe uma cadeia de carateres e uma largura de coluna, e devolve uma cadeia de carateres com as palavras até essa
    largura e outra com o resto das palavras.
    """

    lista = cad_carateres.split()
    cadeia1 = ""
    for palavra in lista:
        if len(cadeia1) + len(palavra) > inteiro:
            break
        cadeia1 = cadeia1 + " " + palavra
    cadeia2 = cad_carateres[len(cadeia1):]  # cria a segunda subcadeia, composta pelo resto das palavras
    return limpa_texto(cadeia1), limpa_texto(cadeia2)  # utiliza a função limpa_texto para garantir que não
    # existem espaços a mais, e devolve as duas subcadeias


def insere_espacos(cad_carateres, inteiro):

    """
    cad. carateres x inteiro ---> cad. carateres
    Recebe uma cadeia de carateres e uma largura de coluna e acrescenta espaços entre as palavras da cadeia até esta ter
    a largura pretendida.
    """

    if " " in cad_carateres:  # verifica se a frase tem pelo menos duas palavras
        inteiro -= len("".join(cad_carateres.split()))  # transforma a variável inteiro na diferença entre a largura de
        # coluna e o numero de carateres ocupados por letras
        lista = cad_carateres.split()  # cria uma lista com todas as palavras da frase
        espacos_frase = len(lista) - 1  # número de conjuntos de espaços na frase
        espaco_entre_palavras = inteiro // espacos_frase  # calcula o número de espaços que é preciso pôr entre cada
        # palavra
        for i in range(espacos_frase):
            lista[i] += " " * espaco_entre_palavras
        if inteiro % espacos_frase != 0:  # verifica se sobraram carateres livres depois da divisão inteira de espaços
            for i in range(inteiro % espacos_frase):  # cria um ciclo que adiciona o resto dos espaços, adicionando um
                # em cada palavra até a coluna ter a largura desejada
                lista[i] += " "
        return "".join(lista)
    else:
        return cad_carateres + (inteiro - len(cad_carateres)) * " "


def justifica_texto(cad_carateres, largura):
    """
    cad. carateres x inteiro ---> tuplo
    Recebe uma cadeia de carateres e uma largura de coluna e devolve um tuplo de cadeias justificadas com essa largura..
    """
    if not isinstance(cad_carateres, str) or not isinstance(largura, int) or len(cad_carateres) == 0 or largura < 1:
        raise ValueError("justifica_texto: argumentos invalidos")
    for palavra in cad_carateres.split():
        if len(palavra) > largura:
            raise ValueError("justifica_texto: argumentos invalidos")
    cad_carateres = limpa_texto(cad_carateres)
    texto_justificado = ()
    while len(cad_carateres) > 0:
        if len(cad_carateres) > largura:
            linha = corta_texto(cad_carateres, largura)[0]
            linha = insere_espacos(linha, largura)
            texto_justificado += (linha,)
        else:
            texto_justificado += (cad_carateres + (largura - len(cad_carateres)) * " ",)  # se o comprimento da cadeia
            # for inferior à largura, a última linha é adicionada com espaços no fim até preencher a largura
        cad_carateres = corta_texto(cad_carateres, largura)[-1]  # remove a linha da cadeia de carateres
    return texto_justificado


def calcula_quocientes(votos, num_deputados):
    """
    dicionário x inteiro ---> inteiro
    Recebe um dicionário com os votos apurados num círculo e um número de deputados, e devolve um dicionário com as
    mesmas chaves que contém a lista com os quocientes calculados com o método de Hondt por ordem decrescente.
    """
    copia = votos.copy()
    for partido in copia:
        lista = []
        for divisor in range(1, num_deputados + 1):
            lista += [copia[partido] / divisor]
        copia[partido] = lista  # substitui o número de votos do partido pela lista dos quocientes
    return copia


def atribui_mandatos(votos, num_deputados):
    """
    dicionário x inteiro ---> lista
    Recebe um dicionário com os votos apurados num círculo e um número de deputados e devolve uma lista com os partidos
    que ficaram com cada deputado.
    """
    res = []
    copia = calcula_quocientes(votos, num_deputados)
    while len(res) != num_deputados:
        maior_partido = ""  # partido com o quociente maior
        maior_num = 0  # quociente maior
        for partido, quocientes in copia.items():
            if quocientes[0] > maior_num or (quocientes[0] == maior_num and votos[partido] < votos[maior_partido]):
                maior_partido, maior_num = partido, quocientes[0]
        del copia[maior_partido][0]
        res.append(maior_partido)
    return res


def obtem_partidos(info):
    """
    dicionário ---> lista
    Recebe um dicionário com a informação sobre as eleições num território com vários círculos eleitorais e devolve uma
    lista com o nome de todos os partidos por ordem alfabética.
    """
    res = []
    for circulo in info:
        for partido in info[circulo]["votos"]:
            if partido not in res:
                res.append(partido)
    return sorted(res)


def obtem_resultado_eleicoes(info):
    """
    dicionário ---> lista
    Recebe um dicionário com a informação sobre as eleições num território com vários círculos eleitorais, e devolve uma
    lista ordenada em que cada elemento é um tuplo com o nome do partido, o número total de deputados obtidos e o número
    total de votos obtidos.
    """
    if not isinstance(info, dict):
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    for circulo in info:
        if "votos" not in info[circulo].keys() or "deputados" not in info[circulo].keys() or len(info[circulo]) != 2:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if not isinstance(info[circulo]["deputados"], int) or info[circulo]["deputados"] < 1:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if len(info[circulo]["votos"]) < 1:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        for partido in info[circulo]["votos"]:
            if not isinstance(info[circulo]["votos"][partido], int) or info[circulo]["votos"][partido] < 1:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    res = {}
    for circulo in info:
        res[circulo] = atribui_mandatos(info[circulo]["votos"], info[circulo]["deputados"])  # cria um dicionário no
        # qual as chaves são os círculos e os valores são as listas dos partidos que ficaram com cada deputado
    deputados_obtidos = {}
    for circulo in res:  # este ciclo cria um dicionário no qual as chaves são os partidos e os valores são o número de
        # deputados que cada partido obteve
        for partido in res[circulo]:
            if partido in deputados_obtidos:
                deputados_obtidos[partido] += 1
            else:
                deputados_obtidos[partido] = 1
    for partido in obtem_partidos(info):  # adiciona os partidos que não receberam nenhum deputado ao dicionário dos
        # deputados obtidos
        if partido not in deputados_obtidos:
            deputados_obtidos[partido] = 0
    votos_obtidos = {}
    for circulo in info:  # este ciclo cria um dicionário no qual as chaves são os partidos e os valores são o total de
        # votos que o partido obteve
        for partido in info[circulo]["votos"]:
            if partido in votos_obtidos:
                votos_obtidos[partido] += info[circulo]["votos"][partido]
            else:
                votos_obtidos[partido] = info[circulo]["votos"][partido]
    lista = []
    for partido in obtem_partidos(info):
        lista.append((partido, deputados_obtidos[partido], votos_obtidos[partido]))

    def bubble_sort(l):  # esta função bubble sort é usada para ordenar os tuplos na lista final por ordem decrescente
        # de número total de votos
        changed = True
        size = len(l) - 1
        while changed:
            changed = False
            for i in range(size):
                if l[i][2] < l[i + 1][2]:
                    l[i], l[i + 1] = l[i + 1], l[i]
                    changed = True
            size = size - 1
        return l
    return bubble_sort(lista)


def produto_interno(vetor1, vetor2):
    """
    tuplo x tuplo ---> real
    Recebe dois tuplos com a mesma dimensão e devolve o seu produto.
    """

    produto = 0
    for i in range(len(vetor1)):
        produto = produto + vetor1[i] * vetor2[i]
    return float(produto)


def verifica_convergencia(matriz, vetor, solucao, precisao):

    """
    tuplo x tuplo x tuplo x real ---> booleano
    Recebe uma matriz A, um vetor c, uma solução x e uma precisão, e devolve True caso o valor absoluto do erro de todas
    as equações seja inferior à precisão, |fi(x) − ci| < ε, e False caso contrário.
    """

    for i in range(len(matriz)):
        if abs(produto_interno(matriz[i], solucao) - vetor[i]) > precisao:
            return False
    return True


def retira_zeros_diagonal(matriz, vetor):
    """
    tuplo x tuplo ---> tuplo x tuplo
    Recebe uma matriz e um vetor e reoordena as suas linhas de forma a que não existam zeros na diagonal.
    """
    matriz, vetor = list(matriz), list(vetor)  # transforma a matriz e o vetor em listas para que os seus elementos
    # possam ser alterados
    for i in range(len(matriz)):
        if matriz[i][i] == 0:
            for j in range(len(matriz)):
                if matriz[j][i] != 0 and matriz[i][j] != 0:
                    matriz[i], matriz[j] = matriz[j], matriz[i]  # as linhas i e j são trocadas
                    vetor[i], vetor[j] = vetor[j], vetor[i]  # as linhas i e j do vetor também são trocadas
                    break
    return tuple(matriz), tuple(vetor)  # transforma a matriz e o vetor em tuplos e devolve-os


def eh_diagonal_dominante(matriz):
    """
    tuplo ---> booleano
    Recebe uma matriz e devolve True se esta for diagonalmente dominante. Caso contrário devolve False
    """
    for i in range(len(matriz)):
        soma_linha = 0  # soma dos valores absolutos de cada entrada de uma linha exceto a que se encontra na diagonal
        for j in range(len(matriz[i])):
            if j != i:  # se a entrada não estiver na diagonal
                soma_linha += abs(matriz[i][j])
            if soma_linha > abs(matriz[i][i]):
                return False
    return True


def resolve_sistema(matriz, vetor, precisao):
    """
    tuplo x tuplo x real ---> tuplo
    Recebe uma matriz, um vetor e uma precisão, e devolve um tuplo que é a solução do sistema de equações de entrada
    utilizando o método de Jacobi.
    """
    if not isinstance(matriz, tuple) or not isinstance(vetor, tuple) or not isinstance(precisao, float) or precisao < 0:
        raise ValueError("resolve_sistema: argumentos invalidos")
    for linha in matriz:
        if len(linha) != len(matriz) or not isinstance(linha, tuple):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for entrada in linha:
            if not isinstance(entrada, (int, float)):
                raise ValueError("resolve_sistema: argumentos invalidos")
    for i in vetor:
        if not isinstance(i, (float, int)):
            raise ValueError("resolve_sistema: argumentos invalidos")
    matriz, vetor = retira_zeros_diagonal(matriz, vetor)[0], retira_zeros_diagonal(matriz, vetor)[1]
    if not eh_diagonal_dominante(matriz):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")
    x = [] + [0] * len(matriz)  # cria a lista que contém a estimativa da solução da equação. Inicialmente todas as
    # entradas são zero
    while not verifica_convergencia(matriz, vetor, x, precisao):
        for i in range(len(x)):
            x[i] = x[i] + (vetor[i] - produto_interno(matriz[i], x)) / matriz[i][i]  # método de Jacobi
    return tuple(x)  # transforma a lista da solução num tuplo e devolve-o
