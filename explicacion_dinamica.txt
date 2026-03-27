Explicación intuitiva: Corte óptimo de varilla (Programación dinámica)

Idea principal
- Tenemos una varilla de longitud n y una tabla de precios p[i] para segmentos de longitud i.
- Queremos cortar la varilla (posiblemente en varios segmentos) para maximizar el ingreso total.
- Observación clave: la mejor solución para una varilla de longitud n contiene, para cualquier primer corte, soluciones óptimas para la varilla restante. Esta propiedad se llama subestructura óptima.

Cómo razonar el problema
- Si cortamos primero un segmento de longitud i, obtenemos p[i] por ese segmento y queda una varilla de longitud n-i. La mejor forma de aprovechar lo restante es la ganancia óptima para n-i.
- Por tanto, la mejor ganancia para longitud n es el máximo sobre todas las opciones de primer corte: max_{1<=i<=n} (p[i] + mejor_ganancia(n-i)).

Recurrencia y tablas
- Definimos R[j] = ganancia máxima para una varilla de longitud j.
- Recurrencia: R[0] = 0; para j>=1,
  R[j] = max_{1<=i<=j} (p[i] + R[j-i]).
- Además guardamos s[j] = el valor de i que alcanza el máximo (primer corte óptimo), para poder reconstruir la solución.

Algoritmo bottom-up (intuitivo)
1. Creamos un arreglo R[0..n] inicializado con 0 y s[0..n] con 0.
2. Iteramos j desde 1 hasta n:
   - Probamos todos los cortes posibles i=1..j.
   - Calculamos ganancia = p[i] + R[j-i].
   - Elegimos el i que da mayor ganancia; guardamos R[j] y s[j].
3. Para reconstruir los segmentos, empezamos en j=n, tomamos i = s[j], añadimos ese segmento, hacemos j = j - i y repetimos hasta j=0.

Ejemplo concreto (precios: p={1:1, 2:5, 3:8}, n=4)
- j=1: opciones: i=1 -> 1 + R[0] = 1 → R[1] = 1, s[1]=1
- j=2: i=1 -> 1 + R[1] = 2; i=2 -> 5 + R[0] = 5 → R[2] = 5, s[2]=2
- j=3: i=1 -> 1 + R[2] = 6; i=2 -> 5 + R[1] = 6; i=3 -> 8 + R[0] = 8 → R[3] = 8, s[3]=3
- j=4: i=1 -> 1 + R[3] = 9; i=2 -> 5 + R[2] = 10; i=3 -> 8 + R[1] = 9; i=4 -> p[4] (0 si no existe) → R[4] = 10, s[4]=2
Reconstrucción: s[4]=2 → corte 2, queda 2 → s[2]=2 → corte 2. Solución: dos segmentos de longitud 2 (5+5=10).

Complejidad
- Tiempo: O(n^2) porque para cada j hacemos hasta j pruebas.
- Espacio: O(n) para almacenar R y s.

Por qué no usar un enfoque voraz
- Un criterio voraz típico sería escoger siempre el segmento con mejor rendimiento p[i]/i. Esto falla porque puede ignorar combinaciones de cortes que juntas dan mayor beneficio.
- Programación dinámica garantiza óptimo al explorar todas las combinaciones de primer corte + solución óptima de la parte restante.

Relación con tu código
- La función `corte_optimo_dinamica` construye exactamente las tablas R y s en forma bottom-up.
- La función `reconstruir_solucion` recorre s para producir los segmentos finales.

Consejos prácticos
- Si algunos p[i] no están dados, tratarlos como 0 (no disponibles) o completar la tabla según el problema.
- Para grandes n, si los precios tienen estructura especial (por ejemplo, totalmente convexos o lineales), puede haber métodos más rápidos; en general, O(n^2) es estándar.

Resumen (en una línea)
- Descomponer: prueba cada posible primer corte i, suma precio del corte y mejor resultado para lo que queda; memoiza/tabla para evitar repetir trabajo y reconstruye la solución guardando las decisiones.
