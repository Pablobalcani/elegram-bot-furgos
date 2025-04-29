import aiohttp

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Wallapop/1.0.0 (Linux; Android 10)",  # Móvil simulado
    }

    search_url = "https://api.wallapop.com/api/v3/general/search"

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            payload = {
                "keywords": modelo,
                "filters": {
                    "price": {
                        "min": precio_min,
                        "max": precio_max
                    }
                },
                "order_by": "newest",
                "latitude": 40.416775,
                "longitude": -3.703790,
                "distance": 50000  # 50km
            }

            try:
                async with session.post(search_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("search_objects", [])

                        for item in items:
                            titulo = item.get('title', 'Sin título')
                            precio = item.get('price', 0)
                            item_id = item.get('id', '')

                            enlace = f"https://es.wallapop.com/item/{item_id}"

                            resultados.append({
                                "titulo": titulo,
                                "precio": f"{precio}€",
                                "url": enlace,
                            })
                    else:
                        print(f"⚠️ Error en petición Wallapop para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción buscando en Wallapop para {modelo}: {e}")

    return resultados
