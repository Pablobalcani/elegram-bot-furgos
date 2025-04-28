import aiohttp
from bs4 import BeautifulSoup

async def buscar_milanuncios(modelos, precio_min, precio_max):
    resultados = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            url = f"https://www.milanuncios.com/coches-de-segunda-mano/{modelo_url}.htm?desde={precio_min}&hasta={precio_max}"

            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Aquí corregimos: buscamos en los scripts JSON
                    scripts = soup.find_all('script', type="application/ld+json")
                    for script in scripts:
                        try:
                            import json
                            data = json.loads(script.string)

                            if isinstance(data, dict) and data.get('@type') == 'Product':
                                titulo = data.get('name', 'Sin título')
                                precio = f"{data.get('offers', {}).get('price', 'Sin precio')} €"
                                enlace = data.get('offers', {}).get('url', '')

                                if enlace:
                                    resultados.append({
                                        'titulo': titulo,
                                        'precio': precio,
                                        'url': enlace
                                    })
                        except Exception:
                            continue

    return resultados
