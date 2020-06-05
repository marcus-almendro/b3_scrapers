# b3 scrapers

Web scrapers para o site da B3 e CEI com as seguintes funcionalidades:
* Códigos CVM, de negociação e ISIN das ações listadas
* Eventos corporativos de ações e fundos imobiliários
* Histórico de negociação do investidor

## Instalação
`pip install b3-scrapers`

Caso queira buscar o histórico de negociação:

`pip install chromedriver_binary==83.0.4103.39.0`, substituindo a versão conforme o Chrome disponível no seu sistema. Ver versões disponíveis aqui: https://pypi.org/project/chromedriver-binary/#history
## Modo de uso
```python
from b3_scrapers import *

# ações
codigos = busca_codigos_cvm() 
cod_negs = busca_codigos_negociacao('<codigo_cvm>')
eventos_acoes = busca_eventos_acoes('<codigo_cvm>')
dados_acoes = busca_dados_acoes() # busca codigos cvm, codigos de negociação e eventos

# fii
fiis = busca_codigos_fii()
eventos_fii = busca_eventos_fii('<codigo_negociacao>')
dados_fii = busca_dados_fii() # busca fii listados e eventos

# negociação
import chromedriver_binary
negocios = busca_trades('<cpf>', '<senha>')
```
