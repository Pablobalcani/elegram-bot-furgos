import aiohttp

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    base_url = "https://api.wallapop.com/api/v3/general/search"
    headers = {
        "User-Agent": "Wallapop/4.53.1 Android/7.1.2",
    }

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            params = {
                "keywords": modelo,
                "filters_source": "quick_filters",
                "order_by": "newest",
                "price_min": precio_min,
                "price_max": precio_max,
                "currency": "eur",
                "latitude": 40.4168,    # Opcional: Madrid centro
                "longitude": -3.7038,
                "distance": 200,        # 200 km alrededor
            }

            async with session.get(base_url, headers=headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    items = data.get("search_objects", [])

                    for item in items:
                        title = item.get("title", "Sin título")
                        price = item.get("price", "Sin precio")
                        id = item.get("id")
                        url = f"https://es.wallapop.com/item/{id}"

                        resultados.append({
                            "titulo": title,
                            "precio": price,
                            "url": url,
                        })

    return resultados
