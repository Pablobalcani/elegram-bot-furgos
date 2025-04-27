import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max, paginas=3):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')

            for pagina in range(1, paginas + 1):
                url = (
                    f"https://www.coches.net/segunda-mano/{modelo_url}/"
                    f"?PriceFrom={precio_min}&PriceTo={precio_max}&page={pagina}"
                )

                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        anuncios = soup.find_all('article', class_='Card')

                        if not anuncios:
                            break  # Si no hay anuncios, no seguimos paginando

                        for anuncio in anuncios:
                            titulo_tag = anuncio.find('h2', class_='Card-title')
                            precio_tag = anuncio.find('span', class_='Card-price')
                            link_tag = anuncio.find('a', href=True)

                            # Año y km pueden estar en el bloque Card-infoKilometers
                            info_tag = anuncio.find('div', class_='Card-infoKilometers')

                            if titulo_tag and precio_tag and link_tag:
                                titulo = titulo_tag.get_text(strip=True)
                                precio = precio_tag.get_text(strip=True)
                                enlace = "https://www.coches.net" + link_tag['href']

                                anio_kms = info_tag.get_text(strip=True) if info_tag else "Datos no disponibles"

                                resultados.append({
                                    'titulo': titulo,
                                    'precio': precio,
                                    'anio_kilometros': anio_kms,
                                    'url': enlace
                                })

    return resultados
