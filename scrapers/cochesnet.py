import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            url = f"https://www.coches.net/segunda-mano/{modelo_url}/?PriceFrom={precio_min}&PriceTo={precio_max}"

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        anuncios = soup.find_all('article', class_='Card')

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
                    else:
                        print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en petición coches.net para modelo {modelo}: {e}")

    return resultados
