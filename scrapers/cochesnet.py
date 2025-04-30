import aiohttp
from bs4 import BeautifulSoup

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-').lower()
            for page in range(1, 4):  # 3 primeras páginas
                url = f"https://www.coches.net/segunda-mano/{modelo_url}/?page={page}&PriceFrom={precio_min}&PriceTo={precio_max}"
                print(f"📡 Consultando: {url}")

                try:
                    async with session.get(url, headers=headers) as response:
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
                            print(f"⚠️ Error {response.status} en petición coches.net para modelo {modelo}")
                except Exception as e:
                    print(f"⚠️ Excepción en petición coches.net para {modelo}: {e}")

    return resultados
