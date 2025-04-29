import aiohttp

async def buscar_wallapop(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            url = "https://api.wallapop.com/api/v3/general/search"
            params = {
                "keywords": modelo,
                "price_min": precio_min,
                "price_max": precio_max,
                "order_by": "newest",
                "latitude": 40.416775,  # Madrid
                "longitude": -3.703790,
                "distance": 200000,  # 200 km
                "category_ids": "100"  # coches
            }

            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("search_objects", [])

                        for item in items:
                            title = item.get('title', 'Sin título')
                            price = item.get('price', 0)
                            item_id = item.get('id')

                            if item_id:
                                link = f"https://es.wallapop.com/item/{item_id}"
                                resultados.append({
                                    "titulo": title,
                                    "precio": f"{price}€",
                                    "url": link
                                })
                    else:
                        print(f"⚠️ Error en petición Wallapop para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en Wallapop para {modelo}: {e}")

    return resultados
