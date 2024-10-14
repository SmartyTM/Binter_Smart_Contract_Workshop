# BINTEC - Taller de Smart Contracts
Javier Antoniucci & Luis Gómez - GFT
---

# Ejercicio 2 - Entendamos los hooks

En este ejercicio, restringimos nuestro producto para aceptar solo ingresos en COP (Pesos Colombianos).

**Antecedentes** Los Smart Contracts se basan en el concepto de hooks. 
Los hooks son funciones de Python que son llamadas por Vault durante eventos específicos en el ciclo de vida del producto. Este ejercicio demuestra cómo se puede usar un hook de pre-publicación para validar una transacción antes de que sea aceptada en el libro mayor de Vault.

Para comprobar que una publicación es válida antes de modificar el saldo de una cuenta, debemos agregar verificaciones en el ``pre_posting_hook``. Esto nos permite rechazar la publicación si no cumple con los criterios necesarios definidos para esta cuenta en la lógica de negocio del Smart Contract.



## Uso
Vamos a usar este comando en nuestro Terminal para poder hacer el test que nos muestre que funciona

```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_e02_wrong_denomination_deposit

```

## ¿Qué es un pre_posting_hook?

En Thought Machine Vault, un ```pre_posting_hook``` es un hook que se ejecuta antes de que una transacción sea aceptada en el sistema. Cuando desarrollamos un Smart Contract, el ```pre_posting_hook``` nos permite implementar lógica que valide ciertos aspectos de una transacción antes de que esta modifique el saldo de una cuenta. Este tipo de hook es crucial para garantizar que se cumplan reglas específicas antes de aceptar cualquier operación, como la validación de la moneda, el límite de transacciones o la verificación de requisitos personalizados.

Para comprobar que una publicación es válida antes de modificar el saldo de una cuenta, debemos agregar verificaciones en el ```pre_posting_hook```. Esto nos permite rechazar la publicación si no cumple con los criterios necesarios definidos para esta cuenta en la lógica de negocio del Smart Contract.

## Ejemplo específico para este ejercicio:

Utiliza el ```pre_posting_hook``` para verificar si la denominación de todas las publicaciones enviadas es en 'COP'. Si no es en 'COP', rechaza la publicación con el código de motivo WRONG_DENOMINATION.

Vamos a añadir este código a nuestro Smart Contract del ejercicio ```tutorial_contract.py```


```python
from typing import Union
from contracts_api import (
   PrePostingHookArguments,
   PrePostingHookResult,
   Rejection,
   RejectionReason,
)

api = "4.0.0"
version = "1.0.0"

def pre_posting_hook(
   vault, hook_arguments: PrePostingHookArguments
) -> Union[PrePostingHookResult, None]:
   # Inserte su código aquí para poder procesar el pre-posting hook

```

El propósito de este ejercicio es que creemos un bloque de código que vaya dentro de la función pre_posting_hook que permita leer el previo de la publicación del posting, identificar en que moneda se está realizando la transacción y que acepte sólo esta publicación si corresponde con la moneda identificada para la cuenta.

## La Solución

La solución para este ejercicio se completa con la inserción de este bloque de código:

```python
   if any(posting.denomination != 'COP' for posting in hook_arguments.posting_instructions):
       return PrePostingHookResult(
           rejection=Rejection(
               message="Las transacciones solo pueden ser realizadas en Pesos Colombianos (COP)",
               reason_code=RejectionReason.WRONG_DENOMINATION,
           )
       )
```

En nuestra solución, iteramos sobre la lista de publicaciones que se pasan a nuestro hook, y devolvemos un rechazo si alguna de ellas no está en COP.

## Explicación adicional:

Cuando estamos utilizando el ```pre_posting_hook``` en un Smart Contract para Thought Machine Vault, es común recibir una lista de publicaciones (es decir, transacciones) que deben ser validadas antes de ser aceptadas. En este caso, nuestro objetivo es asegurarnos de que todas las publicaciones estén denominadas en pesos colombianos (COP). Por ello, recorremos cada elemento de esta lista, y si encontramos alguna publicación que no esté en COP, la rechazamos devolviendo un mensaje de rechazo con el motivo correspondiente. Esto asegura que **solo se acepten transacciones que cumplan con las reglas de negocio definidas para este producto.**

Para mayor detalle, vuelva a ejecutar el test usando el comando 
```console
python3 -m unittest simple_tutorial_tests.TutorialTest.test_e02_wrong_denomination_deposit

```


