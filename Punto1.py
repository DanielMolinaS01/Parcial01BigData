import json
import urllib.request
import boto3
from datetime import datetime


def lambda_handler(event, context):
    url1 = "https://www.eltiempo.com/"
    url2 = "https://www.publimetro.co/"

    response1 = urllib.request.urlopen(url1)
    response2 = urllib.request.urlopen(url2)

    html_content1 = response1.read()
    html_content2 = response2.read()

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    s3 = boto3.client('s3')

    bucket = 'parcial01'

    archivo1 = f"El_Tiempo-{fecha_hoy}.html"
    archivo2 = f"Publimetro-{fecha_hoy}.html"

    s3.put_object(Bucket=bucket, Key=f"news/raw/{archivo1}", Body=html_content1)
    s3.put_object(Bucket=bucket, Key=f"news/raw/{archivo2}", Body=html_content2)