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

    if 'manifest' in url:
        return 'manifest'
    
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


async def baixar(url: str, namedir: str):
    """ Realiza o download de algum arquivo """

    name = get_name(url)

    if name:
        if url.startswith('http'):
            try:
                timeout = aiohttp.ClientTimeout(total=10)
                async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            f = await aiofiles.open(f'{namedir}/{name}', mode='wb')
                            await f.write(await resp.read())
                            await f.close()                                
            except:
                print('[ERRO 004]: Erro ao baixar arquivo: \n-->', url + '\n')
                #print('[-] Nome usado para salvar:', name)
                pass

    else:
        print('[ERRO 000]: Filename vazio:', str(len(name)))
        print('-->', url + '\n')
        pass


def createMain(lista, namedir):
    complemento = ""
    for x in lista:
        complemento += f"baixar('{x}', '{namedir}'), "    
    complemento = complemento[:-2]
        
    funcao = f'''
async def main2():
    await asyncio.gather({complemento})'''
    
    return funcao 


def downIMGS(lista, namedir):
    s = time.perf_counter()
    main = createMain(lista, namedir)
    exec(main, globals())
    asyncio.run(main2())
    elapsed = time.perf_counter() - s
    #print(f"executed in {elapsed:0.2f} seconds.")


if __name__ == "__main__":
    url_list = ['urls']

    if lista[0] == 'urls':
        print('Passe suas urls para a "url_list"')
        quit()
    asyncio.run(downIMGS(lista, 'pasta/para/salvar'))