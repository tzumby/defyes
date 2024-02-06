import json
import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

DB_VERSION = "v0.0.190"


def update_db(version=DB_VERSION):
    url = f"https://raw.githubusercontent.com/hop-protocol/hop/{version}/packages/core/src/addresses/mainnet.ts"
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
        json_object = json.loads("{\n" + "\n".join(processed_lines[3::]))

        with open(Path(__file__).parent / f"db_addrs_{version}.json", "w") as outfile:
            json.dump(json_object, outfile, indent=2, default=lambda o: str(o))

    logger.debug(f"Failed to retrieve db. Status code: {response.status_code}")
