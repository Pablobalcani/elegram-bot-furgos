import aiohttp

async def buscar_cochesnet(modelos_ids, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.coches.net",
        "Referer": "https://www.coches.net/",
        "X-Schibsted-Tenant": "coches",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo, (make_id, model_id) in modelos_ids.items():
            url = f"https://web.gw.coches.net/semantic/segunda-mano/?MakeIds%5B0%5D={make_id}&ModelIds%5B0%5D={model_id}"

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data.get('listAds', [])

                        for anuncio in anuncios:
                            price = anuncio.get('price', 0)
                            if precio_min <= price <= precio_max:
                                resultados.append({
                                    "titulo": anuncio.get('title', 'Sin título'),
                                    "precio": f"{price}€",
                                    "url": anuncio.get('urls', {}).get('web', '')
                                })
                    elif response.status == 404:
                        print(f"ℹ️ No hay coches disponibles para {modelo} (404).")
                    else:
                        print(f"⚠️ Error inesperado coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en petición coches.net para {modelo}: {e}")

    return resultados
