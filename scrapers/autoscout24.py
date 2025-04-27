import aiohttp
from bs4 import BeautifulSoup

async def buscar_autoscout24(modelos, precio_min, precio_max, paginas=3):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(" ", "%20")
            for pagina in range(1, paginas + 1):
                url = (
                    f"https://www.autoscout24.es/lst/?sort=standard&desc=0&cy=E&"
                    f"search_id=&makeModelVariant1.modelDescription={modelo_url}"
                    f"&pricefrom={precio_min}&priceto={precio_max}&page={pagina}"
                )
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        anuncios = soup.find_all('article', class_='cl-list-element')

                        for anuncio in anuncios:
                            try:
                                titulo_tag = anuncio.find('h2')
                                precio_tag = anuncio.find('span', class_='cldt-price')
                                km_ano_tags = anuncio.find_all('span', class_='cldt-stage-basic-data')

                                enlace_tag = anuncio.find('a', href=True)

                                titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no disponible"
                                precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

                                kms = "Km no disponible"
                                ano = "Año no disponible"
                                if km_ano_tags:
                                    if len(km_ano_tags) >= 2:
                                        kms = km_ano_tags[0].get_text(strip=True)
                                        ano = km_ano_tags[1].get_text(strip=True)

                                enlace = "https://www.autoscout24.es" + enlace_tag['href'] if enlace_tag else "URL no disponible"

                                resultados.append({
                                    'titulo': titulo,
                                    'precio': precio,
                                    'kilometros': kms,
                                    'anio': ano,
                                    'url': enlace
                                })
                            except Exception as e:
                                print(f"Error procesando anuncio AutoScout24: {e}")

    return resultados
