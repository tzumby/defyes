import requests
from typing import List, Union, Dict
from decimal import Decimal


def get_api_results(wallet: str, blockchain: str) -> Union[List[dict], str]:
    if blockchain == "ethereum":
        chain_id = "1"
    else:
        print("blockchain not available")

    request = requests.get(
        f"https://api.hiddenhand.finance/reward/{chain_id}/{wallet}"
    ).json()
    if not request["error"]:
        return request["data"]
    else:
        return "request returns error"


def underlying(
    wallet: str, token: str, blockchain: str, decimals: bool = True
) -> List[str]:
    result = underlying_all(wallet, blockchain, decimals)
    return [x for x in result if x[0] == token][0]


def underlying_all(
    wallet: str, blockchain: str, decimals: bool = True
) -> Dict:
    api_result = get_api_results(wallet, blockchain)
    result = {"protocol": "HiddenHand", "block": "latest", "positions": []}
    for entry in api_result:
        position = next(
            (p for p in result["positions"] if p["position ID"] == entry["protocol"]),
            None,
        )

        if not position:
            position = {"position ID": entry["protocol"], "balances": []}
            result["positions"].append(position)

        token_decimals = entry["decimals"] if not decimals else 0
        claimable = Decimal(entry["claimable"])
        claimable *= Decimal(10**token_decimals)

        balance = {"token": entry["token"], "balance": claimable}
        position["balances"].append(balance)
    return result
