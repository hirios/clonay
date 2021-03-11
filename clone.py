from downIMGS import downIMGS
from lxml import html
import asyncio
import aiohttp
import aiofiles 


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }


def get_img_urls(html_string: str) -> list: 
    """ Retorna uma lista de urls referentes as imagens de um conteúdo de resposta html (type string) """

    tree = html.fromstring(html_string)
    imgs = tree.xpath('//img/@src')
    return imgs


count = 0
async def clone(URL):
    """ Salva a html de um site num arquivo index.html """ 

    global count
    
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as page:
            count += 1
            if page.status == 200:
                file = await aiofiles.open(f'index{str(count)}.html', 'w', encoding='UTF-8')
                content = await page.text() 

                urls = get_img_urls(content)
                downImgs(urls)

                await file.write(content.replace('src="https://', 'src="'))
            else:
                print('[-] STATUS_CODE ERRO:', page.status)

                
async def main():
    await asyncio.gather(*coroutines_list)


# EXEMPLO
URL1 = 'https://www.pinterest.pt/nikitalitos/melhores-fotos-de-animes-geral/'
URL2 = 'https://madeinjapan.com.br/2017/05/23/top-100-melhores-animes-da-historia/'
coroutines_list = [clone(URL1), clone(URL)]


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"Script executado em {elapsed:0.2f} segundos.")
