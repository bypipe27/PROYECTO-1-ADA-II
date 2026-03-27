# 1. Análisis teórico del problema: Corte óptimo de varilla

## Descripción formal del problema

El problema del **corte óptimo de varilla** consiste en determinar la forma más rentable de dividir una varilla de longitud total $n$, dado un conjunto de precios asociados a cada posible longitud.

### Definición formal

- Sea $n \in \mathbb{N}$ la longitud total de la varilla.
- Sea $p_i$ el precio de una varilla de longitud $i$, para $1 \leq i \leq n$.
- Se permite cortar la varilla en segmentos de longitudes enteras.

El objetivo es encontrar una partición de la varilla en segmentos:

$$
n = l_1 + l_2 + \cdots + l_k
$$

tal que el ingreso total:

$$
R(n) = p_{l_1} + p_{l_2} + \cdots + p_{l_k}
$$

sea máximo.

Cabe aclarar que, algunas observaciones que se pueden tener acerca
de este problema son:
- No existe restricción en la cantidad de cortes.
- Se permite no realizar cortes si esto maximiza el ingreso.
- El problema presenta **subestructura óptima**, ya que la solución óptima para una varilla de longitud $n$ depende de soluciones óptimas de subproblemas más pequeños.


## Justificación de pertenencia a la clase NP

El problema del corte de varilla, en su formulación clásica de optimización, puede asociarse a su versión de decisión:

> Dado un entero $n$, un arreglo de precios $p_i$, y un valor objetivo $V$, ¿existe una forma de cortar la varilla tal que el ingreso total sea al menos $V$?

### Verificación en tiempo polinómico

Dada una solución candidata **(una lista de cortes),** es posible:

- Verificar que la suma de las longitudes sea igual a $n$.
- Calcular el ingreso total sumando los precios correspondientes.
- Comparar el resultado con el valor $V$.

Estos pasos se pueden realizar en tiempo $O(n)$, por lo tanto, la
solución puede ser verificada en `tiempo polinómico`, lo que nos
indica que la versión de decisión del problema sí pertenece a la
clase **NP**.

Pero a pesar de que el problema pertenece a la clase NP, no es
`NP-completo`, debido a que admite soluciones en tiempo polinómico
mediante programación dinámica. Por tanto, también pertenece a
la clase **P**.


## Análisis de la complejidad computacional

### Enfoque ingenuo (recursivo)

Una solución recursiva sin optimización considera todas las posibles formas de cortar la varilla.

La recurrencia es:

$$
R(n) = \max_{1 \leq i \leq n} (p_i + R(n - i))
$$

#### Complejidad:

- Se generan múltiples subproblemas repetidos.
- El número de llamadas crece exponencialmente.

$$
T(n) = O(2^n)
$$

Esto hace que el enfoque sea **ineficiente para valores grandes de \( n \)**.


### Enfoque voraz

Un algoritmo voraz selecciona en cada paso el corte que maximiza una ganancia local (por ejemplo, mayor precio por unidad de longitud).

#### Complejidad:

- Selección de cortes: $O(n)$
- Ejecución total: $O(n)$

#### Limitación:

Este enfoque **no garantiza una solución óptima global**, ya que el problema no cumple la propiedad de elección voraz.



### Enfoque de programación dinámica

Se basa en almacenar soluciones a subproblemas para evitar recomputaciones.

#### Estrategia:

- Se construye un arreglo $R$ donde:

$$
R[j] = \max_{1 \leq i \leq j} (p_i + R[j - i])
$$

#### Complejidad:

- Tiempo:  $O(n^2)$
- Espacio:  $O(n)$