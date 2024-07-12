
# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd



headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.1081610889.1720541786; __gads=ID=d9c4ff4f86e6e15a:T=1720438777:RT=1720548410:S=ALNI_MZ8peg4e2t_9v7zZuMcA4JmoAFwrg; __gpi=UID=00000a3c6dbe9d20:T=1720438777:RT=1720548410:S=ALNI_MbhuE1hNUxAzq0Qk09w-8QK-m6-Ww; __eoi=ID=420d81a3e7d34d02:T=1720438777:RT=1720548410:S=AA-AfjYXLrQ9PKmyA6dA_q2Acf5Z; _ga=GA1.2.32360730.1720438794; FCNEC=%5B%5B%22AKsRol9wuMfjxkOBrCY9nq2mfS9EKY9zr-AX3Winf3PyJ0FyN3QuW3kUBgQpr3Yx_rG3pLouX7ZsPoGzuTQ8VC61LBFBt5kpLuu7C-ZzkeMsrd7B9r_0MDTxY6C58gLK6MrtEP1Kz1ToGRkBHvKDpoSn9jR6_DMj0w%3D%3D%22%5D%5D; _ga_DJLCSW50SC=GS1.1.1720548428.3.1.1720548433.55.0.0; _ga_D6NF5QC4QT=GS1.1.1720548428.3.1.1720548433.55.0.0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


def get_content (url):
   
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    
    data = {}
    
    #NESTE CÓDIGO utiliziamos *_ para Fazer unpack, descompressão de lista, 
    # para ignorar o erro que estava dando no personagem ark thompson (porém o ideal 
    #seria fazer um Tratamento de dados somente nele, faremos posteriormente.).
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
        
    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
            .find("h4")
            .find_next()
            .find_all("li"))
            
    aparicoes = [i.text for i in lis]
    
    return aparicoes


def get_personagens_infos(url):
    resp = get_content(url)

    if resp.status_code != 200:
        print("Não foi possível obter os dados")
        return {}
    
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data

def get_links():
    url = "https://www.residentevildatabase.com/personagens"

    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find('div', class_ = "td-page-content").find_all("a"))

    links = [i['href'] for i in ancoras]
    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_infos(i)
    d['link'] = i
    data.append(d)

# %%
df = pd.DataFrame(data)
df
# %%

# %%
