# BINTEC - Taller de Smart Contracts
Javier Antoniucci & Luis Gómez - GFT
---

# Ejercicio Cuatro - Entendiendo las directivas de hooks y los recolectores de datos
En este ejercicio, cobramos una comisión si el saldo de la cuenta excede un límite de sobregiro.

## Antecedentes
Cada hook tiene su propio tipo de retorno, lo cual le permite comunicar los resultados de la lógica de negocio al resto de Vault. La mayoría de estos tipos de retorno pueden contener directivas, permitiendo que los hooks afecten el estado de Vault al crear publicaciones, enviar notificaciones o modificar horarios. Sin embargo, el pre-posting hook se considera estar en la "ruta caliente" (hot path), lo que significa que su ejecución debe ser lo más rápida posible. Por esta razón, sus valores de retorno se limitan a rechazos y no contienen directivas.

Además de los parámetros, los Smart Contracts suelen necesitar acceder a otros datos, como saldos y publicaciones. La recuperación optimizada de datos nos permite definir de manera precisa qué datos se necesitan, ayudando a mantener la lógica de negocio compacta y mejorando el rendimiento al garantizar que el contrato solo recupere los datos que son necesarios para su ejecución.

El post-posting hook nos permite realizar acciones basadas en la lógica de negocio después de la ejecución de una publicación. Los recolectores de datos nos permiten definir qué intervalos de tiempo o puntos específicos en el tiempo son de interés para la lógica de negocio. En este ejercicio, agregamos una verificación al post-posting hook para cobrar una comisión al cliente si excede su límite de sobregiro. Necesitamos recuperar el saldo comprometido en el momento de la publicación para evaluar correctamente si la cuenta tiene sobregiro después de la publicación.

## Definición del Ejercicio
Usa los parámetros ``overdraft_limit`` y ``overdraft_fee``, definidos a continuación, para hacer la lógica de nuestro producto configurable.

- ``overdraft_limit``: Este parámetro define el límite máximo de sobregiro permitido para la cuenta. Es configurable para que podamos ajustar la cantidad de dinero que un cliente puede sobregirar antes de que se le apliquen comisiones. Esto nos permite personalizar el comportamiento del producto según las necesidades del cliente o las políticas del banco.

- ``overdraft_fee``: Este parámetro establece la comisión que se cobrará cuando el saldo de la cuenta exceda el límite de sobregiro definido. Al hacer este parámetro configurable, podemos ajustar el costo del sobregiro de acuerdo con las condiciones de mercado, regulaciones, o el perfil de riesgo del cliente.

```python
# Parametros Adicionales
   Parameter(
       name="overdraft_limit",
       shape=NumberShape(),
       level=ParameterLevel.TEMPLATE,
       description="Limite de Sobregiro",
       display_name="Sobregiro maximo permitido para esta cuenta",
       default_value=Decimal(100),
   ),
   Parameter(
       name="overdraft_fee",
       shape=NumberShape(),
       level=ParameterLevel.TEMPLATE,
       description="Tasa por Sobregiro",
       display_name="Tarifa cobrada sobre saldos que excedan el limite de sobregiro",
       default_value=Decimal(20),
   ),
```

A continuación incluiremos un ``Helper``. 
Un `Helper` tiene un papel clave en facilitar ciertas tareas repetitivas o complejas, ayudando a simplificar la lógica de negocio del contrato. Los helpers son funciones auxiliares diseñadas para encapsular funcionalidades comunes y permitir la reutilización del código, haciéndolo más limpio, mantenible y eficiente.
Este Helper nos ayudará a poder transferir las tasas que se puedan recaudar de un saldo que ha excedido el límite de Sobregiro hasta una cuenta interna del banco.

```python
# Helper functions
def _get_overdraft_fee_postings(overdraft_fee, denomination):
   posting_instructions = _make_internal_transfer_instructions(
       amount=overdraft_fee,
       denomination=denomination,
       from_account_id="main_account", # vault.account_id
       to_account_id="internal_account",
   )
   return posting_instructions
```

y a continuación, añadiremos el bloque de código que creará los Postings (publicaciones en el ledger) de los movimientos que se generan del cobro de las tasas y se transfieren a una cuenta interna.

```python
def _make_internal_transfer_instructions(
   amount: Decimal,
   denomination: str,
   from_account_id: str,
   to_account_id: str,
   from_account_address: str = DEFAULT_ADDRESS,
   to_account_address: str = DEFAULT_ADDRESS,
   asset: str = DEFAULT_ASSET,
)  -> list[CustomInstruction]:
   postings = [
       Posting(
           credit=True,
           amount=amount,
           denomination=denomination,
           account_id=to_account_id,
           account_address=to_account_address,
           asset=asset,
           phase=Phase.COMMITTED,
       ),
       Posting(
           credit=False,
           amount=amount,
           denomination=denomination,
           account_id=from_account_id,
           account_address=from_account_address,
           asset=asset,
           phase=Phase.COMMITTED,
       ),
   ]
   custom_instruction = CustomInstruction(
       postings=postings,
   )
   return [custom_instruction]

```

El ejercicio tendrá como objetivo, usando todo el código expuesto anteriormente e incorporado al Smart Contract ``tutorial_contract.py``, implementar el ``post_posting_hook`` para realizar lo siguiente:

- **Recuperar los saldos** de la cuenta en el momento de la ejecución del hook mediante la definición de un data_fetcher, un concepto utilizado en los Smart Contracts de Thought Machine Vault para optimizar la recuperación de datos necesarios.

- **Verificar si el saldo neto** COMPROMETIDO (en la dirección de cuenta DEFAULT_ADDRESS y del tipo de activo DEFAULT_ASSET) es mayor que el sobregiro permitido.

- **Cobrar una comisión (Tasa)** si el saldo excede el sobregiro permitido, utilizando las funciones auxiliares proporcionadas.

Introduzca su código en este bloque de código y añadalo conjuntamente a ``tutorial_contract.py```

```python

data_fetchers = [
  # Inserte su código aquí para Recuperar el Saldo
]


# Inserte su código aquí para requerir los parámetros
def post_posting_hook(
  vault, hook_arguments: PostPostingHookArguments
) -> Union[PostPostingHookResult, None]:
  # Inserte su código aquí para Verificar y Cobrar una comisión (Tasa)
```


Una vez creado el código, utilice este comando de consola para poder comprobar que pasa los tests

```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_e04_fee_applied_after_withdrawal
```
