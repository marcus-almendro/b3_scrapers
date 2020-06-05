from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
from more_itertools import unique_everseen
from tqdm import tqdm

url = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?Letra='
alphanum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def busca_codigos_cvm():
    dados = []
    for letra in tqdm(alphanum, desc='Baixando codigos CVM'):
        with urlopen(url + letra) as html:
            soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'id': 'ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_grdEmpresa_ctl01'})

        try:
            df = pd.read_html(str(table))[0]
        except ValueError:
            continue

        codigos = list(unique_everseen(
            [link.get('href').split('=')[1] for link in soup.findAll('a', attrs={'href': re.compile("codigoCvm=")})]
        ))
        df['codigo_cvm'] = codigos
        df.drop(columns=['Razão Social',
                         'Segmento'], inplace=True)
        df = df.rename(columns={'Nome de Pregão': 'nome'})
        dados += df.to_dict('records')
    return dados
