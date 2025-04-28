import aiohttp
from bs4 import BeautifulSoup

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            for pagina in range(1, 6):  # Hasta 5 páginas
                url = f"https://www.milanuncios.com/coches-de-segunda-mano/{modelo_url}.htm?desde={precio_min}&hasta={precio_max}&pagina={pagina}"

                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        anuncios = soup.find_all('div', class_='aditem')

                        if not anuncios:
                            break  # Si no hay anuncios, parar paginación

                        for anuncio in anuncios:
                            titulo_tag = anuncio.find('a', class_='aditem-detail-title')
                            precio_tag = anuncio.find('span', class_='aditem-price')
                            link_tag = titulo_tag

                            if titulo_tag and precio_tag and link_tag:
                                titulo = titulo_tag.text.strip()
                                precio = precio_tag.text.strip()
                                enlace = "https://www.milanuncios.com" + link_tag.get('href')

                                resultados.append({
                                    'titulo': titulo,
                                    'precio': precio,
                                    'url': enlace
                                })

    return resultados
