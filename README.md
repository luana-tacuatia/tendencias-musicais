# 🎵 Análise de Tendências Musicais com Last.fm

Este repositório é resultado do desenvolvimento de um projeto para a disciplina de **Projeto Integrador IV** dos cursos do eixo de **Computação** da Universidade Virtual do Estado de São Paulo (UNIVESP).

Este projeto permite **explorar, analisar e visualizar tendências musicais** de diferentes países, com foco no **Brasil** e no cenário **Global**, utilizando dados do **Last.fm**. Ele combina **dados históricos semanais**, **visualizações interativas** e **análises de aprendizado de máquina** para identificar padrões, popularidade e previsões de crescimento.

---

## 🌟 Funcionalidades Principais

### 1. **Análise Atual**

- Visualize **Top Músicas**, **Top Artistas** e **Top Gêneros Musicais**.
- Compare **dois países simultaneamente** ou país vs. Mundial.
- Exibição interativa dos dados em **tabelas coloridas**.
- Gráficos que destacam tendências imediatas.

### 2. **Análise Semanal**

- Compare dados de **semanas consecutivas** para o Brasil, Mundial ou ambos.
- Visualize **variações em reproduções e ouvintes**.
- Explore tendências das Top músicas, artistas ou gêneros ao longo do tempo.
- Permite **identificar rapidamente crescimento ou declínio** de popularidade.

### 3. **Descubra Padrões e Tendências**

- Analisa os dados semanais usando **Machine Learning**:
  - **Clustering (K-Means):** identifica grupos de músicas/artistas similares.
  - **Previsão de crescimento:** estima reproduções futuras para os próximos dias.
- Possibilita selecionar **Brasil ou Mundial**, e escolher entre músicas, artistas ou gêneros musicais.
- Visualizações interativas de clusters e tendências.

---

## 🗂 Estrutura do Projeto

```
tendencias-musicais/
│
├─ app.py # Script principal do Streamlit
├─ requirements.txt # Dependências do projeto
├─ README.md # Este arquivo
├─ src/
│ ├─ utils.py # Funções de dados, snapshots semanais e limpeza
│ ├─ render.py # Renderização de tabelas e gráficos
│ ├─ ml_analysis.py # Funções de clustering e previsão
│ ├─ api.py # Comunicação com Last.fm
│ ├─ styles.py # Estilos CSS customizados
│ └─ constants.py # Constantes do projeto (países, cores)
└─ data/ # Snapshots semanais armazenados automaticamente
```

---

## ⚡ Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit:** para criar o painel interativo.
- **Pandas:** manipulação e análise de dados.
- **Altair:** visualizações interativas de gráficos.
- **Scikit-learn:** análise de clusters e previsões.
- **Last.fm API:** dados de músicas, artistas e gêneros.
- **dotenv / Streamlit secrets:** gerenciamento seguro da API key.

---

## 📈 Fluxo de Dados

1. **Consulta Last.fm**
   - Busca dados atuais do Brasil e Mundial (Top músicas, artistas e gêneros).
2. **Snapshot Semanal**
   - Armazena automaticamente os dados em arquivos JSON semanais.
3. **Limpeza Automática**
   - Remove snapshots desnecessários de outros países.
4. **Análise**
   - Tabelas interativas.
   - Gráficos de tendência.
   - Machine Learning (clustering e previsão de crescimento).

---
