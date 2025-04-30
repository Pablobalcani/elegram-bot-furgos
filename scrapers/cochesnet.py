import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max, paginas=3):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')

            for pagina in range(1, paginas + 1):
                url = f"https://www.coches.net/segunda-mano/{modelo_url}/?page={pagina}&PriceFrom={precio_min}&PriceTo={precio_max}"
                print(f"📡 Consultando: {url}")

                try:
                    async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                        if response.status != 200:
                            print(f"⚠️ Error {response.status} en petición coches.net para modelo {modelo}")
                            continue

                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        anuncios = soup.find_all('article', class_='Card')

                        for anuncio in anuncios:
                            titulo_tag = anuncio.find('h2', class_='Card-title')
                            precio_tag = anuncio.find('span', class_='Card-price')
                            link_tag = anuncio.find('a', href=True)

                            if titulo_tag and precio_tag and link_tag:
                                resultados.append({
                                    'titulo': titulo_tag.text.strip(),
                                    'precio': precio_tag.text.strip(),
                                    'url': "https://www.coches.net" + link_tag['href']
                                })

                except Exception as e:
                    print(f"❌ Excepción al procesar {url}: {e}")

    return resultados
