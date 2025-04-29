import aiohttp
from bs4 import BeautifulSoup

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            query = modelo.replace(' ', '%20')
            url = f"https://es.wallapop.com/app/search?keywords={query}&filters_source=search_box&price_min={precio_min}&price_max={precio_max}&order_by=newest"

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        anuncios = soup.find_all('a', class_='ItemCardList__itemCard')

                        for anuncio in anuncios:
                            titulo_tag = anuncio.find('span', class_='ItemCardList__item-title')
                            precio_tag = anuncio.find('span', class_='ItemCardList__item-price')

                            if titulo_tag and precio_tag:
                                titulo = titulo_tag.get_text(strip=True)
                                precio = precio_tag.get_text(strip=True)
                                enlace = "https://es.wallapop.com" + anuncio['href']

                                resultados.append({
                                    "titulo": titulo,
                                    "precio": precio,
                                    "url": enlace,
                                })
                    else:
                        print(f"⚠️ Error en petición Wallapop para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción scrapeando Wallapop para {modelo}: {e}")

    return resultados
