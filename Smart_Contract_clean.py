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

# Constantes y configuración
# Definimos la versión del API que estamos utilizando para este Smart Contract, en este caso es la 4.0.0
api = "4.0.0"  # Esto es un SmartContract usando el Contract Language API 4.0.0

# Definimos la versión del contrato siguiendo las prácticas de versionado semántico
version = "0.0.1"  # Usamos versionado semántico. Revisar las buenas prácticas para su uso en https://semver.org/

# Parámetros del Smart Contract
parameters = [
  Parameter(
       name='denomination',  # Nombre del parámetro, que se utilizará para identificarlo en el Smart Contract
       shape=DenominationShape(),  # Forma del parámetro, especificando que se trata de una denominación monetaria
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, aquí se establece a nivel de plantilla (TEMPLATE)
       default_value="COP",  # Valor por defecto del parámetro, que en este caso es 'COP' (Pesos Colombianos)
   ),
   Parameter(
       name="overdraft_limit",
       shape=NumberShape(),  # Forma del parámetro, en este caso un número
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, establecido a nivel de plantilla (TEMPLATE)
       description="Limite de Sobregiro",  # Descripción del parámetro
       display_name="Sobregiro maximo permitido para esta cuenta",  # Nombre para mostrar del parámetro
       default_value=Decimal(100),  # Valor por defecto del límite de sobregiro, en este caso 100
   ),
   Parameter(
       name="overdraft_fee",
       shape=NumberShape(),  # Forma del parámetro, en este caso un número
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, establecido a nivel de plantilla (TEMPLATE)
       description="Tasa por Sobregiro",  # Descripción del parámetro
       display_name="Tarifa cobrada sobre saldos que excedan el limite de sobregiro",  # Nombre para mostrar del parámetro
       default_value=Decimal(20),  # Valor por defecto de la comisión de sobregiro, en este caso 20
   ),
   Parameter(
       name="gross_interest_rate",
       shape=NumberShape(min_value=0, max_value=1, step=Decimal("0.01")),  # Definición del rango válido para la tasa
       level=ParameterLevel.TEMPLATE,  # Nivel del parámetro, establecido a nivel de plantilla (TEMPLATE)
       description="Gross interest rate",  # Descripción del parámetro
       display_name="Rate paid on positive balances",  # Nombre para mostrar del parámetro
   ),
]

# Recolectores de datos
data_fetchers = [
    BalancesObservationFetcher(
        fetcher_id="latest_balances",  # Identificador del recolector de saldos
        at=DefinedDateTime.EFFECTIVE_DATETIME,  # Momento específico en el que se obtienen los saldos (tiempo efectivo)
    ),
    BalancesObservationFetcher(
       fetcher_id="end_of_day_balances",  # Identificador del recolector de saldos al final del día
       at=RelativeDateTime(
           origin=DefinedDateTime.EFFECTIVE_DATETIME, find=Override(hour=0, minute=0, second=0),
       ),
   ),
]

# Definimos los tipos de eventos del contrato
event_types = [
   SmartContractEventType(name="ACCRUE_INTEREST"),  # Evento para la acumulación de interés
]

# Hooks del Smart Contract
# Hook de activación que se ejecuta al activar el contrato
def activation_hook(
   vault, hook_arguments: ActivationHookArguments
) -> Union[ActivationHookResult, None]:
   # Acumula intereses diariamente a la medianoche
   interest_accrual_event = ScheduledEvent(
       expression=ScheduleExpression(hour=0, minute=0, second=0),  # Expresión para programar el evento a medianoche
       start_datetime=hook_arguments.effective_datetime,  # Fecha y hora de inicio del evento
   )
   return ActivationHookResult(
       scheduled_events_return_value={
           "ACCRUE_INTEREST": interest_accrual_event,  # Asignación del evento programado
       }
   )

# Hook para eventos programados (en este caso, acumulación de intereses)
@requires(event_type="ACCRUE_INTEREST", parameters=True)
@fetch_account_data(event_type="ACCRUE_INTEREST", balances=["end_of_day_balances"])
def scheduled_event_hook(
   vault, hook_arguments: ScheduledEventHookArguments
) -> Union[ScheduledEventHookResult, None]:
   if hook_arguments.event_type == "ACCRUE_INTEREST":
       # Obtener las instrucciones para acumular interés
       interest_accrual_postings = _get_interest_accrual_postings(vault, hook_arguments.effective_datetime)
       if interest_accrual_postings:
           return ScheduledEventHookResult(
               posting_instructions_directives=[
                   PostingInstructionsDirective(
                       posting_instructions=interest_accrual_postings,  # Instrucciones para publicar el interés acumulado
                   )
               ],
           )

# Hook previo a la publicación
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

# Hook posterior a la publicación
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
       BalanceCoordinate(DEFAULT_ADDRESS, DEFAULT_ASSET, denomination, Phase.COMMITTED)  # Coordenadas del saldo comprometido
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
                       posting_instructions=overdraft_fee_postings,  # Instrucciones para cobrar la comisión
                   )
               ]
           )

# Funciones auxiliares (helpers)
# Función para obtener las instrucciones de publicación necesarias para cobrar la comisión de sobregiro
def _get_overdraft_fee_postings(overdraft_fee, denomination):
   # Utiliza la transferencia interna de fondos para aplicar la tarifa de sobregiro
   posting_instructions = _make_internal_transfer_instructions(
       amount=overdraft_fee,  # Cantidad de la comisión de sobregiro a transferir
       denomination=denomination,  # Denominación de la comisión (en este caso COP)
       from_account_id="main_account",  # ID de la cuenta principal desde donde se transferirá la comisión
       to_account_id="internal_account",  # ID de la cuenta interna donde se depositará la comisión
   )
   return posting_instructions

# Función para obtener las instrucciones de acumulación de interés
def _get_interest_accrual_postings(vault, effective_datetime):
   # Calculamos el interés acumulado hasta la fecha efectiva
   accrued_interest = _calculate_accrued_interest(vault, effective_datetime)
   denomination = vault.get_parameter_timeseries(name="denomination").latest()  # Obtenemos la denominación actual
   if accrued_interest > 0:
       # Creamos las instrucciones de transferencia interna para aplicar el interés acumulado
       posting_instructions = _make_internal_transfer_instructions(
           amount=accrued_interest,  # Monto del interés acumulado
           denomination=denomination,  # Denominación del interés
           from_account_id="internal_account",  # ID de la cuenta de donde se extrae el interés
           from_account_address="ACCRUED_OUTGOING",  # Dirección de la cuenta de origen
           to_account_id=vault.account_id,  # ID de la cuenta destinataria (cuenta del cliente)
           to_account_address="ACCRUED_INCOMING"  # Dirección de la cuenta destinataria
       )
       return posting_instructions

# Función para calcular el interés acumulado
def _calculate_accrued_interest(vault, effective_datetime):
   denomination = vault.get_parameter_timeseries(name="denomination").latest()  # Obtenemos la denominación actual

   # Obtener el saldo efectivo al final del día
   balances = vault.get_balances_observation(fetcher_id="end_of_day_balances").balances
   effective_balance = balances[
       BalanceCoordinate(DEFAULT_ADDRESS, DEFAULT_ASSET, denomination, Phase.COMMITTED)  # Coordenadas del saldo
   ].net

   # Obtener la tasa de interés bruta y calcular la tasa diaria
   gross_interest_rate = vault.get_parameter_timeseries(name="gross_interest_rate").at(at_datetime=effective_datetime)
   daily_rate = gross_interest_rate / 365  # Dividimos la tasa bruta por 365 para obtener la tasa diaria

   # Calculamos el interés acumulado usando la tasa diaria
   accrued_interest = _precision_accrual(effective_balance * daily_rate)

   return accrued_interest

# Función para asegurar la precisión del cálculo del interés acumulado
def _precision_accrual(amount):
  return amount.quantize(Decimal('.00001'), rounding=ROUND_HALF_UP)  # Ajuste de precisión al quinto decimal

# Función para generar instrucciones de transferencia interna de fondos
def _make_internal_transfer_instructions(
   amount: Decimal,
   denomination: str,
   from_account_id: str,
   to_account_id: str,
   from_account_address: str = DEFAULT_ADDRESS,
   to_account_address: str = DEFAULT_ADDRESS,
   asset: str = DEFAULT_ASSET,
) -> list[CustomInstruction]:
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