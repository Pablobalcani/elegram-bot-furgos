import aiohttp
from bs4 import BeautifulSoup

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            search_url = f"https://es.wallapop.com/app/search?keywords={modelo}&filters_source=quick_filters"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept-Language": "es-ES,es;q=0.9",
            }

            try:
                async with session.get(search_url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        cards = soup.find_all('article', {'data-testid': 'item-card'})

                        for card in cards:
                            title_tag = card.find('p', {'data-testid': 'item-title'})
                            price_tag = card.find('span', {'data-testid': 'item-price'})
                            link_tag = card.find('a', href=True)

                            if title_tag and price_tag and link_tag:
                                precio = int(price_tag.text.replace('€', '').replace('.', '').strip())
                                if precio_min <= precio <= precio_max:
                                    resultados.append({
                                        "titulo": title_tag.text.strip(),
                                        "precio": f"{precio}€",
                                        "url": f"https://es.wallapop.com{link_tag['href']}"
                                    })
                    else:
                        print(f"⚠️ Error en petición Wallapop para modelo {modelo}: {response.status}")

            except Exception as e:
                print(f"⚠️ Excepción scraping Wallapop para modelo {modelo}: {e}")

    return resultados
