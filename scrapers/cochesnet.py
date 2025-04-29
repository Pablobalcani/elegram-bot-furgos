import aiohttp

MAKE_MODEL_IDS = {
    'rifter': (33, 1252),
    'berlingo combi': (11, 189),
    'tourneo courier': (15, 1127),
    'doblo': (14, 694),
}

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            ids = MAKE_MODEL_IDS.get(modelo.lower())
            if not ids:
                print(f"⚠️ IDs no encontrados para modelo {modelo}")
                continue
            make_id, model_id = ids

            url = f"https://web.gw.coches.net/semantic/segunda-mano/?MakeIds[0]={make_id}&ModelIds[0]={model_id}"

            async with session.get(url) as response:
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
 