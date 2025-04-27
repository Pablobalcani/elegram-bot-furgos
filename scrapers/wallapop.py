import aiohttp

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Wallapop/1.0.0 (Linux; Android 10)",
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            start = 0
            limit = 20  # número de resultados por página
            max_paginas = 5  # número máximo de páginas a recorrer por modelo

            for pagina in range(max_paginas):
                params = {
                    "keywords": modelo,
                    "price_min": precio_min,
                    "price_max": precio_max,
                    "order_by": "newest",
                    "latitude": 40.416775,
                    "longitude": -3.703790,
                    "distance": 50000,
                    "start": start,
                    "num": limit,
                }
                url = "https://api.wallapop.com/api/v3/items"

                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            items = data.get("items", [])

                            if not items:
                                break  # No más resultados

                            for item in items:
                                titulo = item.get('title', 'Sin título')
                                precio = item.get('price', 0)
                                enlace = f"https://es.wallapop.com/item/{item.get('id', '')}"

                                resultados.append({
                                    "titulo": titulo,
                                    "precio": f"{precio}€",
                                    "url": enlace,
                                })

                            start += limit  # Incrementamos el start para la siguiente página
                        else:
                            print(f"⚠️ Error en petición Wallapop para modelo {modelo}: {response.status}")
                            break
                except Exception as e:
                    print(f"❌ Excepción buscando {modelo} en Wallapop: {e}")
                    break

    return resultados
