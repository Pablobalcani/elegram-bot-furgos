import aiohttp

MODELOS_IDS = {
    "rifter": (50, 30883),
    "berlingo": (11, 1831),
    "tourneo courier": (27, 29807),
    "doblo": (26, 1909)
}

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            modelo_normalizado = modelo.lower().strip().replace(" combi", "")
            make_id, model_id = MODELOS_IDS.get(modelo_normalizado, (None, None))
            if not make_id or not model_id:
                print(f"⚠️ IDs no encontrados para modelo {modelo}")
                continue

            url = (
                f"https://web.gw.coches.net/semantic/segunda-mano/"
                f"?MakeIds[0]={make_id}&ModelIds[0]={model_id}"
                f"&PriceFrom={precio_min}&PriceTo={precio_max}"
            )

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data.get("listAds", [])

                        for anuncio in anuncios:
                            titulo = anuncio.get('model', 'Sin título')
                            precio = anuncio.get('price', 0)
                            enlace = f"https://www.coches.net{anuncio.get('url', '')}"

                            resultados.append({
                                'titulo': titulo,
                                'precio': f"{precio} €",
                                'url': enlace
                            })
                    else:
                        print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción buscando en coches.net: {e}")

    return resultados
