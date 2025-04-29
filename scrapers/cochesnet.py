import aiohttp

MAKE_MODEL_IDS = {
    'rifter': (33, 1252),
    'berlingo combi': (11, 189),
    'tourneo courier': (15, 1127),
    'doblo': (14, 694),
}

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.coches.net",
        "Referer": "https://www.coches.net/",
        "x-adevinta-channel": "web-desktop",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            ids = MAKE_MODEL_IDS.get(modelo.lower())
            if not ids:
                print(f"⚠️ IDs no encontrados para modelo {modelo}")
                continue
            make_id, model_id = ids

            url = "https://web.gw.coches.net/semantic/segunda-mano/"
            params = {
                "MakeIds[0]": make_id,
                "ModelIds[0]": model_id,
                "PriceFrom": precio_min,
                "PriceTo": precio_max,
            }

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    anuncios = data.get('listAds', [])

                    for anuncio in anuncios:
                        titulo = anuncio.get('title', 'Sin título')
                        precio = anuncio.get('price', 'Sin precio')
                        enlace = f"https://www.coches.net{anuncio.get('url', '')}"

                        resultados.append({
                            'titulo': titulo,
                            'precio': f"{precio}€",
                            'url': enlace
                        })
                else:
                    print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")

    return resultados
