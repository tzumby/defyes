import logging
from .protocols import (
    ankr as Ankr,
    ankr,
    curve as Curve,
    curve,
    lido as Lido,
    lido,
    swapr as Swapr,
    swapr,
    uniswapv3 as UniswapV3,
    uniswapv3,
    compoundv3 as Compoundv3,
    compoundv3,
    angle as Angle,
    angle,
    unit as Unit,
    unit,
    notional as Notional,
    notional,
    agave as Agave,
    agave,
    compound as Compound,
    compound,
    realt as RealT,
    realt,
    connext as Connext,
    connext,
    honeyswap as Honeyswap,
    honeyswap,
    hiddenhand as HiddenHand,
    hiddenhand,
    ironbank as IronBank,
    ironbank,
    sushiswap as SushiSwap,
    sushiswap,
    mstable as mStable,
    mstable,
    aave as Aave,
    aave,
    bancor as Bancor,
    bancor,
    symmetric as Symmetric,
    symmetric,
    maker as Maker,
    maker,
    elk as Elk,
    elk,
    rocketpool as RocketPool,
    rocketpool,
    azuro as Azuro,
    azuro,
    balancer as Balancer,
    balancer,
    reflexer as Reflexer,
    reflexer,
    qidao as QiDao,
    qidao,
    idle as Idle,
    idle,
    votium as Votium,
    votium,
)
from .protocols import (
    stakewise as Stakewise,
    stakewise,
    aura as Aura,
    aura,
    convex as Convex,
    convex,
)
from .protocols import (
    element as Element,
    element,
)

logging.getLogger(__name__).addHandler(logging.NullHandler())


def add_stderr_logger(level: int = logging.DEBUG) -> logging.StreamHandler:
    """
    Helper for quickly adding a StreamHandler to the logger. Useful for
    debugging.
    Returns the handler after adding it.
    """
    # This method needs to be in this __init__.py to get the __name__ correct
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("Added a stderr logging handler to logger: %s", __name__)
    return handler
