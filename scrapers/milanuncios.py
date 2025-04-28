import aiohttp
from bs4 import BeautifulSoup

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            url = f"https://www.milanuncios.com/coches-de-segunda-mano/{modelo_url}.htm?desde={precio_min}&hasta={precio_max}"

            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    anuncios = soup.find_all('div', class_='ad-item')

                    for anuncio in anuncios:
                        titulo_tag = anuncio.find('a', class_='aditem-detail-title')
                        precio_tag = anuncio.find('span', class_='aditem-price')
                        enlace_tag = anuncio.find('a', href=True)

                        if titulo_tag and precio_tag and enlace_tag:
                            titulo = titulo_tag.text.strip()
                            precio = precio_tag.text.strip()
                            enlace = "https://www.milanuncios.com" + enlace_tag['href']

                            resultados.append({
                                'titulo': titulo,
                                'precio': precio,
                                'url': enlace,
                            })

    return resultados
