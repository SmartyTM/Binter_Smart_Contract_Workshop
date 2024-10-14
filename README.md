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

## Solución

La solución tiene dos bloques de código que son necesarios.

### Definición del parámetro

```python
parameters = [
  Parameter(
       name='denominacion',
       shape=DenominationShape(),
       level=ParameterLevel.TEMPLATE,
       default_value="COP",
   ),
]
```

### Definir el suo del parámetro

Como segundo paso, definir como usarlo dentro de nuestro anterior bloque de código añadiendo 

```python
allowed_denomination = vault.get_parameter_timeseries(name="denominacion").latest()
```

La Resultante de este código finalmente será :

```python
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

```

## Comprobación

Por favor, ejecute el test de esta solución para comprobar su funcionamiento

```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_wrong_denomination_with_parameter_deposit
```
