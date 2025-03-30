# Projeto de Web Scraping e Extração de Dados da ANS com Airflow

Este projeto utiliza o Apache Airflow para automatizar o processo de web scraping e extração de dados de arquivos PDF, com o objetivo de coletar informações sobre a atualização do rol de procedimentos da ANS (Agência Nacional de Saúde Suplementar).

## Descrição

O projeto automatiza o download de arquivos PDF disponíveis no portal da ANS, relacionados à atualização do rol de procedimentos. Além do download, o projeto extrai dados das tabelas presentes nos PDFs, converte esses dados em arquivos CSV e compacta os arquivos CSV em arquivos ZIP. O processo é orquestrado por uma DAG (Directed Acyclic Graph) no Airflow.

## Funcionalidades

-   **Download de PDFs**: A DAG executa a extração dos links dos PDFs disponíveis na página da ANS e baixa os arquivos.
-   **Extração de Dados PDF**: Os dados das tabelas nos arquivos PDF são extraídos e convertidos em DataFrames do pandas.
-   **Geração de Arquivos CSV**: Os DataFrames são salvos como arquivos CSV, facilitando a análise e o uso dos dados.
-   **Compactação em ZIP**: Os arquivos CSV gerados são compactados em arquivos ZIP para facilitar o armazenamento e a transferência.
-   **Automatização**: A DAG pode ser agendada para rodar periodicamente, mantendo os dados atualizados.

## Pré-requisitos

-   Python 3
-   Apache Airflow
-   Bibliotecas Python:
    -   requests
    -   beautifulsoup4
    -   pdfplumber
    -   pandas
    -   zipfile

## Instalação

1.  Clone este repositório:

    ```bash
    git clone https://github.com/AlanBReis/ans-data-pipeline-airflow.git
    cd ans-data-pipeline-airflow
    ```

2.  Instale as dependências:

    ```bash
    pip install requirements.txt
    ```

3.  Configure o Airflow (se necessário).
4.  Coloque a DAG na pasta `dags` do Airflow.

## Uso

1.  Inicie o Airflow.
2.  Ative a DAG no Airflow UI.
3.  A DAG irá executar o processo de download, extração e compactação automaticamente.
4.  Os arquivos CSV e ZIP gerados estarão na pasta Downloads.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)