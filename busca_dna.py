import tkinter as tk
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import os
import webbrowser
import time


# Função que calcula o maior prefixo que é igual ao sufixo
def maiorPrefSufProprio(cadeia):
    maior = 0
    for i in reversed(range(len(cadeia) - 1)):
        prefixo = cadeia[:(i + 1)]
        sufixo = cadeia[-(i + 1):]
        if prefixo == sufixo:
            if len(prefixo) > maior:
                maior = len(prefixo)
                break
    return maior


# Função que cria as transições para o autômato KMP
def criaTransicoes(cadeia, alfabeto):
    sub = ""
    transicoes = []
    for estado in range(len(cadeia) + 1):
        if estado < len(cadeia):
            letra_correta = cadeia[estado]
        else:
            letra_correta = 'FIM'
        for letra_alternativa in alfabeto:
            if letra_alternativa == letra_correta:
                proximo = estado + 1
            else:
                proximo = maiorPrefSufProprio(sub + letra_alternativa)
            estado_antes = 's' + str(estado)
            estado_depois = 's' + str(proximo)
            transicoes.append([estado_antes, letra_alternativa, estado_depois])
        sub = sub + letra_correta
    return transicoes


# Função para ajustar a janela ao tamanho da tela
def ajustar_tamanho_tela(janela):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    janela.geometry(f"{largura_tela}x{altura_tela}")


# Função que valida se a cadeia contém apenas caracteres válidos (A, T, C, G)
def validar_cadeia(cadeia):
    # Converte para maiúsculas
    cadeia = cadeia.upper()
    # Verifica se todos os caracteres são válidos (A, T, C, G)
    for char in cadeia:
        if char not in 'ATCG':
            return False
    return True


# Função chamada pelo botão de busca
def buscar():
    cmaior = entrada_cmaior.get()
    cmenor = entrada_cmenor.get()

    # Limpa o campo de texto antes de exibir novos resultados
    resultado_texto.delete(1.0, tk.END)

    # Valida as entradas
    if not validar_cadeia(cmaior) or not validar_cadeia(cmenor):
        resultado_texto.insert(tk.END, "Erro: As cadeias devem conter apenas os caracteres A, T, C e G.\n")
        return

    # Converte as cadeias em listas
    cmaior_lista = list(cmaior.upper())  # Garante que a cadeia será em maiúsculas
    cmenor_lista = list(cmenor.upper())  # Garante que a cadeia será em maiúsculas

    # Busca sem autômato
    qtd_ocorrencias_sem, qtd_comparacoes_sem, posicoes_sem = buscar_sem_automato(cmaior_lista, cmenor_lista, resultado_texto)

    # KMP
    alfabeto = ['A', 'T', 'C', 'G']
    transicoes = criaTransicoes(cmenor, alfabeto)
    dtransicoes = dict(((e1, e2), s) for e1, e2, s in transicoes)
    estados = ['s' + str(n) for n in range(len(cmenor) + 1)]
    iniciais = ['s0']
    finais = ['s' + str(len(cmenor))]

    qtd_ocorrencias_com, qtd_comparacoes_com, posicoes_com = buscar_com_automato(cmaior_lista, cmenor_lista, transicoes, dtransicoes, finais, iniciais, resultado_texto)

    # Exibir resultados no texto da interface
    resultado_texto.insert(tk.END, f"Busca SEM autômato:\n")
    resultado_texto.insert(tk.END, f"Posições: {posicoes_sem}\n")
    resultado_texto.insert(tk.END, f"Quantidade de comparações: {qtd_comparacoes_sem}\n")
    resultado_texto.insert(tk.END, f"Quantidade de ocorrências: {qtd_ocorrencias_sem}\n\n")

    resultado_texto.insert(tk.END, f"Busca COM autômato (KMP):\n")
    resultado_texto.insert(tk.END, f"Posições: {posicoes_com}\n")
    resultado_texto.insert(tk.END, f"Quantidade de comparações: {qtd_comparacoes_com}\n")
    resultado_texto.insert(tk.END, f"Quantidade de ocorrências: {qtd_ocorrencias_com}\n")

    # Exibir o grafo do autômato KMP
    exibir_grafo_na_interface(transicoes, estados)


# Função para criar e exibir o grafo do autômato KMP
def exibir_grafo(transicoes, estados):
    # Cria um grafo vazio
    G = nx.DiGraph()

    # Coloca os vértices no grafo G
    G.add_nodes_from(estados)

    # Colocar as arestas no grafo G
    for v in transicoes:
        G.add_edge(v[0], v[2], label=v[1])
    
    # Criar visualização com pyvis
    nt = Network('500px', '800px', directed=True)
    nt.from_nx(G)
    
    # Salva o grafo em um arquivo HTML
    nt.save_graph('Grafo_KMP.html')  # Gera o arquivo HTML

    # Aguarda para garantir que o arquivo foi salvo corretamente
    time.sleep(1)  # Ajuste o tempo de espera conforme necessário

    # Caminho absoluto para o arquivo HTML
    file_path = os.path.abspath('Grafo_KMP.html')

    # Usa o webbrowser para abrir o arquivo HTML no navegador padrão
    webbrowser.open(f'file://{file_path}')
    print(f"Grafo gerado e aberto no navegador padrão.")

# Função chamada pelo botão para exibir o grafo na interface
def exibir_grafo_na_interface(transicoes, estados):
    exibir_grafo(transicoes, estados)
    resultado_texto.insert(tk.END, "Grafo gerado como 'Grafo_KMP.html'. Abra-o manualmente no navegador, se não abrir automaticamente.\n")


# Função para buscar a subsequência sem o uso de autômato
def buscar_sem_automato(cmaior, cmenor, resultado_texto):
    qtd_ocorrencias = 0
    qtd_comparacoes = 0
    posicoes = []

    for i in range(len(cmaior)):
        achou = True
        for j in range(len(cmenor)):
            if (i + j) == len(cmaior):
                achou = False
                break
            qtd_comparacoes += 1
            resultado_texto.insert(tk.END, f"Comparando {cmaior[i + j]} com {cmenor[j]}\n")  # Exibe comparação em tempo real
            if cmenor[j] != cmaior[i + j]:
                achou = False
                break
        if achou:
            posicoes.append(i)
            qtd_ocorrencias += 1
            resultado_texto.insert(tk.END, f"Ocorrência encontrada na posição {i}\n")  # Exibe mensagem quando encontra uma ocorrência

    return qtd_ocorrencias, qtd_comparacoes, posicoes


# Função para buscar a subsequência usando o autômato KMP
def buscar_com_automato(cmaior, cmenor, transicoes, dtransicoes, finais, inicial, resultado_texto):
    qtd_ocorrencias = 0
    qtd_comparacoes = 0
    posicoes = []
    estado = inicial[0]

    for i in range(len(cmaior)):
        if estado in finais:
            posicoes.append(i - len(cmenor))
            qtd_ocorrencias += 1
            resultado_texto.insert(tk.END, f"Ocorrência encontrada na posição {i - len(cmenor)} (KMP)\n")  # Exibe quando encontra uma ocorrência

        simbolo = cmaior[i]
        estado = dtransicoes[(estado, simbolo)]
        qtd_comparacoes += 1
        resultado_texto.insert(tk.END, f"Comparando {cmaior[i]} com {simbolo}\n")  # Exibe comparação em tempo real

    # Verificar a última ocorrência
    if estado in finais:
        posicoes.append(len(cmaior) - len(cmenor))
        qtd_ocorrencias += 1
        resultado_texto.insert(tk.END, f"Ocorrência encontrada na posição {len(cmaior) - len(cmenor)} (KMP)\n")  # Exibe quando encontra uma ocorrência

    return qtd_ocorrencias, qtd_comparacoes, posicoes


# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Busca de Padrões de DNA")
ajustar_tamanho_tela(janela)  # Ajusta a janela ao tamanho da tela

label_cmaior = tk.Label(janela, text="Digite a cadeia maior (A, T, C, G):")
label_cmaior.pack()
entrada_cmaior = tk.Entry(janela, width=50)
entrada_cmaior.pack()

label_cmenor = tk.Label(janela, text="Digite a cadeia menor (A, T, C, G):")
label_cmenor.pack()
entrada_cmenor = tk.Entry(janela, width=50)
entrada_cmenor.pack()

botao_buscar = tk.Button(janela, text="Buscar", command=buscar)
botao_buscar.pack()

resultado_texto = tk.Text(janela, height=40, width=90)
resultado_texto.pack()

janela.mainloop()
