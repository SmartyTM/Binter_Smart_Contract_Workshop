from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
   Parameter,  # Importamos la clase Parameter para definir parámetros configurables
   DenominationShape,  # Importamos la clase DenominationShape para definir la forma del parámetro de denominación
   ParameterLevel,  # Importamos ParameterLevel para especificar el nivel del parámetro
)

# Definimos la versión del API que estamos utilizando para este Smart Contract, en este caso es la 4.0.0
api = "4.0.0"  # Esto es un SmartContract usando el Contract Language API 4.0.0

# Definimos la versión del contrato siguiendo las prácticas de versionado semántico
version = "0.0.1"  # Usamos versionado semántico. Revisar las buenas prácticas para su uso en https://semver.org/

# Definimos los parámetros del Smart Contract
parameters = [
  Parameter(
       name='denominacion',  # Nombre del parámetro, que se utilizará para identificarlo en el Smart Contract
       shape=DenominationShape(),  # Forma del parámetro, especificando que se trata de una denominación monetaria
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, aquí se establece a nivel de plantilla (TEMPLATE)
       default_value="COP",  # Valor por defecto del parámetro, que en este caso es 'COP' (Pesos Colombianos)
   ),
]

# Decorador que indica que este hook requiere acceso a parámetros
@requires(parameters=True)
def pre_posting_hook(
  vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
    # Obtenemos el valor actual del parámetro 'denominacion' utilizando la serie temporal del parámetro
    allowed_denomination = vault.get_parameter_timeseries(name="denomination").latest()
    
    # Verificamos si alguna de las publicaciones no está en la denominación permitida (obtenida del parámetro)
    if any(posting.denomination != allowed_denomination for posting in hook_arguments.posting_instructions):
        # Si alguna publicación no tiene la denominación permitida, devolvemos un resultado de rechazo
        return PrePostingHookResult(
            rejection=Rejection(
                # Mensaje de rechazo que se muestra al usuario explicando el motivo
                message="Las transacciones solo pueden ser realizadas en Pesos Colombianos (COP)",
                # Código de razón para el rechazo, especificando que la denominación es incorrecta
                reason_code=RejectionReason.WRONG_DENOMINATION,
            )
        )
    # Si todas las publicaciones están en la denominación permitida, la función devuelve None y la transacción continúa normalmente