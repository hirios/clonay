import asyncio
import aiohttp
import aiofiles 
import time
import nest_asyncio


# permitindo asyncio.run() a partir de outro módulo
nest_asyncio.apply()


async def baixar(url):
    name = url.split('/')[-1]

    if '.jpg' in name:
        name = name.split('.jpg?')[0] + '.jpg'
        
    elif '.jpeg' in name:
        name = name.split('.jpeg?')[0] + '.jpeg'

    elif '.png' in name:
        name = name.split('.png?')[0] + '.png'


    if url.startswith('http'):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f'imagens/{name}', mode='wb')
                        await f.write(await resp.read())
                        await f.close()                                
        except:
            print('[-] Erro ao baixar imagem; url:', url)
            pass

            
def createMain(lista):
    complemento = ""
    for x in lista:
        complemento += f"baixar('{x}'), "    
    complemento = complemento[:-2]
        
    funcao = f'''
async def main2():
    await asyncio.gather({complemento})'''
    
    return funcao 


def downImgs(lista):
    s = time.perf_counter()
    main = createMain(lista)
    exec(main, globals())
    asyncio.run(main2())
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")

