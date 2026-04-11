# Propuesta de Solución mediante un Enfoque Voraz
## 0. Alcance

Este documento describe **exactamente** la estrategia implementada en `voraz.py`:

- Se calcula el rendimiento $\frac{precio}{longitud}$ de cada longitud disponible.
- Se ordenan los segmentos **una sola vez** por rendimiento descendente.
- En cada iteración se toma el **primer segmento factible** (el de mayor rendimiento que cabe en la longitud restante).
- Si no cabe ninguno, el algoritmo termina (puede quedar longitud sin usar).

> Nota: El problema de corte de varilla se modela más naturalmente como una variante de **mochila no acotada** (se pueden repetir longitudes).

---

## 1. Definición clara del criterio de selección

### 1.1 Problema
Dada una varilla de longitud total $n$ y un diccionario de precios por longitud, se busca una partición en cortes para maximizar la ganancia total.

### 1.2 Criterio voraz usado
El criterio implementado es:

$$
\text{rendimiento}(\ell)=\frac{precio(\ell)}{\ell}
$$

Se priorizan longitudes con mayor rendimiento y, durante la construcción de la solución, se elige siempre la primera que quepa en el remanente.

### 1.3 Pseudocódigo  `voraz.py`

```text
VORAZ(longitud_varilla, precio_dic)
    segmentos ← []
    PARA CADA (longitud, precio) EN precio_dic:
        rendimiento ← precio / longitud
        segmentos.agregar({longitud, precio, rendimiento})

    ordenar(segmentos, clave=rendimiento, descendente=True)

    ganancia_total ← 0
    seleccionados ← []
    restante ← longitud_varilla

    MIENTRAS restante > 0:
        mejor ← None

        PARA CADA s EN segmentos:   // ya ordenados
            SI s.longitud ≤ restante:
                mejor ← s
                romper

        SI mejor ES None:
            romper

        ganancia_total ← ganancia_total + mejor.precio
        restante ← restante - mejor.longitud
        seleccionados.agregar(mejor)

    RETORNAR (ganancia_total, seleccionados)
```

---

## 2. Justificación del diseño

### 2.1 Por qué este criterio
- **Intuición económica:** prioriza “precio por unidad de longitud”.
- **Simplicidad:** evita explorar combinaciones completas.
- **Velocidad práctica:** fácil de implementar y rápido para tamaños medianos.

### 2.2 Complejidad real de esta implementación
Sea:
- $m =$ cantidad de longitudes disponibles en `precio_dic`.
- $k =$ cantidad de cortes realizados.

Entonces:

- Construcción de segmentos: $O(m)$
- Ordenamiento por rendimiento: $O(m\log m)$
- Selección iterativa (peor caso): $O(k\,m)$

Complejidad total:

$$
O(m\log m + k\,m)
$$

Caso típico con longitudes desde 1 hasta $n$: $m\approx n$ y $k\le n$, por lo que el peor caso puede verse como $O(n^2)$.

### 2.3 Espacio
- Lista de segmentos: $O(m)$
- Lista de seleccionados (como en el código): $O(k)$

Espacio adicional total: $O(m+k)$.

---

## 3. Discusión: ¿garantiza optimalidad?

### 3.1 Respuesta corta
**No.** Es una heurística: toma decisiones localmente buenas, pero no garantiza óptimo global.

Esto ocurre porque el criterio usado en `voraz.py` solo evalúa el rendimiento inmediato de cada segmento y luego escoge el primer corte que cabe en la longitud restante. En otras palabras, el algoritmo prioriza una buena decisión local, pero no revisa si esa elección deja una combinación mejor para el resto de la varilla.

Además, si en algún momento ningún segmento cabe en la longitud restante, el proceso se detiene y puede quedar una parte sin usar. Esa condición también muestra que el método no explora todas las posibilidades de corte.

### 3.2 Contraejemplo 

- Longitud de varilla: $n=4$
- Precios: $\{1:1,\;2:5,\;3:8\}$

Rendimientos:
- $1 \to 1/1 = 1.0$
- $2 \to 5/2 = 2.5$
- $3 \to 8/3 \approx 2.67$ (mejor)

Orden voraz: $3, 2, 1$.

Ejecución voraz:
1. Toma 3 (cabe en 4): ganancia $8$, restante $1$
2. 3 no cabe, 2 no cabe, toma 1: ganancia $+1$, restante $0$
3. Total voraz = $9$

Óptimo global:
- Cortar $2+2$ da $5+5=10$

Conclusión:

$$
\text{Voraz}=9 \;<\; 10=\text{Óptimo}
$$

Por lo tanto, **el voraz falla** en este caso.

### 3.3 Intuición de la falla
Elegir primero la pieza de mejor rendimiento ($3$) bloquea la combinación $2+2$, que produce mayor ganancia total.

---

## 4. Comparación conceptual con Programación Dinámica

### 4.1 Enfoque PD para este problema
Para longitudes disponibles en un conjunto $L$:

$$
dp[i] = \max_{\ell \in L,\;\ell\le i}\left(precio(\ell) + dp[i-\ell]\right),\quad dp[0]=0
$$

Esto evalúa todas las posibilidades relevantes y garantiza optimalidad.

### 4.2 Comparación resumida

| Criterio | Voraz  | Programación Dinámica |
|---|---|---|
| Tipo | Heurística | Método exacto |
| Garantía de óptimo | No | Sí |
| Complejidad tiempo | $O(m\log m + k\,m)$ | $O(n\,m)$ (o $O(n^2)$ si $m\approx n$) |
| Espacio | $O(m+k)$ | $O(n)$ |
| Idea central | Mejor rendimiento local | Mejor combinación global |

### 4.3 Cuándo conviene cada uno
- **Voraz:** cuando importa rapidez/simplicidad y se acepta no garantizar óptimo.
- **PD:** cuando se exige solución óptima y el costo extra de cómputo/memoria es aceptable.

### 4.4 Diferencia fundamental en la estrategia

#### Enfoque voraz (`voraz.py`)
- Calcula el rendimiento de cada longitud disponible una sola vez.
- Ordena los segmentos de mayor a menor rendimiento.
- En cada paso toma el primer segmento que todavía cabe en la varilla restante.
- No vuelve a evaluar combinaciones previas ni intenta comparar futuros arreglos posibles.

#### Programación dinámica (`dinamico.py`)
- Construye una tabla `dp` desde la longitud 1 hasta `n`.
- Para cada longitud `i`, prueba todos los cortes válidos `j` que aparecen en `precios`.
- Calcula `valor = precios[j] + dp[i - j]` y conserva el mejor.
- Guarda también qué corte produjo ese máximo para reconstruir la solución final.

#### Consecuencia práctica
El voraz decide con base en la mejor razón precio/longitud disponible en ese instante. La programación dinámica, en cambio, compara todas las formas de formar cada sublongitud y conserva la mejor ganancia alcanzable. Por eso el primero puede quedarse con una decisión localmente buena pero globalmente peor, mientras que el segundo sí preserva la mejor opción para cada subproblema.


---

## 5. Validación experimental con tests

Para reforzar el análisis teórico, se incluyen resultados representativos de `test.py`.

### 5.1 Ejemplos de pruebas relevantes

| Caso | Parámetros | Resultado Voraz | Resultado PD | Interpretación |
|---|---|---|---|---|
| Voraz subóptimo documentado | $n=4$, precios $\{1:1,2:5,3:8\}$ | $9$ | $10$ | Confirma que voraz no garantiza óptimo global |
| Rendimientos uniformes | $n=6$, precios $\{1:2,2:4,3:6\}$ | $12$ | $12$ | Ambos coinciden cuando no hay ventaja combinatoria |
| Ningún segmento cabe | $n=3$, precios $\{5:10,10:20\}$ | $0$ | $-\infty$ (convención actual en PD) | Ambos reflejan inviabilidad, con distinta convención de retorno |

### 5.2 Comando de ejecución de pruebas

Desde la carpeta `scripts/`:

```bash
python -m unittest test.py
```

### 5.3 Conclusión de la validación

Las pruebas respaldan lo expuesto en este documento:

- El voraz es útil y eficiente como heurística.
- La programación dinámica conserva la ventaja cuando se requiere optimalidad garantizada.

---

## 6. Conclusión final

El enfoque voraz resulta útil cuando se busca una solución simple, rápida y fácil de implementar. Su criterio de selección por rendimiento permite obtener buenos resultados en varios casos, pero su alcance sigue siendo local: no revisa todas las combinaciones posibles de cortes.

La programación dinámica, en cambio, evalúa los subproblemas necesarios para construir la mejor solución global. Por eso, aunque requiere más trabajo de cálculo y memoria, sí ofrece una garantía formal de optimalidad.

En síntesis:

- **Voraz:** conveniente como aproximación rápida, sin garantía de óptimo.
- **PD:** preferible cuando importa asegurar la mejor ganancia.

Así, ambos enfoques cumplen funciones distintas: uno prioriza simplicidad y rapidez; el otro, exactitud y máxima ganancia.