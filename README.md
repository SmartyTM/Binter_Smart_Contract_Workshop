# BINTEC - Taller de Smart Contracts
Javier Antoniucci & Luis Gómez - GFT
---

# Ejercicio Tres - Entendiendo los Parámetros y los Requisitos de Hooks

En este ejercicio, cambiamos la restricción de denominación para que sea configurable en lugar de estar codificada de forma fija.


## Definición de Parámetros en Smart Contracts
En Thought Machine Vault, los parámetros son valores configurables que **permiten ajustar la lógica de negocio de un Smart Contract sin necesidad de modificar el código directamente.** Los parámetros se definen en el contrato y luego se pueden establecer o actualizar durante la configuración del producto. Esto incluye, por ejemplo, valores como la denominación permitida, límites de transacción, o tasas de interés.

Los parámetros son muy útiles para garantizar la flexibilidad y reutilización de los Smart Contracts, permitiendo adaptar un producto a diferentes condiciones sin tener que reescribir o redeployar el código.

El ejercicio comienza con añadiendo este bloque de código a nuestro ```tutorial_contract.py``` que estamos usando para estos ejercicios :

```python
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

```

Compruebe que el ejercicio consta de insertar 2 bloques de código que permitan definir el parámetro y poder usarlo más adelante.

Copie este código en ```tutorial_contract.py``` y añada los elementos que faltan.

Una vez tenga finalizado el código, ejecute el test en consola usando :

```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_wrong_denomination_with_parameter_deposit
```


