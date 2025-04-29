import aiohttp

async def buscar_cochesnet(modelos_cochesnet, precio_min, precio_max):
    resultados = []

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; Bot/1.0; +https://github.com)",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo, (make_id, model_id) in modelos_cochesnet.items():
            url = f"https://web.gw.coches.net/semantic/segunda-mano/?MakeIds%5B0%5D={make_id}&ModelIds%5B0%5D={model_id}&PriceFrom={precio_min}&PriceTo={precio_max}"

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data.get('listAds', [])

                        for anuncio in anuncios:
                            titulo = anuncio.get('title', 'Sin título')
                            precio = anuncio.get('price', 0)
                            enlace = anuncio.get('url', '')

                            if enlace:
                                enlace = "https://coches.net" + enlace

                            resultados.append({
                                'titulo': titulo,
                                'precio': f"{precio}€",
                                'url': enlace
                            })

                    elif response.status == 404:
                        print(f"ℹ️ No hay coches disponibles para {modelo} (404).")
                    else:
                        print(f"⚠️ Error inesperado coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en coches.net para {modelo}: {e}")

    return resultados
