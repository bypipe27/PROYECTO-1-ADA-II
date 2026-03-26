# Propuesta de Solución mediante un Enfoque Voraz

## Analogía

**Analogía directa con Problema de Mochila (clase):**
El problema de corte de varilla es **estructuralmente idéntico** al problema de mochila 0/1:
- En mochila: elegimos objetos con peso y valor limitados por capacidad.
- En varilla: elegimos cortes con longitud y precio, limitados por longitud total.

Por eso **aplicamos las mismas 3 estrategias voraces** vistas en clase (mayor valor, menor peso/longitud, mejor relación).

---

## 1. Definición Clara del Criterio de Selección

### 1.1 El Problema
Tienes una varilla de longitud $n$ unidades. Cortarla en piezas de diferentes longitudes tiene diferentes precios. **Pregunta:** ¿Cómo cortar la varilla para ganar máximo dinero?

**Ejemplo simple:**
- Varilla de 10 metros
- Precios: 1 metro = \$1, 2 metros = \$5, 3 metros = \$8, 4 metros = \$9, ...
- Opción 1: No cortar, venderla entera → \$30
- Opción 2: Cortarla de forma inteligente → ¿ganancia mayor?

### 1.2 Criterio Voraz: Máxima Relación Precio/Longitud

**¿En qué consiste el voraz para varilla?** 

En lugar de pensar "¿qué corte me da más dinero?", pensamos: **"¿qué corte me da más dinero por cada metro que uso?"**

Esto es exactamente lo que vimos en mochila con "mejor relación valor/peso".

$$\text{Relación = } \frac{\text{Precio de pieza}}{\text{Longitud de pieza}} = \frac{p[i]}{i}$$

**Estrategia voraz concreta:**
En cada paso, **siempre** elegir el corte cuya relación precio/longitud sea máxima, y repetir hasta agotar la varilla.

**Algoritmo voraz:**

```python
def seleccionar_segmentos(segmentos_ordenados, longitud_varilla):
    ganancias_total = 0
    segmentos_seleccionados = []

    while longitud_varilla > 0:
        mejor_segmento = None
        for s in segmentos_ordenados:
            if s["longitud"] <= longitud_varilla:
                mejor_segmento = s
                break
        if mejor_segmento is None:
            break

        ganancias_total += mejor_segmento["precio"]
        longitud_varilla -= mejor_segmento["longitud"]
        segmentos_seleccionados.append(mejor_segmento)

    return ganancias_total, segmentos_seleccionados


def voraz(longitud_varilla, precio_dic):
    segmentos = []
    for longitud, precio in precio_dic.items():
        rendimiento = (precio / longitud)  # rendimiento: precio por unidad
        segmentos.append({"longitud": longitud, "precio": precio, "rendimiento": rendimiento})

    # Ordeno por rendimiento (descendente) y selecciono repetidamente
    segmentos.sort(key=lambda x: x["rendimiento"], reverse=True)
    return seleccionar_segmentos(segmentos, longitud_varilla)
```

**Complejidad temporal:** $O(n^2)$ en el peor caso.

---

## 2. Justificación del Diseño

### 2.1 Fundamentación del Criterio

El criterio de máxima relación precio/longitud es intuitivamente justificable:

1. **Eficiencia de valor:** Maximizar la ganancia por unidad de longitud utilizada.
2. **Greedy choice property:** En cada paso, se selecciona la opción localmente óptima (máxima relación).
3. **Rapidez computacional:** No requiere exploración exhaustiva ni tablas de memorización.

### 2.2 Ventajas del Enfoque Voraz

| Aspecto | Ventaja |
|--------|---------|
| **Complejidad temporal** | $O(n^2)$ frente a $O(n^2)$ de PD, pero más simple en práctica |
| **Uso de memoria** | $O(1)$ espacios adicionales vs $O(n)$ en PD |
| **Implementación** | Algoritmo simple y directo |
| **Comprensión** | Fácil de explicar y entender |

### 2.3 Lógica de Selección

El diseño se basa en la premisa de que seleccionar piezas con **mejor precio por unidad de longitud** lleva a resultados óptimos:

- Si una pieza tiene relación $\frac{p[i]}{i} > \frac{p[j]}{j}$, entonces usar esa pieza es preferible.
- Repetir este proceso hasta agotar la varilla maximizará la ganancia.

---

## 3. Discusión Sobre Optimalidad

### 3.1 ¿Garantiza Optimalidad?

**Respuesta directa: NO.**

Así como en la clase vimos que la estrategia voraz de "mejor valor/peso" en la mochila **no siempre da solución óptima**, aquí ocurre exactamente lo mismo.

**Por qué falla el voraz:**

El algoritmo voraz hace **decisiones locales óptimas** (elige el mejor corte AHORA), pero **no garantiza solución global óptima** (mejor resultado TOTAL).

Un corte que se ve bueno ahora puede dejar un "resto" de varilla que es imposible de aprovechar bien. Mientras que un corte "menos atractivo" ahora podría permitir combinaciones mejores después.

### 3.2 Contraejemplo Concreto: El Voraz Falla

**Varilla de longitud 4 metros, tabla de precios:**

| Longitud (m) | 1 | 2 | 3 | 4 |
|----------|---|---|---|---|
| Precio ($) | 3 | 5 | 6 | 7 |
| **Relación ($/m)** | **3.0** ✓ mejor | 2.5 | 2.0 | 1.75 |

**Lo que hace el Voraz (elige mejor relación siempre):**
1. Mejor relación = 3.0 (corte de 1m) → ganancia \$3, resta 3m
2. Mejor relación = 3.0 (corte de 1m) → ganancia \$3, resta 2m  
3. Mejor relación = 2.5 (corte de 2m) → ganancia \$5, resta 0m
4. **Total Voraz = \$3 + \$3 + \$5 = \$11**

**Lo que hace la Programación Dinámica (prueba todas las combinaciones):**
- Opción A: Corte de 4m entero → \$7
- Opción B: Dos cortes de 2m → \$5 + \$5 = \$10
- Opción C: Cuatro cortes de 1m → \$3 + \$3 + \$3 + \$3 = \$12 ✅ **ÓPTIMA**
- Opción D: Corte de 3m + 1m → \$6 + \$3 = \$9

**Resultado:**
- Voraz elige ganancias locales: **\$11**
- Óptima global es: **\$12**
- **El voraz se equivocó por \$1**

### 3.3 Por Qué Falla Aquí

El voraz piensa: "1 metro es lo mejor (\$3/m), tomaré dos veces."

Lo que NO ve: "cuatro cortes de 1 metro juntos dan más que dos de 1 metro + uno de 2 metros."

**Es exactamente lo mismo que vimos en clase con mochila:**
- Estrategia voraz "mejor valor/peso" eligió mal
- Solo explorando TODAS las combinaciones (como PD) encontramos la mejor

---

## 4. Comparación Conceptual con Programación Dinámica

### 4.1 Tabla Comparativa

| Criterio | Enfoque Voraz | Programación Dinámica |
|----------|---------------|-----------------------|
| **Optimalidad** | Heurística (NO óptima en general) | Garantiza solución óptima |
| **Complejidad temporal** | $O(n^2)$ | $O(n^2)$ |
| **Complejidad espacial** | $O(1)$ | $O(n)$ |
| **Construcción de solución** | Greedy choice property | Subestructura óptima |
| **Estrategia** | Local → Global | Bottom-up (tablas) |
| **Decisión** | Basada en relación actual | Basada en análisis exhaustivo |
| **Esfuerzo computacional** | Menor (selección + cálculo de relación) | Mayor (llenar tabla dp) |

### 4.2 Diferencia Fundamental en Estrategia

#### Programación Dinámica:

```
dp[i] = máx(p[i], máx(dp[i-j] + dp[j]) para j = 1..i-1)
```

- Analiza **todas las posibles combinaciones** de cortes.
- Construye soluciones a partir de subproblemas resueltos óptimamente.
- Garantiza encontrar la ganancia máxima.

#### Enfoque Voraz:

```
En cada paso, elige el corte con máxima relación precio/longitud
```

- Toma decisiones locales sin considerar futuras combinaciones.
- No revisa si existen combinaciones mejores.
- Puede fallar en casos donde una decisión "mediocre" ahora permite combinaciones óptimas después.

### 4.3 ¿Cuándo Usar Cada Enfoque?

#### Usar Voraz si:
- Se busca solución **rápida** (tiempo real).
- Se necesita algoritmo **simple** y **fácil de implementar**.
- La optimalidad no es crítica (problema admite heurísticas).
- Análisis previo muestra que el voraz funciona bien para los datos esperados.

#### Usar PD si:
- Se requiere **garantizar optimalidad**.
- El tiempo de ejecución es menos crítico que la calidad de la solución.
- El tamaño del problema es **manejable** ($n \leq 1000$ típicamente).
- Se permite usar memoria $O(n)$.

### 4.4 Perspectiva Teórica

**Problema de la Mochila:** El corte de varilla es análogo al problema de la mochila 0/1.

- **Mochila voraz:** Seleccionar items con máxima relación valor/peso → **Falla** en general.
- **Mochila PD:** Uso de programación dinámica → **Óptima** garantizada.

Esto refuerza que algoritmos voraces, aunque intuitivos, no siempre garantizan optimalidad en problemas combinatorios.

---

## 5. Conclusiones: 

### 5.1 Las 3 Conclusiones Principales

**"Voraz es simple y rápido."**
- ✓ Fácil implementar
- ✓ Complejidad razonable $O(n^2)$
- ✓ No necesita memoria adicional $O(1)$

**"No siempre es correcto."**
- ✗ No garantiza solución óptima
- ✗ Decide localmente, sin ver futuro
- ✗ Puede fallar (vimos ejemplo: voraz da \$11, óptima es \$12)

**"DP es más general."**
- ✓ Garantiza solución óptima
- ✓ Explora todas las opciones
- ✓ Pero usa más memoria y algo más complejo

### 5.2 Cuándo Usar Cada Uno

| Situación | Usa | Razón |
|-----------|-----|-------|
| Necesitas **garantía** de solución mejor | **PD** | Aunque cueste más tiempo |
| Prioridad es **velocidad** | **Voraz** | Si una solución "buena" es suficiente |
| Sistema **tiempo real** | **Voraz** | No hay tiempo para DP |
| **Análisis académico** | **PD** | Demuestra comprensión profunda |

---