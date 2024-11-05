import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

# Função que realiza a busca simples
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

# Função que realiza a busca usando o autômato KMP
def busca_com_automato(cmaior, cmenor):
    resultado_texto.insert(tk.END, "Iniciando a busca COM autômato\n")
    
    alfabeto = ['A', 'T', 'C', 'G']
    estados = ['s0', 's1', 's2', 's3']
    inicial = ['s0']
    finais = ['s3']
    transicoes = [
        ['s0', 'A', 's1'], ['s0', 'T', 's0'], ['s0', 'C', 's0'], ['s0', 'G', 's0'],
        ['s1', 'A', 's1'], ['s1', 'T', 's2'], ['s1', 'C', 's0'], ['s1', 'G', 's0'],
        ['s2', 'A', 's1'], ['s2', 'T', 's0'], ['s2', 'C', 's3'], ['s2', 'G', 's0'],
        ['s3', 'A', 's1'], ['s3', 'T', 's0'], ['s3', 'C', 's2'], ['s3', 'G', 's0']
    ]
    
    dtransicoes = dict(((e1, e2), s) for e1, e2, s in transicoes)
    estado = inicial[0]
    qtd_ocorrencias = 0

    for i in range(len(cmaior)):
        if estado in finais:
            resultado_texto.insert(tk.END, f"Achou uma ocorrência na posição {i - len(cmenor)}\n")
            qtd_ocorrencias += 1
        
        simbolo = cmaior[i]
        resultado_texto.insert(tk.END, f"Estado atual = {estado}\nSimbolo atual = {simbolo}\n")
        estado = dtransicoes.get((estado, simbolo), estado)
        
    if estado in finais:
        resultado_texto.insert(tk.END, f"Achou uma ocorrência na posição {len(cmaior) - len(cmenor)}\n")
        qtd_ocorrencias += 1

    return qtd_ocorrencias

# Função para limpar o gráfico
def limpar_grafico():
    plt.close('all')

# Função para gerar o autômato visual
def gerar_automato():
    limpar_grafico()  # Limpa o gráfico anterior antes de gerar um novo

    alfabeto = ['A', 'T', 'C', 'G']
    estados = ['s0', 's1', 's2', 's3']
    transicoes = [
        ['s0', 'A', 's1'], ['s0', 'T', 's0'], ['s0', 'C', 's0'], ['s0', 'G', 's0'],
        ['s1', 'A', 's1'], ['s1', 'T', 's2'], ['s1', 'C', 's0'], ['s1', 'G', 's0'],
        ['s2', 'A', 's1'], ['s2', 'T', 's0'], ['s2', 'C', 's3'], ['s2', 'G', 's0'],
        ['s3', 'A', 's1'], ['s3', 'T', 's0'], ['s3', 'C', 's2'], ['s3', 'G', 's0']
    ]

    G = nx.DiGraph()
    G.add_nodes_from(estados)

    for trans in transicoes:
        G.add_edge(trans[0], trans[2], label=trans[1])

    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), label_pos=0.5)
    plt.title("Autômato gerado para busca KMP")
    plt.show()

# Função principal para a interface de busca
def buscar():
    cmaior = entrada_cmaior.get().strip().upper()
    cmenor = entrada_cmenor.get().strip().upper()

    if any(char not in 'ATCG' for char in cmaior) or any(char not in 'ATCG' for char in cmenor):
        resultado_texto.delete(1.0, tk.END)
        resultado_texto.insert(tk.END, "Erro: As cadeias devem conter apenas os caracteres A, T, C e G.\nSem espaços!.\n")
        return

    cmaior = [char for char in cmaior]
    cmenor = [char for char in cmenor]

    resultado_texto.delete(1.0, tk.END)

    ocorrencias_simples = busca_simples(cmaior, cmenor)
    ocorrencias_com = busca_com_automato(cmaior, cmenor)

    resultado_texto.insert(tk.END, f"\nTotal de ocorrências (SEM autômato): {ocorrencias_simples}\n")
    resultado_texto.insert(tk.END, f"Total de ocorrências (COM autômato): {ocorrencias_com}\n")

    gerar_automato()

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
