import aiohttp

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            params = {
                "CategoryId": 32,  # Categoría de coches
                "Text": modelo,
                "FromPrice": precio_min,
                "ToPrice": precio_max,
                "Start": 1  # Empezar desde el primer anuncio
            }
            url = "https://www.milanuncios.com/ajx/buscador/"

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    anuncios = data.get('adverts', [])

                    for anuncio in anuncios:
                        titulo = anuncio.get('subject', 'Sin título')
                        precio = anuncio.get('price', 'Sin precio')
                        url_anuncio = f"https://www.milanuncios.com{anuncio.get('url', '')}"

                        resultados.append({
                            "titulo": titulo,
                            "precio": f"{precio}€",
                            "url": url_anuncio
                        })
                else:
                    print(f"⚠️ Error en petición Milanuncios para modelo {modelo}: {response.status}")

    return resultados
