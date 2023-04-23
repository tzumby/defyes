import requests
from typing import List, Union

def get_api_results(wallet: str, blockchain: str) -> Union[List[dict], str]:
    if blockchain == 'ethereum':
        chain_id = '1'
    else:
        print('blockchain not available')

    request = requests.get(f'https://api.hiddenhand.finance/reward/{chain_id}/{wallet}').json()
    if not request['error']:
        return request['data']
    else:
        return "request returns error"


def underlying(wallet: str, token: str, blockchain: str, decimals: bool = True) -> List[str]:
    result = underlying_all(wallet, blockchain, decimals)
    return [x for x in result if x[0] == token][0]


def underlying_all(wallet: str, blockchain: str, decimals: bool = True) -> List[List[str]]:
    result = get_api_results(wallet, blockchain)
    token_claimable = {}

    for d in result:
        token = d['token']
        claimable = float(d['claimable'])
        if not decimals:
            claimable = claimable * 10**d['decimals']
        if token in token_claimable:
            token_claimable[token] += claimable
        else:
            token_claimable[token] = claimable

    return [[k, str(v)] for k, v in token_claimable.items()]



