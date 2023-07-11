from contextlib import contextmanager

from web3.exceptions import BadFunctionCallOutput, ContractLogicError

suppressed_error_codes = {-32000, -32015}


@contextmanager
def suppress_some_contract_method_errors():
    try:
        yield
    except (ContractLogicError, BadFunctionCallOutput):
        pass
    except ValueError as e:
        if e.args[0]["code"] not in suppressed_error_codes:
            raise


def call_contract_method(method, block):
    with suppress_some_contract_method_errors():
        return method.call(block_identifier=block)
