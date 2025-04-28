import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            for pagina in range(1, 6):  # Ahora miramos hasta 5 páginas
                url = f"https://www.coches.net/segunda-mano/{modelo_url}/?PriceFrom={precio_min}&PriceTo={precio_max}&page={pagina}"

                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        anuncios = soup.find_all('article', class_='Card')

                        if not anuncios:
                            break  # Si ya no hay anuncios, salimos del bucle de páginas

                        for anuncio in anuncios:
                            titulo_tag = anuncio.find('h2', class_='Card-title')
                            precio_tag = anuncio.find('span', class_='Card-price')
                            link_tag = anuncio.find('a', href=True)

                            if titulo_tag and precio_tag and link_tag:
                                titulo = titulo_tag.text.strip()
                                precio = precio_tag.text.strip()
                                enlace = "https://www.coches.net" + link_tag['href']

                                resultados.append({
                                    'titulo': titulo,
                                    'precio': precio,
                                    'url': enlace
                                })

    return resultados
