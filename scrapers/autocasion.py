import aiohttp
from bs4 import BeautifulSoup

async def buscar_autocasion(modelos, precio_min, precio_max, paginas=3):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(" ", "-").lower()
            for pagina in range(1, paginas + 1):
                url = f"https://www.autocasion.com/coches-segunda-mano/{modelo_url}?pagina={pagina}&precio-desde={precio_min}&precio-hasta={precio_max}"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        anuncios = soup.find_all('article', class_='content')

                        for anuncio in anuncios:
                            try:
                                titulo_tag = anuncio.find('h2', class_='title')
                                precio_tag = anuncio.find('span', class_='price')
                                km_tag = anuncio.find('li', class_='kms')
                                ano_tag = anuncio.find('li', class_='year')
                                enlace_tag = anuncio.find('a', href=True)

                                titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no disponible"
                                precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"
                                kms = km_tag.get_text(strip=True) if km_tag else "Km no disponible"
                                ano = ano_tag.get_text(strip=True) if ano_tag else "Año no disponible"
                                enlace = "https://www.autocasion.com" + enlace_tag['href'] if enlace_tag else "URL no disponible"

                                resultados.append({
                                    'titulo': titulo,
                                    'precio': precio,
                                    'kilometros': kms,
                                    'anio': ano,
                                    'url': enlace
                                })
                            except Exception as e:
                                print(f"Error procesando anuncio: {e}")

    return resultados
