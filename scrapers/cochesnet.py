from bs4 import BeautifulSoup
import aiohttp
import asyncio

# URLs estáticas basadas en los modelos específicos
URLS_COCHESNET = {
    "rifter": "https://www.coches.net/segunda-mano/?MakeIds%5B0%5D=33&ModelIds%5B0%5D=1252",
    "berlingo combi": "https://www.coches.net/segunda-mano/?MakeIds%5B0%5D=15&ModelIds%5B0%5D=1127",
    "tourneo courier": "https://www.coches.net/segunda-mano/?MakeIds%5B0%5D=14&ModelIds%5B0%5D=694"
}

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo, url_base in URLS_COCHESNET.items():
            for page in range(1, 4):
                url = f"{url_base}&page={page}&PriceFrom={precio_min}&PriceTo={precio_max}"
                print(f"📡 Consultando: {url}")

                try:
                    async with session.get(url) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, "html.parser")
                            anuncios = soup.select("div.card")

                            if not anuncios:
                                print(f"ℹ️ No se encontraron anuncios en página {page} para {modelo}")
                                continue

                            for anuncio in anuncios:
                                titulo = anuncio.select_one("h2.card-title")
                                precio = anuncio.select_one("span.price")
                                enlace = anuncio.select_one("a")

                                if titulo and precio and enlace:
                                    resultados.append({
                                        "titulo": titulo.text.strip(),
                                        "precio": precio.text.strip(),
                                        "url": "https://www.coches.net" + enlace["href"]
                                    })
                        else:
                            print(f"⚠️ Error {response.status} en petición coches.net para modelo {modelo}")
                except Exception as e:
                    print(f"⚠️ Excepción en petición coches.net para modelo {modelo}: {e}")

    return resultados
