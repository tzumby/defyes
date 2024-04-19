from decimal import Decimal

from defyes.protocols.mu import get_protocol_data_for


def test_get_protocol_data_for():
    blockchain = "gnosis"
    wallet = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"
    lptoken_address = "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a"
    block = 33472627

    result = get_protocol_data_for(blockchain, wallet, lptoken_address, block)

    expected_result = {
        "blockchain": "gnosis",
        "block_id": 33472627,
        "protocol": "Mu Exchange",
        "positions_key": "holding_token_address",
        "version": 0,
        "wallet": "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f",
        "decimals": 18,
        "positions": {
            "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a": {
                "holdings": [
                    {
                        "address": "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a",
                        "balance": Decimal("247617.950948613945569201"),
                    }
                ],
                "underlyings": [
                    {
                        "address": "0xaf204776c7245bF4147c2612BF6e5972Ee483701",
                        "balance": Decimal("268178.964115319996226166"),
                    }
                ],
            }
        },
    }

    assert result == expected_result
