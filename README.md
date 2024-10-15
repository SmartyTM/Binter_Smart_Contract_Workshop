# BINTEC - Taller de Smart Contracts
Javier Antoniucci & Luis Gómez - GFT
---

# Ejercicio Cinco - Entendiendo los eventos programados y las direcciones de saldo

En este ejemplo, acumulamos un interés diario a la cuenta.

Antecedentes

Los Smart Contracts utilizan un concepto llamado **direcciones de saldo (balance addresses)**. Las direcciones de saldo en Vault se definen a través de cuatro atributos clave: activo, denominación, dirección y fase.

- Activo (asset): Clasifica el tipo de fondos de los cuales se mantienen saldos. Por defecto, el activo es COMMERCIAL_BANK_MONEY, aunque se pueden utilizar otros activos según la configuración.
- Denominación (denomination): Es la unidad en la que se mide un activo, generalmente un código de moneda. Cada cuenta tiene una lista de denominaciones permitidas que restringe las publicaciones que pueden aceptarse.
- Dirección (address): Permite almacenar saldos separados o particionar el total de fondos de una cuenta. La dirección por defecto es DEFAULT, pero se pueden crear otras según las necesidades del contrato.
- Fase (phase): Define el estado de los fondos, con valores como POSTING_PHASE_COMMITTED, POSTING_PHASE_PENDING_INCOMING, y POSTING_PHASE_PENDING_OUTGOING. Esto ayuda a diferenciar entre fondos disponibles y fondos reservados, por ejemplo, en una autorización de pago.

Esto permite al desarrollador del Smart Contract separar el dinero en la cuenta del cliente en "fondos" distintos. Estas direcciones de saldo se pueden utilizar de diversas maneras, por ejemplo, en Smart Contracts que acumulan intereses. Dado que la acumulación de intereses a menudo ocurre en un horario diferente al de la aplicación del interés, los desarrolladores de Smart Contracts suelen colocar el interés acumulado en una dirección separada. De este modo, cuando se aplica el interés, la cantidad de interés acumulado se conoce y se guarda fuera del fondo principal, conocido como DEFAULT_ADDRESS, de la cuenta.

En los Smart Contracts, las tareas basadas en el tiempo, ya sean repetitivas o puntuales, que necesitan realizarse a lo largo del ciclo de vida de una cuenta se denominan eventos programados. Ejemplos típicos de eventos programados son la acumulación diaria de intereses, el pago mensual de intereses o una tarifa anual de la cuenta.

Teniendo en cuenta que necesitamos conocer que es un ``Event Type``lo definermos como :

Cada evento programado en un Smart Contract tiene un tipo de evento asociado a él. Cada tipo de evento debe tener un nombre único dentro de cada Smart Contract y puede tener etiquetas opcionales de programación (Scheduler tags). Cada Smart Contract debe incluir una lista de todos los tipos de eventos (SmartContractEventTypes) definidos en sus activation_hook y conversion_hook.

Ahora procederemos a la Implementación de un Evento Programado. Para implementar un evento programado:

- Define el ``event type`` (tipo de evento) en los metadatos del contrato.
- Define su calendario de ejecución en el ``activation_hook``.
- Define las acciones a realizar en el ``scheduled_event_hook``. También debes especificar el ``event_type`` como argumento en los decoradores ``@requires`` o ``@fetch_account_data`` del ``scheduled_event_hook``.

Para realizar el ejercicio, completa la función ``_get_interest_accrual_postings`` del bloque de código que viene más abajo.. Esta función instruye la transferencia del monto acumulado desde la dirección "ACCRUED_OUTGOING" de "internal_account" a la dirección "ACCRUED_INCOMING" de la cuenta del cliente, la cual puedes referenciar usando ``vault.account_id``.

Tambien define un evento programado "ACCRUE_INTEREST" que se ejecuta todos los días y llama a ``_get_interest_accrual_postings``.

Añade, primero, estos bloques de código a nuestro ya conocido Smart Contract ``tutorial_contract.py```

```python
# Parametro Adicional
   Parameter(
       name="gross_interest_rate",
       shape=NumberShape(min_value=0, max_value=1, step=Decimal("0.01")),
       level=ParameterLevel.TEMPLATE,
       description="Gross interest rate",
       display_name="Rate paid on positive balances",
   ),
```

También este 

```python 
# Additional data fetcher
   BalancesObservationFetcher(
       fetcher_id="end_of_day_balances",
       at=RelativeDateTime(
           origin=DefinedDateTime.EFFECTIVE_DATETIME, find=Override(hour=0, minute=0, second=0),
       ),
   ),
```

y también este Helper, que es donde va usted a añadir el código que completa el ejercicio.

```python
# Funciones Helper Adicionales
def _get_interest_accrual_postings(vault, effective_datetime):
   # Insert your code here.


def _calculate_accrued_interest(vault, effective_datetime):
   denomination = vault.get_parameter_timeseries(name="denomination").latest()


   # Obtener el Saldo Efectivo
   balances= vault.get_balances_observation(fetcher_id="end_of_day_balances").balances
   effective_balance = balances[
       BalanceCoordinate(DEFAULT_ADDRESS, DEFAULT_ASSET, denomination, Phase.COMMITTED)
   ].net


   # Obtener la tasa de interés bruta y calcule la tasa diaria
   gross_interest_rate = vault.get_parameter_timeseries(name="gross_interest_rate").at(at_datetime=effective_datetime)
   daily_rate = gross_interest_rate/365


   accrued_interest = _precision_accrual(effective_balance * daily_rate)


   return accrued_interest

def _precision_accrual(amount):
  return amount.quantize(Decimal('.00001'), rounding=ROUND_HALF_UP)

```

Una vez implementada su solición al problema, no olvide probar con este comando de consola para pasar los tests oportunos.

```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_e05_execution_schedule
```

## Solución

Para implementar la Solución, comenzaremos con la creación de un Tipo de Evento

```python 
event_types = [
   SmartContractEventType(name="ACCRUE_INTEREST"),
]
```

Para después crear el activation hook que lanza el evento y completa el proceso en el momento definido.


```python

def activation_hook(
   vault, hook_arguments: ActivationHookArguments
) -> Union[ActivationHookResult, None]:


   # Acumulación de Interest diario a la media noche
   interest_accrual_event = ScheduledEvent(
       expression=ScheduleExpression(hour=0, minute=0, second=0),
       start_datetime=hook_arguments.effective_datetime,
   )


   return ActivationHookResult(
       scheduled_events_return_value={
           "ACCRUE_INTEREST": interest_accrual_event,
       }
   )


@requires(event_type="ACCRUE_INTEREST", parameters=True)
@fetch_account_data(event_type="ACCRUE_INTEREST", balances=["end_of_day_balances"])
def scheduled_event_hook(
   vault, hook_arguments:ScheduledEventHookArguments
) -> Union[ScheduledEventHookResult, None]:
if hook_arguments.event_type == "ACCRUE_INTEREST":
       interest_accrual_postings = _get_interest_accrual_postings(vault, hook_arguments.effective_datetime)
        if interest_accrual_postings:
           return ScheduledEventHookResult(
               posting_instructions_directives=[
                   PostingInstructionsDirective(
                       posting_instructions=interest_accrual_postings,
                   )
               ],
           )
def _get_interest_accrual_postings(vault, effective_datetime):
   accrued_interest = _calculate_accrued_interest(vault, effective_datetime)
   denomination = vault.get_parameter_timeseries(name="denomination").latest()


   if accrued_interest > 0:
       posting_instructions = _make_internal_transfer_instructions(
           amount=accrued_interest,
           denomination=denomination,
           from_account_id="internal_account",
           from_account_address="ACCRUED_OUTGOING",
           to_account_id=vault.account_id,
           to_account_address="ACCRUED_INCOMING"
       )
       return posting_instructions

```
