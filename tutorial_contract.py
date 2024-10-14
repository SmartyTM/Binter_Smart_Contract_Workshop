
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
    
   # Inserte su código aquí para poder procesar el pre-posting hook y eliminar el error que muestra el VSC
   
   # El propósito de este ejercicio es que creemos un bloque de código que vaya dentro de la función 
   # pre_posting_hook que permita leer el previo de la publicación del posting, 
   # identificar en que moneda se está realizando la transacción y que acepte sólo esta publicación 
   # si corresponde con la moneda identificada para la cuenta.
   
   