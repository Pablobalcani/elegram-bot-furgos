import aiohttp
from bs4 import BeautifulSoup

async def buscar_autocasion(modelos, precio_min, precio_max):
    resultados = []

    async with aiohttp.ClientSession() as session:
        for modelo in modelos:
            modelo_url = modelo.replace(' ', '-')
            url = f"https://www.autocasion.com/coches-ocasion/{modelo_url}?precioDesde={precio_min}&precioHasta={precio_max}"

            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    anuncios = soup.find_all('div', class_='content')  # Ajusta el contenedor si es necesario

                    for anuncio in anuncios:
                        titulo_tag = anuncio.find('h2', class_='title')
                        precio_tag = anuncio.find('span', class_='price')

                        link_tag = anuncio.find('a', href=True)

                        if titulo_tag and precio_tag and link_tag:
                            titulo = titulo_tag.text.strip()
                            precio = precio_tag.text.strip()
                            enlace = "https://www.autocasion.com" + link_tag['href']

                            resultados.append({
                                'titulo': titulo,
                                'precio': precio,
                                'url': enlace
                            })

    return resultados
