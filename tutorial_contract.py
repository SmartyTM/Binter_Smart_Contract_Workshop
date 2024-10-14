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

# Definimos la función principal que se llama antes de realizar una publicación (transacción)
def pre_posting_hook(
   vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
    # Iteramos sobre todas las instrucciones de publicación que se han pasado a la función
    # Verificamos si alguna de las publicaciones no está en la denominación 'COP' (Pesos Colombianos)
    if any(posting.denomination != 'COP' for posting in hook_arguments.posting_instructions):
        # Si alguna publicación no es en 'COP', devolvemos un resultado de rechazo
        return PrePostingHookResult(
            rejection=Rejection(
                # Mensaje de rechazo que se muestra al usuario explicando el motivo
                message="Las transacciones solo pueden ser realizadas en Pesos Colombianos (COP)",
                # Código de razón para el rechazo, especificando que la denominación es incorrecta
                reason_code=RejectionReason.WRONG_DENOMINATION,
            )
        )
    # Si todas las publicaciones están en 'COP', la función devuelve None y la transacción continúa normalmente