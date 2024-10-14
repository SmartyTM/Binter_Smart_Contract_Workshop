
from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
)

api = "4.0.0"  # Esto es un SmartContract usando el Contract Language  API 4.0.0
version = "0.0.1"  # Usamos versionado semático. Revisar las buenas prácticas para su uso en https://semver.org/


def pre_posting_hook(
   vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
    
   # Solución para el Ejercicio 2
    if any(posting.denomination != 'COP' for posting in hook_arguments.posting_instructions):
       return PrePostingHookResult(
           rejection=Rejection(
               message="Las transacciones solo pueden ser realizadas en Pesos Colombianos (COP)",
               reason_code=RejectionReason.WRONG_DENOMINATION,
           )
       )

