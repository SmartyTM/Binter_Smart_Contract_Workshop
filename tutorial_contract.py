from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
)

# Definimos la versión del API que estamos utilizando para este Smart Contract, en este caso es la 4.0.0
api = "4.0.0"  # Esto es un SmartContract usando el Contract Language API 4.0.0

# Definimos la versión del contrato siguiendo las prácticas de versionado semántico
version = "0.0.1"  # Usamos versionado semántico. Revisar las buenas prácticas para su uso en https://semver.org/

from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
)

# Definimos la versión del API que estamos utilizando para este Smart Contract, en este caso es la 4.0.0
api = "4.0.0"  # Esto es un SmartContract usando el Contract Language API 4.0.0

# Definimos la versión del contrato siguiendo las prácticas de versionado semántico
version = "0.0.1"  # Usamos versionado semántico. Revisar las buenas prácticas para su uso en https://semver.org/

parameters = [
  # Defina sus parámetros que precisa para poder pasar el valor de COP u otro tipo de moneda a su Smart Contract
]
@requires(parameters=True)
def pre_posting_hook(
  vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
   allowed_denomination = # ïndique que Denominación de moneda permite para su uso en este Smart Contract
   if any(posting.denomination != allowed_denomination for posting in hook_arguments.posting_instructions):
       return PrePostingHookResult(
           rejection=Rejection(
               message="Las transacciones solo pueden ser realizadas en Pesos Colombianos (COP)",
               reason_code=RejectionReason.WRONG_DENOMINATION,
           )
       )