
# Análisis del Proceso

## Explicación de cómo se llegó a cada modelo

El desarrollo comenzó con la implementación del enfoque voraz, dada su simplicidad conceptual: seleccionar siempre el segmento con mayor rendimiento (precio/longitud). Este modelo fue fácil de programar y permitió validar rápidamente los primeros casos de prueba, aunque pronto se identificaron sus limitaciones en cuanto a optimalidad global.

Posteriormente, se abordó la programación dinámica. El objetivo era garantizar la obtención de la solución óptima para cualquier configuración de precios y longitudes. Se diseñó una tabla `dp` para almacenar la mejor ganancia posible para cada longitud, y una lista de rastreo para reconstruir los cortes realizados.

## Dificultades encontradas

Una de las principales dificultades surgió en el llenado de la tabla dinámica. Inicialmente, el bucle interno probaba todos los cortes posibles para cada longitud:

```python
for i in range(1, n + 1):
	for j in range(1, i + 1):
		if j in precios:
			if precios[j] + dp[i - j] > dp[i]:
				dp[i] = precios[j] + dp[i - j]
				corte[i] = j
```

Este enfoque, aunque correcto, resultó ineficiente para valores grandes de `n`, ya que el número de iteraciones crecía rápidamente y el programa se volvía muy lento o incluso se bloqueaba.

## Solución implementada tras detectar el problema

Para resolver este problema de eficiencia, se optimizó el bucle interno para iterar solo sobre los cortes disponibles en el diccionario de precios, en vez de todos los posibles valores de `j`. Esto redujo drásticamente la complejidad y permitió manejar entradas grandes de manera eficiente. El fragmento optimizado es:

```python
for i in range(1, n + 1):
	max_valor = float('-inf')
	for j in precios:
		if j <= i:
			valor = precios[j] + dp[i - j]
			if valor > max_valor:
				max_valor = valor
				corte[i] = j
	dp[i] = max_valor
```

Con este cambio, el algoritmo pasó a ser mucho más eficiente y escalable.

## Decisiones de diseño relevantes

- Se priorizó la claridad y modularidad del código, separando la lógica voraz y dinámica en funciones independientes.
- Se utilizó una estructura de rastreo (`corte`) para reconstruir la secuencia de cortes óptimos, facilitando la interpretación de resultados.
- Se diseñaron pruebas exhaustivas, cubriendo tanto casos básicos como límites y de estrés, para asegurar la robustez de ambas implementaciones.

# Conclusiones

El desarrollo de ambos enfoques permitió comparar de manera directa la eficiencia y optimalidad de la programación voraz frente a la dinámica. Se comprobó empíricamente que el voraz, aunque rápido y sencillo, puede ser subóptimo en configuraciones no triviales, mientras que la programación dinámica garantiza siempre la mejor solución posible, a costa de mayor complejidad computacional.

A nivel de diseño algorítmico, la experiencia evidenció la importancia de analizar la estructura del problema antes de elegir una estrategia: problemas de optimización global suelen requerir enfoques más sofisticados que los métodos voraces. Además, la optimización del bucle interno en la PD fue clave para escalar la solución, mostrando cómo pequeños cambios en la implementación pueden tener un gran impacto en el rendimiento.

En síntesis, el trabajo permitió profundizar en la relación entre complejidad, optimalidad y eficiencia, y reforzó la necesidad de validar las soluciones tanto teórica como experimentalmente. La comparación sistemática entre ambos enfoques aportó una visión crítica sobre cuándo es aceptable sacrificar optimalidad por eficiencia y viceversa, un aprendizaje fundamental en el diseño de algoritmos.
