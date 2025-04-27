
import requests
from bs4 import BeautifulSoup

def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []
    url = 'https://www.coches.net/segunda-mano/?MaxPrice=8000&SortField=price&SortDirection=asc'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            anuncios = soup.select('article')

            for anuncio in anuncios:
                titulo = anuncio.select_one('.card-title')
                precio_texto = anuncio.select_one('.price')

                if titulo and precio_texto:
                    titulo_text = titulo.get_text(strip=True).lower()
                    precio_num = ''.join(filter(str.isdigit, precio_texto.get_text()))
                    precio = int(precio_num) if precio_num else 999999

                    if any(modelo in titulo_text for modelo in modelos) and precio_min <= precio <= precio_max:
                        link_tag = anuncio.select_one('a')
                        if link_tag and 'href' in link_tag.attrs:
                            link = "https://www.coches.net" + link_tag['href']
                            resultados.append(f"{titulo_text.title()}\nPrecio: {precio}€\n{link}")

    except Exception as e:
        print(f"Error en Coches.net: {e}")
    
    return resultados
