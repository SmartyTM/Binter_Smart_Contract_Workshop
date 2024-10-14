from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
   Parameter,  # Importamos la clase Parameter para definir parámetros configurables
   DenominationShape,  # Importamos la clase DenominationShape para definir la forma del parámetro de denominación
   ParameterLevel,  # Importamos ParameterLevel para especificar el nivel del parámetro
   NumberShape,  # Importamos NumberShape para definir parámetros numéricos como límites y tarifas
   CustomInstruction,  # Importamos CustomInstruction para definir instrucciones personalizadas de publicación
   Posting,  # Importamos Posting para crear instrucciones de movimiento de dinero
   Phase,  # Importamos Phase para especificar la fase de una publicación
   PostPostingHookArguments,  # Importamos para manejar argumentos del post-posting hook
   PostPostingHookResult,  # Importamos para definir el resultado del post-posting hook
   PostingInstructionsDirective,  # Importamos para generar directivas que incluyan instrucciones de publicación
   BalanceCoordinate,  # Importamos para definir cómo obtener saldos específicos
   BalancesObservationFetcher,  # Importamos para recuperar saldos de la cuenta
   DefinedDateTime,  # Importamos para definir tiempos específicos, como el tiempo efectivo
)

# Definimos la versión del API que estamos utilizando para este Smart Contract, en este caso es la 4.0.0
api = "4.0.0"  # Esto es un SmartContract usando el Contract Language API 4.0.0

# Definimos la versión del contrato siguiendo las prácticas de versionado semántico
version = "0.0.1"  # Usamos versionado semántico. Revisar las buenas prácticas para su uso en https://semver.org/

# Definimos los parámetros del Smart Contract
parameters = [
  Parameter(
       name='denomination',  # Nombre del parámetro, que se utilizará para identificarlo en el Smart Contract
       shape=DenominationShape(),  # Forma del parámetro, especificando que se trata de una denominación monetaria
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, aquí se establece a nivel de plantilla (TEMPLATE)
       default_value="COP",  # Valor por defecto del parámetro, que en este caso es 'COP' (Pesos Colombianos)
   ),
   # Parámetro que define el límite de sobregiro permitido para la cuenta
   Parameter(
       name="overdraft_limit",
       shape=NumberShape(),  # Forma del parámetro, en este caso un número
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, establecido a nivel de plantilla (TEMPLATE)
       description="Limite de Sobregiro",  # Descripción del parámetro
       display_name="Sobregiro maximo permitido para esta cuenta",  # Nombre para mostrar del parámetro
       default_value=Decimal(100),  # Valor por defecto del límite de sobregiro, en este caso 100
   ),
   # Parámetro que define la comisión a cobrar cuando el saldo excede el límite de sobregiro
   Parameter(
       name="overdraft_fee",
       shape=NumberShape(),  # Forma del parámetro, en este caso un número
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, establecido a nivel de plantilla (TEMPLATE)
       description="Tasa por Sobregiro",  # Descripción del parámetro
       display_name="Tarifa cobrada sobre saldos que excedan el limite de sobregiro",  # Nombre para mostrar del parámetro
       default_value=Decimal(20),  # Valor por defecto de la comisión de sobregiro, en este caso 20
   ),
]

# Funciones auxiliares (helpers)
# Función para obtener las instrucciones de publicación necesarias para cobrar la comisión de sobregiro
# Utiliza la transferencia interna de fondos para aplicar la tarifa de sobregiro
def _get_overdraft_fee_postings(overdraft_fee, denomination):
   posting_instructions = _make_internal_transfer_instructions(
       amount=overdraft_fee,  # Cantidad de la comisión de sobregiro a transferir
       denomination=denomination,  # Denominación de la comisión (en este caso COP)
       from_account_id="main_account",  # ID de la cuenta principal desde donde se transferirá la comisión
       to_account_id="internal_account",  # ID de la cuenta interna donde se depositará la comisión
   )
   return posting_instructions

# Función para generar instrucciones de transferencia interna de fondos
# Especifica los detalles de las publicaciones (créditos y débitos) que se deben realizar
def _make_internal_transfer_instructions(
   amount: Decimal,
   denomination: str,
   from_account_id: str,
   to_account_id: str,
   from_account_address: str = DEFAULT_ADDRESS,
   to_account_address: str = DEFAULT_ADDRESS,
   asset: str = DEFAULT_ASSET,
)  -> list[CustomInstruction]:
   # Definimos las publicaciones necesarias para realizar la transferencia
   postings = [
       Posting(
           credit=True,  # Indicamos que es una publicación de crédito para la cuenta destinataria
           amount=amount,  # Cantidad a transferir
           denomination=denomination,  # Denominación de la transacción
           account_id=to_account_id,  # ID de la cuenta destinataria
           account_address=to_account_address,  # Dirección de la cuenta destinataria
           asset=asset,  # Tipo de activo
           phase=Phase.COMMITTED,  # Fase de la transacción (comprometida)
       ),
       Posting(
           credit=False,  # Indicamos que es una publicación de débito para la cuenta de origen
           amount=amount,  # Cantidad a transferir
           denomination=denomination,  # Denominación de la transacción
           account_id=from_account_id,  # ID de la cuenta de origen
           account_address=from_account_address,  # Dirección de la cuenta de origen
           asset=asset,  # Tipo de activo
           phase=Phase.COMMITTED,  # Fase de la transacción (comprometida)
       ),
   ]
   # Creamos una instrucción personalizada que incluye ambas publicaciones
   custom_instruction = CustomInstruction(
       postings=postings,
   )

   # Devolvemos una lista que contiene la instrucción personalizada
   return [custom_instruction]

# Decorador que indica que este hook requiere acceso a parámetros
@requires(parameters=True)
def pre_posting_hook(
  vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
    # Obtenemos el valor actual del parámetro 'denomination' utilizando la serie temporal del parámetro
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
    
# Definimos un recolector de datos para obtener los saldos en el momento de la ejecución efectiva del hook
data_fetchers = [
    BalancesObservationFetcher(
        fetcher_id="latest_balances",  # Identificador del recolector de saldos
        at=DefinedDateTime.EFFECTIVE_DATETIME,  # Momento específico en el que se obtienen los saldos (tiempo efectivo)
    ),
]

# Decorador que indica que el hook requiere acceso a parámetros y balances observados
@requires(parameters=True)
@fetch_account_data(balances=["latest_balances"])
def post_posting_hook(
   vault, hook_arguments: PostPostingHookArguments
) -> Union[PostPostingHookResult, None]:
   # Obtenemos los valores más recientes de los parámetros
   denomination = vault.get_parameter_timeseries(name="denomination").latest()  # Denominación permitida
   overdraft_limit = vault.get_parameter_timeseries(name="overdraft_limit").latest()  # Límite de sobregiro permitido
   overdraft_fee = vault.get_parameter_timeseries(name="overdraft_fee").latest()  # Comisión por sobregiro

   # Obtenemos los saldos observados mediante el recolector de datos
   balances = vault.get_balances_observation(fetcher_id="latest_balances").balances

   # Obtenemos el saldo comprometido (neto) para la cuenta en la dirección y el activo predeterminados
   committed_balances = balances[
       BalanceCoordinate(DEFAULT_ADDRESS, DEFAULT_ASSET, denomination, Phase.COMMITTED)
   ]
   net_committed_balance = committed_balances.net

   # Verificamos si el saldo comprometido es mayor que el límite de sobregiro permitido
   if -net_committed_balance > overdraft_limit:
       # Si se excede el límite de sobregiro, generamos las instrucciones para cobrar la comisión de sobregiro
       overdraft_fee_postings = _get_overdraft_fee_postings(overdraft_fee, denomination)
       if overdraft_fee_postings:
           # Devolvemos un resultado del hook que incluye las instrucciones para publicar la comisión
           return PostPostingHookResult(
               posting_instructions_directives=[
                   PostingInstructionsDirective(
                       posting_instructions=overdraft_fee_postings,
                   )
               ]
           )
