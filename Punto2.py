import requests
from bs4 import BeautifulSoup
import csv
import boto3
from datetime import datetime

url1 = 'https://www.eltiempo.com/'
url2 = 'https://www.publimetro.co/'

pagina1 = requests.get(url1)
pagina2 = requests.get(url2)

soup1 = BeautifulSoup(pagina1.content, 'html.parser')
soup2 = BeautifulSoup(pagina2.content, 'html.parser')

bucket = parcial01
s3 = boto3.client('s3')
fecha_hoy = datetime.now().strftime("%Y-%m-%d")

titularesTiempo = soup1.find_all('h2') #h2 haciendo referencia a html
titularesPublimetro = soup2.find_all('h2')
datos = []

for titular in titularesTiempo:

        textoTiempo_titular = titular.text.strip()
        enlaceTiempo_titular = titular.a['href']
        datos.append((textoTiempo_titular, enlaceTiempo_titular))

for titular in titularesPublimetro:

        textoPublimetro_titular = titular.text.strip()
        enlacePublimetro_titular = titular.a['href']
        datos.append((textoPublimetro_titular, enlacePublimetro_titular))

with open('titulares.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Titular', 'Enlace'])
            csv_writer.writerows(datos)

archivo1 = f"El_Tiempo-{fecha_hoy}.csv"
archivo2 = f"Publimetro-{fecha_hoy}.csv"

s3.put_object(Bucket=bucket, Key=f"news/raw/{archivo1}", Body=datos)
s3.put_object(Bucket=bucket, Key=f"news/raw/{archivo2}", Body=datos)