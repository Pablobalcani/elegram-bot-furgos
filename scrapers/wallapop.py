import aiohttp

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Wallapop/1.0.0 (Linux; Android 10)",
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            params = {
                "keywords": modelo,
                "price_min": precio_min,
                "price_max": precio_max,
                "order_by": "newest",
                "latitude": 40.416775,  # Coordenadas (puedes cambiarlo)
                "longitude": -3.703790,
                "distance": 50000,  # 50 km alrededor
            }
            url = "https://api.wallapop.com/api/v3/items"

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])

                    for item in items:
                        titulo = item.get('title', 'Sin título')
                        precio = item.get('price', 0)
                        enlace = f"https://es.wallapop.com/item/{item.get('id', '')}"

                        resultados.append({
                            "titulo": titulo,
                            "precio": f"{precio}€",
                            "url": enlace,
                        })

    return resultados
