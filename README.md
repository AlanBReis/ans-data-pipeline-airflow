# Projeto de Web Scraping com Airflow

Este é um projeto que utiliza o Apache Airflow para automatizar o processo de web scraping, com o objetivo de baixar documentos PDF relacionados à atualização do rol de procedimentos da ANS (Agência Nacional de Saúde Suplementar).

## Descrição

O projeto automatiza o download de arquivos PDF disponíveis no portal da ANS, relacionados à atualização do rol de procedimentos, utilizando Airflow. O processo é orquestrado por uma DAG (Directed Acyclic Graph) que coleta os arquivos PDF de um site específico e os armazena localmente.

## Funcionalidades

- **Download de PDFs**: A DAG executa a extração dos links dos PDFs disponíveis na página da ANS.
- **Armazenamento Local**: Os arquivos são baixados e armazenados em uma pasta específica do sistema.
- **Automatização**: A DAG pode ser agendada para rodar periodicamente para manter os arquivos atualizados.

## Pré-requisitos

- Python 3.x
- Apache Airflow
- Bibliotecas Python:
  - `requests`
  - `beautifulsoup4`