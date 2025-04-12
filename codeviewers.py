import inspect
import sys

import settings


def get_code_for(module_name: str, function_name: str):
    settings.logger.debug(
        f"Searching module {module_name} for function {function_name}"
    )
    settings.logger.debug([m for m in sys.modules if module_name in m])

    return inspect.getsource(getattr(sys.modules[module_name], function_name))
