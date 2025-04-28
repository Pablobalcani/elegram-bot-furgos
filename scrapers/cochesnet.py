import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            url = f"https://www.coches.net/segunda-mano/{modelo_url}/?PriceFrom={precio_min}&PriceTo={precio_max}"

            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    anuncios = soup.find_all('a', class_='Card-title-link')

                    for anuncio in anuncios:
                        titulo = anuncio.text.strip()
                        enlace = "https://www.coches.net" + anuncio['href']

                        precio_tag = anuncio.find_parent('div', class_='Card-content').find('span', class_='Card-price')
                        precio = precio_tag.text.strip() if precio_tag else "Precio no disponible"

                        resultados.append({
                            'titulo': titulo,
                            'precio': precio,
                            'url': enlace
                        })
                else:
                    print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")

    return resultados
