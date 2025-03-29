from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os

def download_ans_pdfs(**kwargs):
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    attachments = soup.find_all('a', href=True)

    download_folder = '/home/alan/Documentos/Programms/ans-data-pipeline-airflow/downloads' 
    os.makedirs(download_folder, exist_ok=True)

    for attachment in attachments:
        href = attachment['href']
        if href.endswith('.pdf') and 'Anexo' in attachment.text:
            download_url = href if href.startswith('http') else f"{url}{href}"
            file_name = os.path.join(download_folder, attachment.text.strip() + '.pdf')
            file_response = requests.get(download_url)
            with open(file_name, 'wb') as f:
                f.write(file_response.content)
            print(f"Downloaded: {file_name}")

with DAG(
    dag_id='download_ans_pdfs',
    start_date=datetime(2025, 3, 28),
    schedule_interval=None,
    catchup=False
) as dag:
    download_task = PythonOperator(
        task_id='download_ans_pdfs',
        python_callable=download_ans_pdfs
    )