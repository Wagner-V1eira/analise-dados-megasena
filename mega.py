import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
from tabulate import tabulate
from rich.console import Console
from rich.markdown import Markdown
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

load_dotenv()

try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        TEM_IA = True
    else:
        raise ValueError("Chave de API não encontrada")
except:
    TEM_IA = False
    print("Aviso: Chave de API não configurada no arquivo .env. A IA não será usada.")

def carregar_dados(caminho_arquivo):
    """Carrega os dados do CSV corretamente."""
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin-1')
        colunas_dezenas = df.iloc[:, 2:8]
       
        for col in colunas_dezenas.columns:
            colunas_dezenas[col] = pd.to_numeric(colunas_dezenas[col], errors='coerce')

        todos_numeros = colunas_dezenas.values.flatten()
        todos_numeros = todos_numeros[~pd.isna(todos_numeros)]
        
        return pd.Series(todos_numeros), colunas_dezenas
    except Exception as e:
        print(f"Erro ao ler arquivo CSV: {e}")
        return None, None

def gerar_grafico_frequencia(series_numeros):
    """Gera um gráfico de barras com a frequência de todos os números."""
    contagem = series_numeros.value_counts().sort_index()
    
    plt.figure(figsize=(15, 6))
    sns.barplot(x=contagem.index.astype(int), y=contagem.values, color='skyblue')
    plt.title('Frequência de Sorteio de Cada Número (01-60)')
    plt.xlabel('Número')
    plt.ylabel('Quantidade de Vezes Sorteado')
    plt.xticks(rotation=90)
    plt.tight_layout()
    print("Abrindo gráfico de frequência... Feche a janela para continuar.")
    plt.show()

def gerar_heatmap(df_dezenas):
    """Gera um heatmap mostrando a frequência dos números em um grid 6x10."""
    matriz = np.zeros((6, 10))
    
    contagem = df_dezenas.values.flatten()
    contagem = contagem[~pd.isna(contagem)]
    freq = pd.Series(contagem).value_counts()
    
    for num in range(1, 61):
        if num in freq:
            linha = (num - 1) // 10
            coluna = (num - 1) % 10
            matriz[linha, coluna] = freq[num]
            
    plt.figure(figsize=(12, 6))
    sns.heatmap(matriz, annot=True, fmt='.0f', cmap='YlOrRd', 
                xticklabels=range(1, 11), yticklabels=range(0, 60, 10))
    plt.title('Mapa de Calor da Frequência dos Números (Volante)')
    plt.xlabel('Unidade (1-10)')
    plt.ylabel('Dezena (00-50)')
    print("Abrindo mapa de calor... Feche a janela para continuar.")
    plt.show()

def calcular_atrasos(df_dezenas):
    """Calcula há quantos sorteios cada número não sai."""
    ultimo_indice = df_dezenas.index[-1]
    atrasos = {}
    
    for num in range(1, 61):
        ocorrencias = df_dezenas[df_dezenas.isin([num]).any(axis=1)].index
        
        if len(ocorrencias) > 0:
            ultimo_sorteio = ocorrencias[-1]
            atraso = ultimo_indice - ultimo_sorteio
            atrasos[num] = atraso
        else:
            atrasos[num] = len(df_dezenas) 
            
    return pd.Series(atrasos)

def gerar_grafico_atraso(df_dezenas):
    """Gera um gráfico de barras mostrando o atraso atual de cada número."""
    series_atrasos = calcular_atrasos(df_dezenas)
    
    plt.figure(figsize=(15, 6))
    sns.barplot(x=series_atrasos.index, y=series_atrasos.values, color='salmon')
    plt.title('Atraso Atual (Há quantos sorteios o número não sai)')
    plt.xlabel('Número')
    plt.ylabel('Sorteios de Atraso')
    plt.xticks(rotation=90)
    plt.tight_layout()
    print("Abrindo gráfico de atrasos... Feche a janela para continuar.")
    plt.show()

def analisar_ciclo(df_dezenas):
    """Analisa o ciclo atual das dezenas."""
    todos_numeros = set(range(1, 61))
    numeros_sorteados_ciclo = set()
    ciclo_atual = 1
    inicio_ciclo_idx = 0
    
    for index, row in df_dezenas.iterrows():
        numeros_sorteio = set(row.dropna().astype(int))
        numeros_sorteados_ciclo.update(numeros_sorteio)
        
        if numeros_sorteados_ciclo == todos_numeros:
            ciclo_atual += 1
            numeros_sorteados_ciclo = set()
            inicio_ciclo_idx = index + 1 
            
    faltam_sair = todos_numeros - numeros_sorteados_ciclo
    tamanho_ciclo_atual = len(df_dezenas) - inicio_ciclo_idx
    
    return ciclo_atual, tamanho_ciclo_atual, sorted(list(faltam_sair))

def analisar_repetencia(df_dezenas):
    """Analisa a repetência de números do concurso anterior."""
    repeticoes = []
    
    for i in range(1, len(df_dezenas)):
        anterior = set(df_dezenas.iloc[i-1].dropna().astype(int))
        atual = set(df_dezenas.iloc[i].dropna().astype(int))
        repetidos = len(atual.intersection(anterior))
        repeticoes.append(repetidos)
        
    return pd.Series(repeticoes).value_counts().sort_index()

def gerar_grafico_repetencia(df_dezenas):
    """Gera gráfico de repetência."""
    freq_repetencia = analisar_repetencia(df_dezenas)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=freq_repetencia.index, y=freq_repetencia.values, color='mediumpurple')
    plt.title('Frequência de Números Repetidos do Concurso Anterior')
    plt.xlabel('Quantidade de Números Repetidos')
    plt.ylabel('Quantidade de Sorteios')
    
    total = freq_repetencia.sum()
    for i, v in enumerate(freq_repetencia.values):
        plt.text(i, v + (total*0.01), f"{(v/total)*100:.1f}%", ha='center')
        
    print("Abrindo gráfico de repetência... Feche a janela para continuar.")
    plt.show()

def analisar_primos_fibonacci(df_dezenas):
    """Analisa a frequência de números primos e Fibonacci."""
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}
    fibonacci = {1, 2, 3, 5, 8, 13, 21, 34, 55}
    
    qtd_primos = []
    qtd_fibonacci = []
    
    for _, row in df_dezenas.iterrows():
        numeros = set(row.dropna().astype(int))
        qtd_primos.append(len(numeros.intersection(primos)))
        qtd_fibonacci.append(len(numeros.intersection(fibonacci)))
        
    return pd.Series(qtd_primos).value_counts().sort_index(), pd.Series(qtd_fibonacci).value_counts().sort_index()

def gerar_grafico_primos_fibonacci(df_dezenas):
    """Gera gráficos para Primos e Fibonacci."""
    freq_primos, freq_fib = analisar_primos_fibonacci(df_dezenas)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.barplot(x=freq_primos.index, y=freq_primos.values, ax=axes[0], color='orange')
    axes[0].set_title('Frequência de Números Primos por Sorteio')
    axes[0].set_xlabel('Quantidade de Primos')
    axes[0].set_ylabel('Sorteios')
    
    total_p = freq_primos.sum()
    for i, v in enumerate(freq_primos.values):
        axes[0].text(i, v + (total_p*0.01), f"{(v/total_p)*100:.1f}%", ha='center')

    sns.barplot(x=freq_fib.index, y=freq_fib.values, ax=axes[1], color='green')
    axes[1].set_title('Frequência de Números Fibonacci por Sorteio')
    axes[1].set_xlabel('Quantidade de Fibonacci')
    axes[1].set_ylabel('Sorteios')
    
    total_f = freq_fib.sum()
    for i, v in enumerate(freq_fib.values):
        axes[1].text(i, v + (total_f*0.01), f"{(v/total_f)*100:.1f}%", ha='center')
        
    plt.tight_layout()
    print("Abrindo gráficos de Primos e Fibonacci... Feche a janela para continuar.")
    plt.show()

def analise_estatistica(series_numeros):
    """Gera estatísticas matemáticas."""
    contagem = series_numeros.value_counts()
    
    media_geral = series_numeros.mean()
    media_soma = media_geral * 6

    stats = {
        "total_jogos": len(series_numeros) / 6,
        "frequencia": contagem,
        "pares": series_numeros[series_numeros % 2 == 0].count(),
        "impares": series_numeros[series_numeros % 2 != 0].count(),
        "top_10_detalhado": contagem.nlargest(10).to_dict(),
        "bottom_10_detalhado": contagem.nsmallest(10).to_dict(),
        "media_soma": media_soma
    }
    return stats

def consultar_gemini(stats, df_dezenas):
    """Envia os dados para a IA analisar."""
    if not TEM_IA:
        print("\n[ERRO] Configure a chave de API no código para usar esta função.")
        return

    print("\n--- Analisando dados com Gemini... (aguarde) ---")
    
    ciclo_atual, _, faltam_no_ciclo = analisar_ciclo(df_dezenas)
    
    repetencia_stats = analisar_repetencia(df_dezenas)
    moda_repetencia = repetencia_stats.idxmax()
    
    series_atrasos = calcular_atrasos(df_dezenas)
    top_10_atrasados = series_atrasos.nlargest(10).to_dict()
    
    freq_primos, freq_fib = analisar_primos_fibonacci(df_dezenas)
    moda_primos = freq_primos.idxmax()
    moda_fib = freq_fib.idxmax()

    prompt = f"""
    Você é um cientista de dados sênior, especialista em análise de probabilidades e estatística de loterias.
    Sua tarefa é realizar uma análise completa dos resultados históricos da Mega-Sena para a 'Mega da Virada'.

    **DADOS ESTATÍSTICOS COMPLETOS:**
    
    1. **FREQUÊNCIA:**
       - Top 10 "Quentes" (Mais saíram): {stats['top_10_detalhado']}
       - Top 10 "Frios" (Menos saíram): {stats['bottom_10_detalhado']}
       
    2. **ATRASOS (IMPORTANTE):**
       - Os 10 números mais atrasados atualmente (há quantos sorteios não saem): {top_10_atrasados}
       
    3. **CICLO DAS DEZENAS:**
       - Estamos no ciclo {ciclo_atual}.
       - Faltam sair estes números para fechar o ciclo: {faltam_no_ciclo}.
       
    4. **ESTRUTURA DO JOGO (PADRÕES):**
       - Pares/Ímpares: {stats['pares']} pares e {stats['impares']} ímpares no histórico total.
       - Soma das Dezenas (Média): {stats['media_soma']:.2f}
       - Repetência (Do concurso anterior): O padrão mais comum é repetir {moda_repetencia} número(s).
       - Primos: O padrão mais comum é ter {moda_primos} número(s) primo(s) por jogo.
       - Fibonacci: O padrão mais comum é ter {moda_fib} número(s) Fibonacci por jogo.

    **TAREFA DE ANÁLISE E SUGESTÃO:**

    Com base nesses dados, gere 3 palpites estratégicos para a Mega da Virada:

    1. **Palpite Técnico (O "Jogo Perfeito"):**
       - Deve respeitar rigorosamente os padrões de Primos ({moda_primos}), Fibonacci ({moda_fib}) e Repetência ({moda_repetencia}).
       - Deve equilibrar Pares/Ímpares.
    
    2. **Palpite de "Quebra de Ciclo/Atraso":**
       - Dê prioridade total aos números que faltam no ciclo: {faltam_no_ciclo}.
       - Se precisar completar, use os números mais atrasados da lista: {list(top_10_atrasados.keys())}.
       
    3. **Palpite Equilibrado:**
       - Uma mistura inteligente entre os números mais frequentes (quentes) e os que estão devendo (atrasados).

    **SAÍDA ESPERADA:**
    - Forneça os 3 jogos em uma tabela clara.
    - Explique brevemente a lógica de cada jogo escolhido.
    """

    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        
        console = Console()
        print("\n" + "="*40)
        print("INSIGHTS DO GEMINI:")
        print("="*40)
        
        md = Markdown(response.text)
        console.print(md)
        
    except Exception as e:
        print(f"Erro na conexão com Gemini: {e}")

def analisar_jogo_usuario(df_dezenas, stats):
    """Permite que o usuário digite um jogo e a IA analise."""
    if not TEM_IA:
        print("\n[ERRO] Configure a chave de API no código para usar esta função.")
        return

    print("\n--- ANÁLISE DE JOGO PERSONALIZADO ---")
    print("Digite as 6 dezenas do seu jogo (separadas por espaço ou vírgula):")
    entrada = input("> ")
    
    try:
        numeros_usuario = [int(n) for n in entrada.replace(',', ' ').split()]
        numeros_usuario = sorted(list(set(numeros_usuario))) 
        
        if len(numeros_usuario) != 6:
            print(f"\n[ERRO] Você digitou {len(numeros_usuario)} números únicos. Por favor, digite exatamente 6 números entre 01 e 60.")
            return
            
        if any(n < 1 or n > 60 for n in numeros_usuario):
            print("\n[ERRO] Os números devem ser entre 01 e 60.")
            return
            
    except ValueError:
        print("\n[ERRO] Entrada inválida. Digite apenas números.")
        return

    print("\nCalculando métricas do seu jogo...")
    
    soma = sum(numeros_usuario)
    pares = len([n for n in numeros_usuario if n % 2 == 0])
    impares = len([n for n in numeros_usuario if n % 2 != 0])
    
    primos_lista = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}
    fibonacci_lista = {1, 2, 3, 5, 8, 13, 21, 34, 55}
    
    qtd_primos = len(set(numeros_usuario).intersection(primos_lista))
    qtd_fibonacci = len(set(numeros_usuario).intersection(fibonacci_lista))
    
    series_atrasos = calcular_atrasos(df_dezenas)
    atrasos_jogo = {n: series_atrasos.get(n, 0) for n in numeros_usuario}
    
    ciclo_atual, _, faltam_no_ciclo = analisar_ciclo(df_dezenas)
    numeros_do_ciclo = set(numeros_usuario).intersection(set(faltam_no_ciclo))
    
    ultimo_sorteio = set(df_dezenas.iloc[-1].dropna().astype(int))
    repetidos_ultimo = len(set(numeros_usuario).intersection(ultimo_sorteio))
    
    freq_total = stats['frequencia']
    frequencia_jogo = {n: freq_total.get(n, 0) for n in numeros_usuario}

    prompt = f"""
    Você é um especialista em loterias analisando um jogo específico sugerido por um usuário para a Mega-Sena.
    
    **JOGO DO USUÁRIO:** {numeros_usuario}
    
    **ANÁLISE TÉCNICA DO JOGO:**
    1. **Estrutura Básica:**
       - Soma: {soma} (Média histórica é aprox. 183)
       - Pares: {pares} | Ímpares: {impares} (Equilíbrio ideal é 3/3 ou 4/2)
       
    2. **Padrões Avançados:**
       - Primos: {qtd_primos} (Média histórica: 1 a 2)
       - Fibonacci: {qtd_fibonacci} (Média histórica: 0 a 1)
       - Repetidos do último concurso: {repetidos_ultimo} (Média histórica: 0 a 1)
       
    3. **Status dos Números (Contexto Atual):**
       - Atrasos (há quantos jogos não saem): {atrasos_jogo}
       - Frequência histórica (vezes que já saíram): {frequencia_jogo}
       - Números que fecham o ciclo atual: {list(numeros_do_ciclo)} (Se houver algum, é um ponto forte).
       
    **SUA TAREFA:**
    Aja como um consultor amigável e sincero. Analise esse jogo:
    
    1. **O que está bom?** (Ex: equilíbrio par/ímpar, uso de números do ciclo, mistura de quentes/frios).
    2. **O que é arriscado?** (Ex: soma muito alta/baixa, muitos números seguidos, muitos primos, números muito atrasados que nunca saem).
    3. **Veredito:** Dê uma nota de 0 a 10 para esse jogo e uma sugestão rápida de melhoria (ex: "Troque o número X pelo Y para equilibrar a soma").
    """
    
    print("\n--- Enviando para análise do Gemini... ---")
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        
        console = Console()
        print("\n" + "="*40)
        print(f"ANÁLISE DO JOGO: {numeros_usuario}")
        print("="*40)
        
        md = Markdown(response.text)
        console.print(md)
        
    except Exception as e:
        print(f"Erro na conexão com Gemini: {e}")

def menu():
    caminho = "megasena.csv"
    
    if not os.path.exists(caminho):
        print(f"Erro: O arquivo '{caminho}' não foi encontrado na pasta atual.")
        return

    series_numeros, df_dezenas = carregar_dados(caminho)
    
    if series_numeros is None or len(series_numeros) == 0:
        print("Não foi possível extrair dados do arquivo.")
        return

    stats = analise_estatistica(series_numeros)

    while True:
        print("\n" + "-"*30)
        print(" MEGA SENA ANALYTICS ")
        print("-" * 30)
        print("1. Ver os Top 10 Números Mais Sorteados")
        print("2. Ver os 10 Menos Sorteados")
        print("3. Análise de Pares vs Ímpares")
        print("4. Pedir análise para o Gemini (IA)")
        print("5. Gráfico de Frequência (Barras)")
        print("6. Mapa de Calor (Heatmap)")
        print("7. Gráfico de Atrasos (última vez que saiu)")
        print("8. Ciclo das Dezenas (Métrica de Especialista)")
        print("9. Análise de Repetência (Dejà vu)")
        print("10. Filtros de Primos e Fibonacci")
        print("11. Analisar Meu Jogo")
        print("12. Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == '1':
            print("\n--- TOP 10 MAIS SORTEADOS ---")
            df_top = stats['frequencia'].head(10).reset_index()
            df_top.columns = ['Número', 'Frequência']
            print(tabulate(df_top, headers='keys', tablefmt='fancy_grid', showindex=False))
        elif escolha == '2':
            print("\n--- TOP 10 MENOS SORTEADOS ---")
            df_bottom = stats['frequencia'].tail(10).reset_index()
            df_bottom.columns = ['Número', 'Frequência']
            print(tabulate(df_bottom, headers='keys', tablefmt='fancy_grid', showindex=False))
        elif escolha == '3':
            total = stats['pares'] + stats['impares']
            perc_par = (stats['pares'] / total) * 100
            perc_impar = 100 - perc_par
            
            tabela_pares = [
                ["Pares", stats['pares'], f"{perc_par:.1f}%"],
                ["Ímpares", stats['impares'], f"{perc_impar:.1f}%"]
            ]
            print("\n--- ANÁLISE PAR vs ÍMPAR ---")
            print(tabulate(tabela_pares, headers=["Tipo", "Quantidade", "Porcentagem"], tablefmt="fancy_grid"))
        elif escolha == '4':
            consultar_gemini(stats, df_dezenas)
        elif escolha == '5':
            gerar_grafico_frequencia(series_numeros)
        elif escolha == '6':
            gerar_heatmap(df_dezenas)
        elif escolha == '7':
            gerar_grafico_atraso(df_dezenas)
        elif escolha == '8':
            ciclo, tamanho, faltam = analisar_ciclo(df_dezenas)
            print(f"\n--- CICLO DAS DEZENAS ---")
            print(f"Estamos no ciclo: {ciclo}")
            print(f"Tamanho atual do ciclo: {tamanho} sorteios")
            print(f"Faltam sair {len(faltam)} números: {faltam}")
            if len(faltam) <= 3:
                print("ALERTA: Ciclo próximo de fechar! Alta tendência para estes números.")
        elif escolha == '9':
            gerar_grafico_repetencia(df_dezenas)
        elif escolha == '10':
            gerar_grafico_primos_fibonacci(df_dezenas)
        elif escolha == '11':
            analisar_jogo_usuario(df_dezenas, stats)
        elif escolha == '12':
            print("Jogue conscientemente! Boa sorte!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()