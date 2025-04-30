from bs4 import BeautifulSoup
import aiohttp
import asyncio

MODELOS_COCHESNET = {
    'fiat doblo': 'fiat-doblo',
    'peugeot rifter': 'peugeot-rifter',
    'citroen berlingo': 'citroen-berlingo',
    'ford tourneo courier': 'ford-tourneo-courier'
}

async def buscar_cochesnet_html(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo, url_nombre in modelos.items():
            for page in range(1, 4):
                url = f"https://www.coches.net/segunda-mano/{url_nombre}/?page={page}&PriceFrom={precio_min}&PriceTo={precio_max}"
                print(f"📡 Consultando: {url}")
                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            anuncios = soup.select('div[data-testid="listing-ad-card"]')

                            if not anuncios:
                                print(f"ℹ️ No se encontraron anuncios en página {page} para {modelo}")
                                continue

                            for anuncio in anuncios:
                                titulo = anuncio.select_one('h2')
                                precio = anuncio.select_one('span[data-testid="ad-price"]')
                                link_tag = anuncio.select_one('a')
                                url_anuncio = f"https://www.coches.net{link_tag['href']}" if link_tag else "Sin enlace"

                                resultados.append({
                                    'titulo': titulo.get_text(strip=True) if titulo else "Sin título",
                                    'precio': precio.get_text(strip=True) if precio else "Sin precio",
                                    'url': url_anuncio
                                })
                        elif response.status == 403:
                            print(f"⚠️ Error 403 en petición coches.net para modelo {modelo}")
                        else:
                            print(f"⚠️ Error {response.status} en petición coches.net para modelo {modelo}")
                except Exception as e:
                    print(f"⚠️ Excepción para modelo {modelo} en página {page}: {e}")

    return resultados

# Ejecutar localmente
# asyncio.run(buscar_cochesnet_html(MODELOS_COCHESNET, 4000, 18000))
