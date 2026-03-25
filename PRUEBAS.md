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

## Diseño de las Pruebas — Programación Voraz

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

### Categoría 3 — Voraz Subóptimo Documentado (Tests 11–12)

Casos diseñados específicamente para exponer las limitaciones del enfoque voraz frente a la Programación Dinámica.

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 11 | test_11_voraz_suboptimo_documentado | precios={1:1, 2:5, 3:8}, varilla=4 | Voraz da $9 (3+1), PD daría $10 (2+2). Se documenta el comportamiento real |
| 12 | test_12_voraz_suboptimo_caso2 | precios={1:1, 3:7, 4:10}, varilla=6 | Voraz elige longitud 4 pero PD con 3+3 obtiene mayor ganancia |

> Estos tests no buscan que el voraz falle: buscan **documentar honestamente** su comportamiento conocido para compararlo más adelante con PD.

### Categoría 4 — Robustez y Estrés (Tests 13–15)

Verifican que el algoritmo se comporte correctamente con entradas grandes o con condiciones inusuales.

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 13 | test_13_varilla_grande | precios={1:3, 2:5}, varilla=100 | Varilla de longitud 100 con segmento dominante reutilizado muchas veces |
| 14 | test_14_muchos_tipos_de_segmentos | precios={i: 2i para i en 1..15}, varilla=30 | 15 tipos distintos de segmentos, todos con el mismo rendimiento |
| 15 | test_15_rendimiento_identico_desempate | precios={2:4, 4:8}, varilla=8 | Dos segmentos con rendimiento idéntico, el algoritmo debe ser estable |



## Categoría 5 - Casos donde la Programación Dinámica supera claramente al Voraz (Test 16-20)

Estos tests ilustran situaciones donde el enfoque dinámico logra una ganancia mayor que el voraz, mostrando la importancia de considerar todas las combinaciones posibles:

| # | Nombre | Entrada | Qué se verifica |
|---|--------|---------|-----------------|
| 16 | test_16_pd_supera_voraz_gran_diferencia | precios={1:2, 3:7, 4:8}, varilla=6 | Voraz elige 3+3 ($14), pero PD encuentra 4+1+1 ($12), mostrando que a veces el voraz no es óptimo, pero en este caso la diferencia es pequeña. |
| 17 | test_17_pd_optimo_con_cortes_pequenos | precios={1:1, 2:5, 5:10}, varilla=10 | Voraz toma 5+5 ($20), pero PD con cinco cortes de 2 ($25) obtiene mucho más. |
| 18 | test_18_pd_optimo_con_combinacion_no_evidente | precios={1:2, 2:5, 3:7, 7:13}, varilla=14 | Voraz toma 7+7 ($26), pero PD con siete cortes de 2 ($35) es mucho mejor. |
| 19 | test_19_pd_optimo_con_segmentos_intermedios | precios={1:1, 2:5, 4:8, 5:10}, varilla=8 | Voraz toma 5+2+1 ($16), pero PD con dos cortes de 4 ($16) iguala, pero si los precios cambian levemente, la PD puede superar al voraz. |
| 20 | test_20_pd_supera_voraz_con_varilla_grande | precios={1:1, 2:5, 3:8, 4:10}, varilla=20 | Voraz repite el segmento de mayor rendimiento, pero PD encuentra una combinación que maximiza la ganancia total. |

Estos ejemplos muestran que la programación dinámica puede encontrar soluciones óptimas que el voraz pasa por alto, especialmente cuando la mejor combinación no es evidente localmente.

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




## Resultados — Programación Voraz

*(Pendiente: completar con resultados reales tras ejecución)*

## Resultados — Programación Dinámica

*(Pendiente: completar tras implementación y ejecución)*

## Conclusiones

*(Pendiente: completar tras comparar ambos enfoques)*

---

*Pruebas desarrolladas con `unittest` — Python 3.x*
*Algoritmo implementado como parte del estudio de Programación Voraz y Dinámica*
