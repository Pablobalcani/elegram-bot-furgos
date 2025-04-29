import aiohttp

MODELOS = [
    {"make_id": 59, "model_id": 2223, "nombre": "Rifter"},
    {"make_id": 15, "model_id": 1127, "nombre": "Berlingo Combi"},
    {"make_id": 67, "model_id": 2087, "nombre": "Tourneo Courier"},
    {"make_id": 28, "model_id": 1135, "nombre": "Doblo"},
]

async def buscar_cochesnet(precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.coches.net",
        "Referer": "https://www.coches.net/",
        "X-Adevinta-Channel": "web-desktop",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in MODELOS:
            url = "https://web.gw.coches.net/semantic/segunda-mano/"
            params = {
                "MakeIds[0]": modelo["make_id"],
                "ModelIds[0]": modelo["model_id"],
                "PriceFrom": precio_min,
                "PriceTo": precio_max,
                "rows": 20,
                "sort": "published_at desc",
            }

            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        coches = data.get("items", [])

                        for coche in coches:
                            resultados.append({
                                "titulo": coche.get("title", "Sin título"),
                                "precio": f"{coche.get('price', 0)}€",
                                "url": f"https://www.coches.net{coche.get('url', '')}",
                            })
                    else:
                        print(f"⚠️ Error en petición coches.net para modelo {modelo['nombre']}: {response.status}")

            except Exception as e:
                print(f"⚠️ Error general en modelo {modelo['nombre']}: {e}")

    return resultados
