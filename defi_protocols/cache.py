import logging
import os

from web3.middleware.cache import generate_cache_key
import diskcache

logger = logging.getLogger(__name__)

_cache = None
if not os.environ.get("DEFI_PROTO_CACHE_DISABLE"):
    cache_dir = os.environ.get("DEFI_PROTO_CACHE_DIR", "/tmp/defi_protocols/")
    logger.debug(f"Cache enabled. Storage is at '{cache_dir}'.")
    _cache = diskcache.Cache(directory=cache_dir, disk_pickle_protocol=5)
    if os.environ.get("DEFI_PROTO_CLEAN_CACHE"):
        _cache.clear()
else:
    logger.debug(f'Cache is disabled')

def is_enabled():
    return _cache is not None

def clear():
    if is_enabled():
        _cache.clear()

def disk_cache_middleware(make_request, web3):
    """
    Cache middleware that supports multiple blockchains.
    It also do not caches if block='latest'.
    """

    RPC_WHITELIST = {'eth_chainId', 'eth_call'}

    def middleware(method, params):
        do_cache = False
        if method in RPC_WHITELIST and 'latest' not in params:
            do_cache = True
        elif method == 'eth_chainId':
            do_cache = True

        if do_cache:
            params_hash = generate_cache_key(params)
            cache_key = f"{web3._network_name}.{method}.{params_hash}"
            if cache_key not in _cache:
                response = make_request(method, params)
                if not ('error' in response or 'result' not in response or response['result'] is None):
                    _cache[cache_key] = response['result']
                return response
            else:
                data = _cache[cache_key]
                return {'jsonrpc': '2.0', 'id': 11, 'result': data}
        else:
            logger.debug(f"Not caching '{method}' with params: '{params}'")
            return make_request(method, params)
    return middleware
