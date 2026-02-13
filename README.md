# BuscaDeDnaEmKMP

Um aplicativo desenvolvido em Python que busca padrões em sequências de DNA utilizando o algoritmo KMP (Knuth-Morris-Pratt) e gera visualizações interativas do autômato finito.

## 📋 Descrição

Este projeto implementa duas abordagens para busca de padrões em cadeias de DNA:
- **Busca simples**: Algoritmo de força bruta que compara caractere por caractere
- **Busca com autômato KMP**: Implementação otimizada usando autômato finito determinístico

O programa permite comparar a eficiência entre os dois métodos e visualizar graficamente o autômato gerado pelo algoritmo KMP.

## 🧬 Funcionalidades

- Interface gráfica intuitiva usando Tkinter
- Validação de entrada para sequências de DNA (aceita apenas A, T, C, G)
- Busca de padrões usando dois algoritmos diferentes
- Contagem de comparações e ocorrências encontradas
- Geração automática de grafo interativo do autômato KMP
- Visualização em tempo real das comparações realizadas
- Abertura automática do grafo no navegador padrão

## 🔧 Dependências

```bash
pip install tkinter
pip install networkx
pip install pyvis
pip install matplotlib
```

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/BuscaDeDnaEmKMP.git
cd BuscaDeDnaEmKMP
```

2. Instale as dependências necessárias

3. Execute o programa:
```bash
python busca_dna.py
```

4. Na interface gráfica:
   - Digite a **cadeia maior** (sequência de DNA onde será feita a busca)
   - Digite a **cadeia menor** (padrão que deseja encontrar)
   - Clique em **Buscar**
   - Observe os resultados e o grafo gerado

## 💡 Exemplo de Uso

**Entrada:**
- Cadeia maior: `ATCGATCGATCG`
- Cadeia menor: `GATC`

**Saída:**
- Posições onde o padrão foi encontrado
- Número de comparações realizadas (ambos os métodos)
- Quantidade de ocorrências
- Grafo interativo do autômato KMP

## 📊 Estrutura do Projeto

```
BuscaDeDnaEmKMP/
│
├── busca_dna.py          # Código principal com interface gráfica completa
├── Atualiza1             # Versão anterior do código
├── README.md             # Documentação do projeto
└── Grafo_KMP.html        # Arquivo gerado com o grafo (criado após execução)
```

## 🔍 Como Funciona

### Algoritmo KMP
O algoritmo KMP utiliza um autômato finito determinístico que:
1. Calcula o maior prefixo próprio que também é sufixo
2. Cria transições de estado para cada caractere do alfabeto
3. Evita comparações redundantes ao processar a cadeia

### Visualização do Autômato
O grafo gerado mostra:
- **Estados**: Representados como s0, s1, s2, etc.
- **Transições**: Arestas rotuladas com os caracteres do DNA
- **Estado final**: Indica quando o padrão foi completamente encontrado

## 📝 Notas Técnicas

- O alfabeto utilizado é fixo: `['A', 'T', 'C', 'G']`
- As entradas são automaticamente convertidas para maiúsculas
- Espaços e caracteres inválidos são rejeitados
- A janela se ajusta automaticamente ao tamanho da tela

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

---

**Desenvolvido como ferramenta educacional para demonstração do algoritmo KMP aplicado à bioinformática**
