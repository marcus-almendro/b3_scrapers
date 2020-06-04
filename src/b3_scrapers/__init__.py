from .codigos_cvm import busca_codigos_cvm
from .codigos_negociacao import busca_codigos_negociacao
from .eventos_acoes import busca_eventos_acoes

from .fii_listados import busca_codigos_fii
from .eventos_fii import busca_eventos_fii

from .negociacao import busca_trades

from tqdm import tqdm


def busca_dados_acoes():
    acoes = []
    codigos = busca_codigos_cvm()
    for codigo in tqdm(codigos, desc='Buscando informações dos papéis'):
        cod_negs = busca_codigos_negociacao(codigo)
        acoes.append({
            'codigo_cvm': codigo,
            'symbols': cod_negs['symbols'],
            'isin': cod_negs['isin'],
            'eventos': busca_eventos_acoes(codigo)
        })
    return acoes


def busca_dados_fii():
    fiis = []
    codigos = busca_codigos_fii()
    for codigo in tqdm(codigos, desc='Buscando informações dos FIIs'):
        fiis.append({
            'codigo_cvm': codigo,
            'symbols': [codigo + '11'],
            'eventos': busca_eventos_fii(codigo)
        })
    return fiis
