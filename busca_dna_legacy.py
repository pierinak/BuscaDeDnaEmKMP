import tkinter as tk
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

# Função para calcular o maior prefixo que é igual a um sufixo da cadeia
def maiorPrefSufProprio(cadeia):
    maior = 0
    for i in reversed(range(len(cadeia)-1)):
        prefixo = cadeia[:(i+1)]
        sufixo = cadeia[-(i+1):]
        if prefixo == sufixo:
            if len(prefixo) > maior:
                maior = len(prefixo)
                break
    return maior

# Função para criar as transições dinamicamente
def criaTransicoes(cadeia, alfabeto):
    sub = ""
    estado = 0
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
            transicao = [estado_antes, letra_alternativa, estado_depois]
            transicoes.append(transicao)
        estado += 1
        sub += letra_correta
    return transicoes

# Função de busca simples
def busca_simples(cmaior, cmenor):
    resultado_texto.insert(tk.END, "Iniciando a busca SEM autômato\n")
    resultado_texto.insert(tk.END, f"Cadeia maior como vetor:\n{cmaior}\n")
    resultado_texto.insert(tk.END, f"Cadeia menor como vetor:\n{cmenor}\n")
    
    qtd_ocorrencias = 0
    for i in range(len(cmaior) - len(cmenor) + 1):
        achou = True
        for j in range(len(cmenor)):
            if cmaior[i + j] != cmenor[j]:
                achou = False
                break
        if achou:
            resultado_texto.insert(tk.END, f"Achou na posição {i}\n")
            qtd_ocorrencias += 1
    return qtd_ocorrencias

# Função de busca com autômato
def busca_com_automato(cmaior, cmenor):
    resultado_texto.insert(tk.END, "Iniciando a busca COM autômato\n")
    
    alfabeto = ['A', 'T', 'C', 'G']
    transicoes = criaTransicoes(cmenor, alfabeto)
    dtransicoes = dict(((e1, e2), s) for e1, e2, s in transicoes)
    
    estado = 's0'
    qtd_ocorrencias = 0

    for i in range(len(cmaior)):
        simbolo = cmaior[i]
        resultado_texto.insert(tk.END, f"Estado atual = {estado}\nSimbolo atual = {simbolo}\n")
        estado = dtransicoes.get((estado, simbolo), estado)
        
        if estado == 's' + str(len(cmenor)):  # Achou uma ocorrência
            resultado_texto.insert(tk.END, f"Achou uma ocorrência na posição {i - len(cmenor) + 1}\n")
            qtd_ocorrencias += 1
    
    return qtd_ocorrencias

# Função para limpar o gráfico
def limpar_grafico():
    plt.close('all')

# Função para gerar o autômato visual
def gerar_automato(cadeia, alfabeto, transicoes):
    limpar_grafico()  # Limpa o gráfico anterior antes de gerar um novo
    G = nx.DiGraph()
    G.add_nodes_from([f's{i}' for i in range(len(cadeia) + 1)])

    for v in transicoes:
        G.add_edge(v[0], v[2], label=v[1])
    
    nt = Network('500px', '800px', directed=True)
    nt.from_nx(G)
    nt.show('G.html', True)

# Função principal para a interface de busca
def buscar():
    cmaior = entrada_cmaior.get().strip().upper()
    cmenor = entrada_cmenor.get().strip().upper()

    # Verifica se as cadeias contêm apenas caracteres válidos
    if any(char not in 'ATCG' for char in cmaior) or any(char not in 'ATCG' for char in cmenor):
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, "Erro: As cadeias devem conter apenas os caracteres A, T, C e G.\nSem espaços!.\n")
        return

    cmaior = [char for char in cmaior]
    cmenor = [char for char in cmenor]

    resultado_texto.delete(1.0, tk.END)

    # Realiza a busca
    ocorrencias_simples = busca_simples(cmaior, cmenor)
    ocorrencias_com = busca_com_automato(cmaior, cmenor)

    resultado_texto.insert(tk.END, f"\nTotal de ocorrências (SEM autômato): {ocorrencias_simples}\n")
    resultado_texto.insert(tk.END, f"Total de ocorrências (COM autômato): {ocorrencias_com}\n")

    alfabeto = ['A', 'T', 'C', 'G']
    transicoes = criaTransicoes(cmenor, alfabeto)
    gerar_automato(cmenor, alfabeto, transicoes)

# Função para ajustar a janela ao tamanho da tela
def ajustar_tamanho_tela():
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    janela.geometry(f"{largura_tela}x{altura_tela}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Busca de Padrões de DNA")
ajustar_tamanho_tela()  # Ajusta a janela ao tamanho da tela

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

resultado_texto = tk.Text(janela, height=50, width=90)
resultado_texto.pack()

janela.mainloop()
