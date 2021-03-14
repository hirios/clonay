from downIMGS import downIMGS, get_name, baixar
from lxml import html
import asyncio
import aiohttp
import aiofiles
import re 
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }


class HTML():
    def __init__(self, html_string, url_to_clone, namedir):
        self.tree = html.fromstring(html_string)
        self.url_to_clone = url_to_clone
        self.namedir = namedir
        

    def clean_html(self):
        """ 
        Remove todos os atributos srcset e data-srcset, necessário em alguns sites para carregar imagens via script """

        for tag in self.tree.xpath('//*[@srcset]'):
             tag.attrib.pop('srcset')

        for tag in self.tree.xpath('//*[@data-srcset]'):
             tag.attrib.pop('data-srcset')


    def get_files(self) -> list: 
        """ Retorna uma lista de urls referentes as imagens de um conteúdo de resposta html (type string) """

        # CAPTURANDO URLS DE IMAGENS, CSS, JSON, JS... RETORNA LISTAS

        imgs = self.tree.xpath('//img/@src')
        imgs2 = self.tree.xpath('//img/@data-src')
        scripts = self.tree.xpath('//script/@src')
        css_and_json = self.tree.xpath('//link/@href')


        # ALGUMAS URL NÃO TÊM O CAMINHO COMPLETO ATÉ O ARQUIVO;
        # NESTES CASOS CONCATENO O FRAGMENTO DA URL COM A URL DO SITE 
        # EX: /exemplo/teste/imagem.png
        # SITE: http://www.google.com/

        for x in range(0, len(css_and_json)):
            if css_and_json[x].startswith('/') or css_and_json[x].startswith('./'):
                split = self.url_to_clone.split('/')[:3]

                if not css_and_json[x].startswith('./'):
                    asyncio.run(baixar(split[0] + '//' + split[2] + css_and_json[x], self.namedir))
                else:
                    asyncio.run(baixar(split[0] + '//' + split[2] + css_and_json[x][1:], self.namedir))
                    

        for x in range(0, len(imgs)):
            if imgs[x].startswith('/') or imgs[x].startswith('./'):
                split = self.url_to_clone.split('/')[:3]

                if not imgs[x].startswith('./'):
                    asyncio.run(baixar(split[0] + '//' + split[2] + imgs[x], self.namedir))
                else:
                    asyncio.run(baixar(split[0] + '//' + split[2] + imgs[x][1:], self.namedir))


        imgs = imgs + imgs2 + scripts + css_and_json
        return imgs


    def run(self):
        self.clean_html()
        imgs = self.get_files()
        self.tree = html.tostring(self.tree).decode('UTF-8')
        return imgs, self.tree


def dir(URL):
    if URL.startswith('http://www.') or URL.startswith('https://www.') or URL.startswith('www'):
        namedir = URL.split('.')[1]
    else:
        namedir = URL.split('/')[2]

    try:
        os.mkdir(namedir)
    except FileExistsError:
        pass

    return namedir


count = 0
rex = r'\((http[^)]+)\)'


async def clone(URL):
    """ Salva a html de um site num arquivo index.html """ 

    global count

    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        async with session.get(URL) as page:

            count += 1
            if page.status == 200:
                namedir = dir(URL)
                file = await aiofiles.open(f'{namedir}.html', 'w', encoding='UTF-8')
                content = await page.text() 

                urls, content = HTML(content, URL, namedir).run()
                urls_imgs3 = re.findall(rex, content) # LISTA URL DE IMAGENS QUANDO ESSAS SÃO PASSADAS NO ATRIBUTO STYLE; EX: style="background-image: url(exemplo.png)"
                downIMGS(urls, namedir)
                downIMGS(urls_imgs3, namedir)
                
                # ALTERO O CAMINHO NA HTML PARA ACESSAR OS ARQUIVOS BAIXADOS 
                for x in urls:
                    content = content.replace('src="' + x + '"', 'src="' + f'./{namedir}/' + get_name(x) + '"')
                    content = content.replace('href="' + x + '"', 'href="' + f'./{namedir}/' + get_name(x) + '"')
                    content = content.replace('src=' + x, 'src="' + f'./{namedir}/' + get_name(x) + '"')

                for x in urls_imgs3:
                    content = content.replace(x, f'./{namedir}/' + get_name(x))

                await file.write(content)
            else:
                print('[-] STATUS_CODE ERRO:', page.status)

                
async def main():
    await asyncio.gather(*coroutines_list)


# EXEMPLO
SITES = ['https://aluno.uninove.br/index.php']

coroutines_list = [*[clone(x) for x in SITES]]


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"Script executado em {elapsed:0.2f} segundos.")
