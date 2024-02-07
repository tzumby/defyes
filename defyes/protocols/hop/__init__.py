import json
import logging
from pathlib import Path

import requests
from karpatkit.constants import Address

logger = logging.getLogger(__name__)

DB_VERSION = "v0.0.190"
DB_FILENAME = "db_addrs.json"


def update_db(filename=DB_FILENAME):
    url = f"https://github.com/hop-protocol/hop/raw/{DB_VERSION}/packages/core/src/addresses/mainnet.ts"
    response = requests.get(url)
    if response.status_code == 200:
        processed_lines = []
        for line in response.text.split("\n"):
            p_line = line.split("//")[0].rstrip().replace("'", '"')
            if ":" in p_line:
                key, data = p_line.split(":")
                key = key.split(":")[0].split(" ")
                p_line = " ".join(key[:-1]) + f'"{key[-1]}":' + data
            processed_lines.append(p_line)
        add_version = f'{{\n  "version": "{DB_VERSION}",\n'
        json_object = json.loads(add_version + "\n".join(processed_lines[3::]))

        with open(Path(__file__).parent / filename, "w") as outfile:
            json.dump(json_object, outfile, indent=2, default=lambda o: str(o))
    else:
        logger.debug("Failed to retrieve db. Status code: %s", response.status_code)


def get_lptokens_from_db(db_file=DB_FILENAME):
    with open(Path(__file__).parent / db_file, "r") as infile:
        data = json.load(infile)
    lp_tokens = {}
    for token, info in data["bridges"].items():
        for blockchain, addrs in info.items():
            for key, addr in addrs.items():
                if "LpToken" in key and addr != Address.ZERO:
                    lp_tokens[blockchain] = lp_tokens.get(blockchain, [])
                    lp_tokens[blockchain].append(addr)

    return lp_tokens


def get_rewards_contracts_from_db(db_file=DB_FILENAME):
    with open(Path(__file__).parent / db_file, "r") as infile:
        data = json.load(infile)
    return data["rewardsContracts"]
