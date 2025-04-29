import aiohttp

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    # Mapeo de los modelos a sus MakeId y ModelId reales
    modelo_a_ids = {
        'rifter': (33, 1252),
        'berlingo combi': (15, 1127),
        'tourneo courier': (14, 694),
        'doblo': (15, 300),
    }

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            ids = modelo_a_ids.get(modelo.lower())
            if not ids:
                print(f"⚠️ IDs no encontrados para modelo {modelo}")
                continue

            make_id, model_id = ids
            url = f"https://web.gw.coches.net/semantic/segunda-mano/?MakeIds%5B0%5D={make_id}&ModelIds%5B0%5D={model_id}"

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data[0].get('listAds', []) if isinstance(data, list) and data else []

                        for anuncio in anuncios:
                            titulo = anuncio.get('title', 'Sin título')
                            precio = anuncio.get('price', 0)
                            enlace = anuncio.get('url', '')

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
                print(f"⚠️ Excepción en petición coches.net para {modelo}: {e}")

    return resultados
