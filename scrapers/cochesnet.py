import aiohttp

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.coches.net/",
        "Origin": "https://www.coches.net",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo, (make_id, model_id) in modelos.items():
            url = (
                f"https://web.gw.coches.net/semantic/segunda-mano/"
                f"?MakeIds%5B0%5D={make_id}&ModelIds%5B0%5D={model_id}"
                f"&PriceFrom={precio_min}&PriceTo={precio_max}"
            )
            print(f"📡 Consultando: {url}")

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, list) and data:
                            anuncios = data[0].get("listAds", [])
                        else:
                            anuncios = []

                        for anuncio in anuncios:
                            titulo = anuncio.get("title", "Sin título")
                            precio = anuncio.get("price", 0)
                            enlace = anuncio.get("url", "")

                            resultados.append({
                                "titulo": titulo,
                                "precio": f"{precio}€",
                                "url": enlace
                            })

                    elif response.status == 404:
                        print(f"ℹ️ No hay coches disponibles para {modelo} (404).")
                    else:
                        print(f"⚠️ Error inesperado para {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en {modelo}: {e}")

    return resultados
