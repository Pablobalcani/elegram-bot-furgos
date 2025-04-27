
import requests
from bs4 import BeautifulSoup

def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []
    url = 'https://www.milanuncios.com/furgonetas-de-segunda-mano/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            anuncios = soup.select('.aditem')

            for anuncio in anuncios:
                titulo = anuncio.select_one('.aditem-detail-title')
                precio_texto = anuncio.select_one('.aditem-price')

                if titulo and precio_texto:
                    titulo_text = titulo.get_text(strip=True).lower()
                    precio_num = ''.join(filter(str.isdigit, precio_texto.get_text()))
                    precio = int(precio_num) if precio_num else 999999

                    if any(modelo in titulo_text for modelo in modelos) and precio_min <= precio <= precio_max:
                        link = anuncio.select_one('a')['href']
                        if not link.startswith('http'):
                            link = 'https://www.milanuncios.com' + link
                        resultados.append(f"{titulo_text.title()}\nPrecio: {precio}€\n{link}")

    except Exception as e:
        print(f"Error en Milanuncios: {e}")
    
    return resultados
