import aiohttp

async def buscar_autoscout24(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            page = 1
            while True:
                url = f"https://www.autoscout24.com/lst?sort=standard&desc=0&ustate=N%2CU&atype=C&cy=E&pricefrom={precio_min}&priceto={precio_max}&page={page}&model={modelo.replace(' ', '%20')}"

                async with session.get(url) as response:
                    if response.status != 200:
                        print(f"⚠️ Error en petición AutoScout24 para modelo {modelo}: {response.status}")
                        break

                    data = await response.json()

                    # Si data es lista directamente
                    if isinstance(data, list):
                        items = data
                    else:
                        items = data.get("items", [])

                    if not items:
                        break  # no más resultados

                    for item in items:
                        titulo = item.get("title", "Sin título")
                        precio = item.get("price", "¿?")
                        enlace = f"https://www.autoscout24.com{item.get('url', '')}"

                        resultados.append({
                            "titulo": titulo,
                            "precio": f"{precio}€",
                            "url": enlace,
                        })

                    page += 1

    return resultados
