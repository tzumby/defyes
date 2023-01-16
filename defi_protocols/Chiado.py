from defi_protocols.functions import *

from defi_protocols.test_env import *

CHIADO = "chiado"

def get_chiado_rpc(blockchain):
  if blockchain == CHIADO:
      return NODE_CHIADO
