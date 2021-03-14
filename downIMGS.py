import asyncio
import aiohttp
import aiofiles 
import time
import nest_asyncio


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }


# permitindo asyncio.run() a partir de outro módulo
nest_asyncio.apply()


def get_name(url: str):
    """ Essa função tenta retornar o nome dos arquivos a partir da url de download """

    # O NOME DO ARQUIVO GERALMENTE VEM NO FINAL DA URL (PATH)
    name = url.split('/')[-1]
    TAGS = ('.jpg', '.jpeg', '.png', '.gif', '.css', '.json', '.js', '.ico')

    # AQUI VERIFICAMOS SE O NOME QUE PEGAMOS TERMINA COM UMAS DESSAS EXTENSÕES
    if name.endswith(TAGS):
        return name
    
    # CASO NÃO TERMINE COM NENHUMA DESSAS EXTENSÕES, ELE TENTA PEGAR E DIVIDIR UM TRECHO 
    # PARECIDO COM ISSO: teste.com/imagem.png?exemplo/outra_coisa
    for x in TAGS:
        if not x.endswith('?'):
            x = x + '?'
            
            if x in name:
                name = name.split(x)[0] + x[:-1]
            else:
                if x[1:] in name:
                    name = name.split(x[1:])[0] +  x[1:-1]

    return name


async def baixar(url: str):
    """ Realiza o download de algum arquivo """
    
    name = get_name(url)

    if name:
        if url.startswith('http'):
            try:
                timeout = aiohttp.ClientTimeout(total=10)
                async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            f = await aiofiles.open(f'imagens/{name}', mode='wb')
                            await f.write(await resp.read())
                            await f.close()                                
            except:
                print('[-] Erro ao baixar arquivo; url:', url)
                #print('[-] Nome usado para salvar:', name)
                pass

    else:
        print('[-] Nome para salvar vazio:', str(len(name)))


def createMain(lista):
    complemento = ""
    for x in lista:
        complemento += f"baixar('{x}'), "    
    complemento = complemento[:-2]
        
    funcao = f'''
async def main2():
    await asyncio.gather({complemento})'''
    
    return funcao 


def downIMGS(lista):
    s = time.perf_counter()
    main = createMain(lista)
    exec(main, globals())
    asyncio.run(main2())
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    url_list = ['urls']

    if lista[0] == 'urls':
        print('Passe suas urls para a "url_list"')
        quit()
    asyncio.run(downIMGS(lista))