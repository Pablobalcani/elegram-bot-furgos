import aiohttp
from bs4 import BeautifulSoup

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            url = f"https://www.milanuncios.com/coches-de-segunda-mano/{modelo.replace(' ', '-')}.htm?desde={precio_min}&hasta={precio_max}"
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    anuncios = soup.find_all('div', class_='aditem')

                    for anuncio in anuncios:
                        titulo_tag = anuncio.find('a', class_='aditem-detail-title')
                        precio_tag = anuncio.find('span', class_='aditem-price')

                        if titulo_tag and precio_tag:
                            titulo = titulo_tag.text.strip()
                            precio = precio_tag.text.strip()
                            enlace = "https://www.milanuncios.com" + titulo_tag.get('href')

                            resultados.append({
                                'titulo': titulo,
                                'precio': precio,
                                'url': enlace
                            })

    return resultados
