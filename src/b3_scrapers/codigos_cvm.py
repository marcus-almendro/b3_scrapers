from urllib.request import urlopen
from bs4 import BeautifulSoup
import string
import re
from tqdm import tqdm

url = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?Letra='
alphanum = string.ascii_lowercase.upper() + ''.join(list(map(str, range(10))))
alphanum = 'A'

def busca_codigos_cvm():
    data = []
    for letra in tqdm(alphanum, desc='Baixando codigos CVM'):
        with urlopen(url + letra) as html:
            soup = BeautifulSoup(html, 'html.parser')

        for link in soup.findAll('a', attrs={'href': re.compile("codigoCvm=")}):
            data.append(link.get('href').split('=')[1])
    return data
