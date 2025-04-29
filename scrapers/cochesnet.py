import aiohttp

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo, (make_id, model_id) in modelos.items():
            url = f"https://web.gw.coches.net/semantic/segunda-mano/?MakeIds%5B0%5D={make_id}&ModelIds%5B0%5D={model_id}"
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data[0].get('listAds', []) if isinstance(data, list) and data else []
                        for anuncio in anuncios:
                            resultados.append({
                                'titulo': anuncio.get('title', 'Sin título'),
                                'precio': f"{anuncio.get('price', 0)}€",
                                'url': anuncio.get('url', '')
                            })
                    elif response.status == 404:
                        print(f"ℹ️ No hay coches disponibles para {modelo} (404).")
                    else:
                        print(f"⚠️ Error inesperado coches.net para {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en coches.net para {modelo}: {e}")
    return resultados
