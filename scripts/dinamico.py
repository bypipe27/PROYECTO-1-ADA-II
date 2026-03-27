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

        # Probar todos los cortes posibles j para la longitud i
        for j in range(1, i + 1):

            # Solo considerar si existe precio para esa longitud
            if j in precios:

                # Si este corte da mejor ganancia, actualizar dp[i]
                if precios[j] + dp[i - j] > dp[i]:
                    dp[i] = precios[j] + dp[i - j]
                    corte[i] = j  # guardar qué corte fue el óptimo

    # Paso 4: Reconstruir los segmentos usando la lista de rastreo
    segmentos = []
    i = n
    while i > 0 and corte[i] > 0:
        longitud = corte[i]
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
    n = 100000

    ganancia, segmentos = resolver_dinamico(precios, n)

    print(f"Varilla de longitud: {n}")
    print(f"Precios: {precios}")
    print(f"\nGanancia óptima: ${ganancia}")
    print("Segmentos seleccionados:")
    for s in segmentos:
        print(f"  Longitud: {s} | Precio: ${precios[s]}")