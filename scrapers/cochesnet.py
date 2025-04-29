import aiohttp

async def buscar_cochesnet(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_encoded = modelo.replace(' ', '-')
            url = f"https://web.gw.coches.net/semantic/segunda-mano/?Model={modelo_encoded}&PriceFrom={precio_min}&PriceTo={precio_max}"

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
