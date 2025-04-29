import aiohttp

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json",
        "x-adevinta-channel": "web-desktop",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            # Aquí adaptamos para cada modelo
            params = {
                "text": modelo,
                "price_from": precio_min,
                "price_to": precio_max,
                "rows": 20,  # número de resultados (puedes subirlo)
                "sort": "published_at desc",  # los más nuevos primero
            }
            url = "https://web.gw.coches.net/semantic/segunda-mano/"

            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("items", [])

                        for item in items:
                            titulo = item.get('title', 'Sin título')
                            precio = item.get('price', 0)
                            enlace = f"https://coches.net{item.get('url', '')}"

                            resultados.append({
                                "titulo": titulo,
                                "precio": f"{precio}€",
                                "url": enlace,
                            })
                    else:
                        print(f"⚠️ Error en petición coches.net para modelo {modelo}: {response.status}")
            except Exception as e:
                print(f"⚠️ Excepción en coches.net para modelo {modelo}: {e}")

    return resultados
