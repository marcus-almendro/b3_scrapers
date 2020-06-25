from .codigos_cvm import busca_codigos_cvm
from .codigos_negociacao import busca_codigos_negociacao
from .eventos_acoes import busca_eventos_acoes

from .fii_listados import busca_codigos_fii
from .eventos_fii import busca_eventos_fii

from .negociacao import busca_trades

from .proventos_fii import busca_proventos_no_range

from tqdm import tqdm
from concurrent import futures


def busca_dados_acoes():
    codigos = busca_codigos_cvm()
    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        return list(tqdm(executor.map(_busca_dados_codigo_cvm, codigos),
                         total=len(codigos),
                         desc='Buscando códigos negociação'))


def busca_dados_fii():
    fiis = busca_codigos_fii()
    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        return list(tqdm(executor.map(_busca_dados_codigo_fii, fiis),
                         total=len(fiis),
                         desc='Buscando informações dos FIIs'))


def _busca_dados_codigo_cvm(codigo):
    cod_negs = busca_codigos_negociacao(codigo['codigo_cvm'])
    return {
        'codigo_cvm': codigo['codigo_cvm'],
        'nome': codigo['nome'],
        'symbols': cod_negs['symbols'],
        'isin': cod_negs['isin'],
        'eventos': busca_eventos_acoes(codigo['codigo_cvm'])
    }


def _busca_dados_codigo_fii(fii):
    return {
        'sigla': fii['sigla'],
        'nome': fii['nome'],
        'symbols': [fii['sigla'] + '11'],
        'eventos': busca_eventos_fii(fii['sigla'])
    }
