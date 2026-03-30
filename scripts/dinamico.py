def resolver_dinamico(precios, n):
    """
    Resuelve el problema de corte de varilla usando Programación Dinámica.
    precios: dict {longitud: precio}
    n: longitud total de la varilla
    Retorna (ganancia_optima, lista de segmentos seleccionados)
    """

    # Paso 1: Crear tabla dp de tamaño n+1 iniciada en ceros
    # dp[i] = mejor ganancia posible para una varilla de longitud i
    dp = [0] * (n + 1)

    # Paso 2: Lista de rastreo para reconstruir los cortes
    # corte[i] = qué longitud de segmento se cortó para obtener dp[i]
    corte = [0] * (n + 1)

    # Paso 3: Llenar la tabla dp desde longitud 1 hasta n
    for i in range(1, n + 1):
        max_valor = float('-inf')

        # Probar solo los cortes que existen en el diccionario
        for j in precios:
            if j <= i:  # solo si el corte es válido
                valor = precios[j] + dp[i - j]

                if valor > max_valor:
                    max_valor = valor
                    corte[i] = j  # guardar qué corte fue el óptimo

        dp[i] = max_valor

    # Paso 4: Reconstruir los segmentos usando la lista de rastreo
    segmentos = []
    i = n
    while i > 0:
        longitud = corte[i]

        if longitud == 0:
            break

        segmentos.append({
            "longitud": longitud,
            "precio": precios[longitud],
            "rendimiento": precios[longitud] / longitud
        })
        i -= longitud

    return dp[n], segmentos


if __name__ == "__main__":

    # Ejemplo: caso donde PD supera al voraz
    precios = {1: 1, 2: 5, 3: 8} 
    n = 1000

    ganancia, segmentos = resolver_dinamico(precios, n)

    print(f"Varilla de longitud: {n}")
    print(f"Precios: {precios}")
    print(f"\nGanancia óptima: ${ganancia}")
    cortes = [s['longitud'] for s in segmentos]
    print("Cortes a realizar:", cortes)