# Análise de Dados da Mega Sena com IA

Este projeto é uma ferramenta de análise de dados para os sorteios da Mega Sena. Ele utiliza bibliotecas de ciência de dados do Python para processar o histórico de resultados e integra a Inteligência Artificial do Google (Gemini) para fornecer insights e análises estatísticas avançadas.

## 🚀 Funcionalidades

- **Carregamento de Dados**: Leitura e processamento de arquivos CSV com histórico de sorteios.
- **Análise Estatística**: Cálculo de frequência de números, dezenas mais e menos sorteadas.
- **Visualização de Dados**: Geração de gráficos de barras para visualizar a frequência dos números.
- **Integração com IA**: Utiliza o Google Gemini para responder perguntas sobre os dados e gerar insights.
- **Interface Interativa**: Menu de opções no terminal para fácil navegação.

## 📋 Pré-requisitos

- Python 3.8 ou superior instalado.
- Uma conta no Google para gerar a chave da API do Gemini.

## 🔧 Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

### 1. Clonar o Repositório

```bash
git clone https://github.com/Wagner-V1eira/analise-dados-megasena.git
cd analise-dados-megasena
```

### 2. Criar um Ambiente Virtual

É recomendável usar um ambiente virtual para isolar as dependências do projeto.

**No Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

## 🔑 Configuração da API (Google AI Studio)

Para utilizar as funcionalidades de IA, você precisará de uma chave de API do Google Gemini.

### Passo a Passo para Obter a Chave:

1.  Acesse o [Google AI Studio](https://aistudio.google.com/).
2.  Faça login com sua conta do Google.
3.  Clique no botão **"Get API key"** (ou "Criar chave de API") no menu lateral ou superior.
4.  Clique em **"Create API key in new project"**.
5.  Copie a chave gerada (ela começa com `AIza...`).

### Configurando o Projeto:

1.  Na pasta raiz do projeto, você encontrará um arquivo chamado `.env.example`.
2.  Renomeie este arquivo para `.env` ou crie um novo arquivo `.env` e copie o conteúdo.
3.  Abra o arquivo `.env` em um editor de texto.
4.  Substitua `Sua_Chave_Aqui` pela chave que você copiou do Google AI Studio.

O arquivo `.env` deve ficar assim:

```env
GOOGLE_API_KEY=AIzaSyBLHpvr6hOT7k9p7OmoeFRpn8mzWeI_2Zw...
```

> **Nota:** O arquivo `.env` contém informações sensíveis e **não deve** ser compartilhado ou enviado para o GitHub. Ele já está configurado no `.gitignore` para ser ignorado.

## ▶️ Como Executar

Certifique-se de que o ambiente virtual está ativado e o arquivo `megasena.csv` está na pasta do projeto.

```bash
python mega.py
```

Siga as instruções apresentadas no menu do terminal para interagir com a ferramenta.

## 📂 Estrutura do Projeto

- `mega.py`: Código fonte principal da aplicação.
- `megasena.csv`: Arquivo de dados com os resultados (necessário baixar ou atualizar).
- `requirements.txt`: Lista de dependências do Python.
- `.env`: Arquivo de configuração de variáveis de ambiente (não versionado).
- `.gitignore`: Arquivos e pastas ignorados pelo Git.

## 🤝 Contribuição

Sinta-se à vontade para abrir issues e pull requests para melhorias no código ou novas funcionalidades.
