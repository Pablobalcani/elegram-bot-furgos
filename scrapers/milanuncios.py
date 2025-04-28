import aiohttp

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            params = {
                "categoryId": 37,  # 37 = Coches en Milanuncios
                "keywords": modelo,
                "priceMin": precio_min,
                "priceMax": precio_max,
                "start": 0,
                "size": 20,  # cuántos resultados quieres por búsqueda
                "sortBy": "relevance",
            }
            url = "https://www.milanuncios.com/anuncios/api/v1/ad/search"

            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        anuncios = data.get("ads", [])

                        for anuncio in anuncios:
                            titulo = anuncio.get("subject", "Sin título")
                            precio = anuncio.get("price", "Sin precio")
                            id_anuncio = anuncio.get("id", "")

                            enlace = f"https://www.milanuncios.com/anuncio/{id_anuncio}"

                            resultados.append({
                                "titulo": titulo,
                                "precio": f"{precio} €",
                                "url": enlace,
                            })
                    else:
                        print(f"⚠️ Error {response.status} buscando {modelo} en Milanuncios.")
            except Exception as e:
                print(f"⚠️ Error buscando {modelo}: {e}")

    return resultados
