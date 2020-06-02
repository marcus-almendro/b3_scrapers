import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
import chromedriver_binary

BASE_URL = 'http://bvmf.bmfbovespa.com.br/Fundos-Listados/FundosListadosDetalhe.aspx?Sigla=$SIGLA&tipoFundo=Imobiliario&aba=abaEventosCorporativos&idioma=pt-br'
chrome_options = ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = None


def busca_eventos_fii(papel):
    global driver
    try:
        driver = Chrome(options=chrome_options)
        driver.implicitly_wait(20)
        driver.get(BASE_URL.replace('$SIGLA', papel[0:4]))
        return _eventos_em_ativos() + _dividendos()
    finally:
        driver.quit()


def _eventos_em_ativos():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {
        'id': 'ctl00_contentPlaceHolderConteudo_ucEventosCorporativos_grdBonificacao_ctl01'})
    try:
        df = pd.read_html(str(table), decimal='.', thousands=',')[0]
    except ValueError:
        return []
    df.drop(columns=['Deliberado em',
                     'Observações'], inplace=True)
    df = df.rename(columns={'Proventos': 'tipo',
                            'Código ISIN': 'isin',
                            'Negócios com até': 'data_com',
                            '% / Fator de Grupamento': 'valor'})
    to_unix(df, 'data_com')
    return df.to_dict('records')


def _dividendos():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {
        'id': 'ctl00_contentPlaceHolderConteudo_ucEventosCorporativos_grdDividendo_ctl01'})
    try:
        df = pd.read_html(str(table), decimal=',', thousands='.')[0]
    except ValueError:
        return []
    df.drop(columns=['Deliberado em',
                     'Relativo a',
                     'Observações'], inplace=True)
    df = df.rename(columns={'Proventos': 'tipo',
                            'Código ISIN': 'isin',
                            'Negócios com até': 'data_com',
                            'Valor (R$)': 'valor',
                            'Início de Pagamento': 'data_pgto'})
    to_unix(df, 'data_com')
    to_unix(df, 'data_pgto')
    return df.to_dict('records')


def to_unix(df, s):
    df[s] = (pd.to_datetime(df[s], dayfirst=True) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
