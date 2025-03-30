from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import pdfplumber
import pandas as pd

# Função para compactar arquivos em ZIP
def compactar_zip(download_folder):
    zip_filename = os.path.join(download_folder, 'arquivos_ANS.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(download_folder):
            for file in files:
                if file.endswith('.pdf'):
                    zipf.write(os.path.join(root, file), arcname=file)
    print(f"Arquivos compactados em: {zip_filename}")

# Função para download dos PDFs
def download_ans_pdfs(**kwargs):
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    attachments = soup.find_all('a', href=True)

    download_folder = '/home/alan/Documentos/Programms/ans-data-pipeline-airflow/downloads'
    os.makedirs(download_folder, exist_ok=True)

    # Baixando os arquivos PDF
    for attachment in attachments:
        href = attachment['href']
        if href.endswith('.pdf') and 'Anexo' in attachment.text:
            download_url = href if href.startswith('http') else f"{url}{href}"
            file_name = os.path.join(download_folder, attachment.text.strip() + '.pdf')
            file_response = requests.get(download_url)
            with open(file_name, 'wb') as f:
                f.write(file_response.content)
            print(f"Downloaded: {file_name}")

    # Compactando os arquivos após o download
    compactar_zip(download_folder)

def extract_and_process_anexo_i(**kwargs):
    download_folder = '/home/alan/Documentos/Programms/ans-data-pipeline-airflow/downloads'
    pdf_path = os.path.join(download_folder, 'Anexo I..pdf')
    extract_pdf_to_csv(pdf_path, 'rol_procedimentos_anexo_i.csv', download_folder)


def extract_pdf_to_csv(pdf_path, csv_name, download_folder):
    if not os.path.exists(pdf_path):
        print(f"Arquivo PDF não encontrado: {pdf_path}")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    all_tables.append(table)
            if not all_tables:
                print(f"Nenhuma tabela encontrada em {pdf_path}")
                return
            df = pd.DataFrame([row for table in all_tables for row in table[1:]], columns=all_tables[0][0])
            df.replace({'OD': 'Outros Procedimentos', 'AMB': 'Ambulatorial'}, inplace=True)
            csv_path = os.path.join(download_folder, csv_name)
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"CSV salvo em: {csv_path}")
            zip_filename = os.path.join(download_folder, f"Teste_Alan_Reis_{csv_name.replace('.csv','')}.zip")
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(csv_path, arcname=csv_name)
            print(f"Zip salvo em: {zip_filename}")
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")

with DAG(
    dag_id='download_ans_pdfs',
    start_date=datetime(2025, 3, 28),
    schedule=None,
    catchup=False
) as dag:
    download_task = PythonOperator(
        task_id='download_ans_pdfs',
        python_callable=download_ans_pdfs
    )
    extract_anexo_i_task = PythonOperator(
        task_id='extract_and_process_anexo_i',
        python_callable=extract_and_process_anexo_i
    )
    download_task >> [extract_anexo_i_task]