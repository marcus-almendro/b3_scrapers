import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'https://cei.b3.com.br/'
chrome_options = ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = None


def busca_trades(cpf, senha):
    global driver
    try:
        driver = Chrome(options=chrome_options)
        driver.implicitly_wait(20)
        _login(cpf, senha)
        lista = []
        for corretora in _corretoras_disponiveis():
            _abre_consulta_trades(corretora)
            lista += _ler_tabela(corretora)
        return lista
    finally:
        driver.quit()


def _login(cpf, senha):
    driver.get(BASE_URL)
    txt_login = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtLogin')
    txt_login.clear()
    txt_login.send_keys(cpf)
    txt_senha = driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtSenha')
    txt_senha.clear()
    txt_senha.send_keys(senha)
    btn_logar = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnLogar')
    btn_logar.click()
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID, 'objGrafPosiInv')))


def _corretoras_disponiveis():
    driver.get(BASE_URL + 'negociacao-de-ativos.aspx')
    from selenium.webdriver.support.select import Select
    agentes = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))
    first_option = int(agentes.first_selected_option.get_attribute('value'))
    if first_option == -1:  # Selecione
        return list(filter(lambda c: c > -1, map(lambda o: int(o.get_attribute('value')), agentes.options)))
    else:
        return [first_option]


def _abre_consulta_trades(corretora):
    driver.get(BASE_URL + 'negociacao-de-ativos.aspx')

    from selenium.webdriver.support.select import Select
    agentes = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))

    if agentes.first_selected_option.text.upper() == 'SELECIONE':
        agentes.select_by_value(str(corretora))
    else:
        btn_consultar = WebDriverWait(driver, 200).until(
            EC.visibility_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_btnConsultar')))
        btn_consultar.click()

        def not_disabled(drv):
            try:
                drv.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes')
            except NoSuchElementException:
                return False
            return drv.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes').get_attribute(
                "disabled") is None

        WebDriverWait(driver, 200).until(not_disabled)

    btn_consultar = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnConsultar')
    btn_consultar.click()

    WebDriverWait(driver, 200).until(EC.visibility_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_rptAgenteBolsa_ctl00_rptContaBolsa_ctl00_pnAtivosNegociados')))


def _ler_tabela(corretora):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    top_div = soup.find('div', {
        'id': 'ctl00_ContentPlaceHolder1_rptAgenteBolsa_ctl00_rptContaBolsa_ctl00_pnAtivosNegociados'})

    table = top_div.find(lambda tag: tag.name == 'table')

    df = pd.read_html(str(table), decimal=',', thousands='.')[0]

    df = df.dropna(subset=['Mercado'])
    df = df.rename(columns={'Código Negociação': 'papel',
                            'Compra/Venda': 'operacao',
                            'Quantidade': 'qtde',
                            'Data do Negócio': 'data',
                            'Preço (R$)': 'preco'})

    df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
    df['operacao'] = df.apply(lambda row: 'venda' if row.operacao == 'V' else 'compra', axis=1)

    df.drop(columns=['Mercado',
                     'Prazo/Vencimento',
                     'Especificação do Ativo',
                     'Valor Total(R$)',
                     'Fator de Cotação'], inplace=True)

    df['corretora'] = corretora

    return df.to_dict('records')
