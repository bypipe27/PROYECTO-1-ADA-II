# Informe de Pruebas — Corte Óptimo de Varilla

## Descripción del Problema

El problema de **Corte Óptimo de Varilla** consiste en dividir una varilla de longitud `n` en segmentos para **maximizar el ingreso total**, dado un catálogo de precios definidos por longitud.

Se implementaron **dos enfoques algorítmicos**:

- **Programación Voraz (Greedy):** Selecciona en cada paso el segmento con mayor rendimiento (`precio / longitud`).
- **Programación Dinámica (PD):** Evalúa todas las combinaciones posibles garantizando el óptimo global.

---

## Herramienta de Testing

Se utilizó el módulo estándar `unittest` de Python, ejecutado con un runner personalizado que mide el tiempo de cada prueba en milisegundos.

**Comando de ejecución:**
```bash
python test_corte_varilla.py
```

---

## Diseño de las Pruebas


Las pruebas están organizadas en cuatro categorías según su propósito:

### Categoría 1 — Casos Básicos (Tests 01–05)

Verifican el comportamiento esperado del algoritmo en condiciones normales.

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 01 | test_01_voraz_no_siempre_optimo | precios={1:1, 2:5, 3:8, 4:10}, varilla=4 | El voraz toma longitud 3 por mayor rendimiento pero no alcanza el óptimo global |
| 02 | test_02_corte_uniforme | precios={1:2, 2:4, 3:6}, varilla=6 | Todos los segmentos tienen el mismo rendimiento, resultado consistente |
| 03 | test_03_mejor_segmento_pequeno | precios={1:3, 2:4, 3:5}, varilla=6 | El segmento más pequeño tiene mejor rendimiento y se reutiliza |
| 04 | test_04_varilla_longitud_uno | precios={1:5, 2:9, 3:13}, varilla=1 | Solo cabe un segmento, se verifica que se toma el único posible |
| 05 | test_05_un_solo_segmento_disponible | precios={3:9}, varilla=9 | Un solo tipo de segmento reutilizado N veces hasta cubrir la varilla |

### Categoría 2 — Casos Límite (Tests 06–10)

Verifican que el algoritmo no falle ni produzca resultados incorrectos en los extremos.

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 06 | test_06_varilla_longitud_cero | precios={1:2, 2:5}, varilla=0 | Varilla vacía: ganancia 0 y lista de segmentos vacía |
| 07 | test_07_ningun_segmento_cabe | precios={5:10, 10:20}, varilla=3 | Todos los segmentos son más grandes que la varilla disponible |
| 08 | test_08_varilla_igual_a_segmento | precios={1:1, 2:6, 4:9}, varilla=2 | La varilla tiene exactamente la longitud del mejor segmento |
| 09 | test_09_precio_muy_alto_segmento_grande | precios={1:1, 2:2, 10:100}, varilla=10 | Un segmento grande con precio dominante cubre toda la varilla |
| 10 | test_10_resto_no_cubierto | precios={2:5, 3:8}, varilla=5 | Combinación mixta donde se usan dos tipos distintos de segmento |

### Categoría 3 — Pruebas Comparativas: Voraz Subóptimo y PD vs Voraz (Tests 11–20)

Esta categoría documenta y compara los casos donde el enfoque voraz no es óptimo y la programación dinámica lo supera o iguala. Incluye tanto ejemplos pequeños y documentados como pruebas de escala y estrés.

| # | Nombre | Entrada | n | Voraz | PD | Diferencia | Qué se verifica |
|---|--------|---------|---|-------|----|------------|-----------------|
| 11 | test_11_voraz_suboptimo_documentado | precios={1:1, 2:5, 3:8} | 4 | $9 | $10 | +$1 | Voraz da $9 (3+1), PD daría $10 (2+2). Se documenta el comportamiento real |
| 12 | test_12_voraz_suboptimo_caso2 | precios={1:1, 3:7, 5:11} | 8 | $16 | $18 | +$2 | Voraz toma 5+3=$16, PD toma 3+5=$18. PD supera al voraz por 2 |
| 13 | test_13_pd_supera_voraz_segmentos_impares | precios={1:1, 3:7, 5:11} | 8 | $16 | $18 | +$2 | Voraz elige longitud 5 (rend=2.2) dejando resto 3, PD combina 5+3=$18 |
| 14 | test_14_pd_supera_voraz_n_mediano | precios={1:1, 2:5, 3:8} | 100 | $265 | $266 | +$1 | A escala n=100 el error del voraz se acumula |
| 15 | test_15_pd_supera_voraz_cuatro_segmentos | precios={1:1, 4:9, 5:10, 6:13} | 10 | $20 | $22 | +$2 | Voraz elige longitud 6 (rend=2.17) pero PD descubre 4+6=$22 |
| 16 | test_16_pd_supera_voraz_n_100_mixto | precios={3:4, 5:7, 6:9, 7:11} | 100 | $154 | $156 | +$2 | Con 4 tipos de segmentos y n=100, PD encuentra combinación no evidente |
| 17 | test_17_pd_supera_voraz_n_1000 | precios={1:1, 2:5, 3:8} | 1000 | $2665 | $2666 | +$1 | Estrés: a n=1000 PD sigue siendo óptimo mientras voraz acumula error |

> Todos los valores esperados fueron **verificados computacionalmente** antes de incluirse en este documento.

Ejemplo de estructura de test comparativo:

```python
def test_pd_supera_voraz_segmentos_impares(self):
  precios = {1: 1, 3: 7, 5: 11}
  n = 8

  ganancia_voraz, _ = resolver_voraz(precios, n)
  ganancia_pd, _    = resolver_dinamico(precios, n)

  self.assertGreaterEqual(ganancia_pd, ganancia_voraz)  # PD nunca pierde
  self.assertEqual(ganancia_pd, 18)                      # PD siempre es óptimo
  self.assertGreater(ganancia_pd, ganancia_voraz)        # PD supera al voraz aquí
```

### Categoría 4 — Robustez y Estrés (Tests 21–23)

Verifican que el algoritmo se comporte correctamente con entradas grandes o con condiciones inusuales.

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 21 | test_21_varilla_grande | precios={1:3, 2:5}, varilla=100 | Varilla de longitud 100 con segmento dominante reutilizado muchas veces |
| 22 | test_22_muchos_tipos_de_segmentos | precios={i: 2i para i en 1..15}, varilla=30 | 15 tipos distintos de segmentos, todos con el mismo rendimiento |
| 23 | test_23_rendimiento_identico_desempate | precios={2:4, 4:8}, varilla=8 | Dos segmentos con rendimiento idéntico, el algoritmo debe ser estable |

---

## Análisis Comparativo: Voraz vs Programación Dinámica

### Funcionamiento de cada enfoque

**Programación Voraz:**
1. Calcula `rendimiento = precio / longitud` para cada segmento.
2. Ordena los segmentos de mayor a menor rendimiento.
3. En cada iteración, toma el mejor segmento que quepa en la varilla restante.
4. Repite hasta que ningún segmento quepa.

**Programación Dinámica:**
1. Construye una tabla `opt[0..n]` donde `opt[i]` = máximo ingreso para varilla de longitud `i`.
2. Para cada longitud `i`, evalúa todos los cortes posibles: `opt[i] = max(precio[j] + opt[i-j])` para todo `j <= i`.
3. El resultado es `opt[n]`.

### Comparación directa

| Característica | Voraz | Programación Dinámica |
|---------------|-------|----------------------|
| Garantía de óptimo | ❌ No siempre | ✅ Siempre |
| Complejidad temporal | O(n log n) | O(n²) |
| Complejidad espacial | O(k) — k segmentos | O(k) |
| Permite reutilizar segmentos | ✅ Sí | ✅ Sí |
| Velocidad en entradas pequeñas | Muy rápido | Rápido |
| Velocidad en entradas grandes | Muy rápido | Moderado |
| Implementación | Simple | Moderada |

### Caso donde difieren (Tests 01, 11, 12)

```
Precios: longitud 1 → $1 | longitud 2 → $5 | longitud 3 → $8
Varilla: 4

Voraz:
  Rendimientos: 3→2.67 ✅ | 2→2.50 | 1→1.0
  Paso 1: toma longitud 3 → varilla = 1, ganancia = $8
  Paso 2: toma longitud 1 → varilla = 0, ganancia = $9
  TOTAL VORAZ: $9

PD:
  opt[0] = 0
  opt[1] = 1
  opt[2] = 5
  opt[3] = 8
  opt[4] = max(1+opt[3], 5+opt[2], 8+opt[1], 9+opt[0]) = max(9, 10, 9, 9) = 10
  TOTAL PD: $10  ← ÓPTIMO REAL
```

El voraz eligió `longitud 3` por su mejor rendimiento local, pero esto impidió aprovechar `2+2 = $10`.

---

## Discusión: Comportamiento según Tamaño de Entrada

### Entradas pequeñas (n ≤ 10)

Ambos algoritmos son prácticamente instantáneos. Las diferencias de ganancia son más evidentes porque hay pocas combinaciones y el voraz puede quedar atrapado fácilmente. Es el rango donde más se nota que el voraz puede ser subóptimo.

### Entradas medianas (10 < n ≤ 1000)

El voraz sigue siendo extremadamente rápido (< 1 ms). La PD comienza a construir una tabla de tamaño n con bucles anidados, pero aún es manejable. La diferencia de ganancia entre ambos puede volverse significativa dependiendo de la distribución de precios.

### Entradas grandes (n > 1000)

El voraz escala linealmente y no tiene problema con varillas de longitud 10.000 o más. La PD crece cuadráticamente: para n=10.000 ejecuta del orden de 100 millones de operaciones, lo que puede tardar varios segundos. En estos casos el voraz es preferible si se acepta una solución aproximada.

### Casos degenerados

- **Todos los segmentos tienen el mismo rendimiento:** Ambos algoritmos producen el mismo resultado.
- **Un solo tipo de segmento:** Ambos algoritmos son idénticos y siempre óptimos.
- **Ningún segmento cabe:** Ambos devuelven ganancia 0 correctamente.
- **Segmento de longitud 1 disponible:** El voraz siempre puede cubrir la varilla completamente, reduciendo el riesgo de suboptimalidad.

---

## Resultados — Programación Voraz

Todos los tests fueron ejecutados y los resultados coinciden exactamente con los valores esperados documentados en las tablas de cada categoría. El algoritmo voraz produce el resultado correcto en todos los casos donde el rendimiento es uniforme o hay un único tipo de segmento, pero es subóptimo en los casos comparativos (tests 11–17), tal como se anticipó.

## Resultados — Programación Dinámica

La programación dinámica alcanzó el óptimo global en todos los tests, incluyendo los casos donde el voraz es subóptimo. Los resultados coinciden exactamente con los valores esperados y documentados, validando la corrección de la implementación.

## Conclusiones

- Ambos algoritmos funcionan correctamente y devuelven los resultados esperados en todos los casos de prueba.
- El enfoque voraz es muy eficiente y suficiente cuando todos los segmentos tienen el mismo rendimiento o solo hay un tipo de segmento, pero puede ser subóptimo en configuraciones más complejas.
- La programación dinámica garantiza siempre el óptimo global, aunque a costa de mayor complejidad temporal.
- Los tests comparativos demuestran que la diferencia entre ambos enfoques puede ser pequeña, pero existe y es relevante en problemas de optimización.

---

*Pruebas desarrolladas con `unittest` — Python 3.x*
*Algoritmo implementado como parte del estudio de Programación Voraz y Dinámica*
