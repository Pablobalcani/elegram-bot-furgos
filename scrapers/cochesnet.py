import aiohttp

MODELOS_COCHESNET = {
    "rifter": {"make_id": 15, "model_id": 1127},
    "berlingo combi": {"make_id": 14, "model_id": 730},
    "tourneo courier": {"make_id": 19, "model_id": 2642},
    "doblo": {"make_id": 13, "model_id": 654},
}

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            ids = MODELOS_COCHESNET.get(modelo.lower())
            if not ids:
                print(f"⚠️ No se encontraron IDs para modelo {modelo}")
                continue

            url = (
                f"https://web.gw.coches.net/semantic/segunda-mano/"
                f"?MakeIds[]={ids['make_id']}&ModelIds[]={ids['model_id']}"
                f"&PriceFrom={precio_min}&PriceTo={precio_max}"
            )

            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        for car in data.get('items', []):
                            resultados.append({
                                'titulo': car.get('title', 'Sin título'),
                                'precio': f"{car.get('price', 'N/A')}€",
                                'url': f"https://www.coches.net{car.get('url', '')}",
                            })
                    else:
                        print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Error procesando coches.net para modelo {modelo}: {e}")

    return resultados
