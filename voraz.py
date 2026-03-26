# Propuesta Voraz para el problema del corte optimo de varillas

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


# Funcion voraz que recibe la longitud de la varilla y
# el diccionario de precios por cm, y devuelve la ganancia total 
# y los segmentos cortados

def voraz(longitud_varilla, precio_dic):
    segmentos = []
    for longitud,precio in precio_dic.items():
            rendimiento = (precio/longitud)  # rendimiento: es el precio por cm
            #Agrego longitud, precio y rendimiento a la lista de segmentos
            segmentos.append({"longitud":longitud, "precio": precio, "rendimiento": rendimiento})

# Ordeno la lista de segmentos por rendimiento de mayor a menor
    segmentos.sort(key=lambda x: x["rendimiento"], reverse=True) 
    # Llamo a la función seleccionar_segmentos para obtener la ganancia total y los segmentos cortados
    return(seleccionar_segmentos(segmentos, longitud_varilla)) 



if __name__ == "__main__":
    varilla = 4
    precios_x_cm = {1:1, 2:5, 3:8}#, 4:9, 5:10, 6:17, 7:17, 8:20, 9:24, 10:30}

    ganancia,segmentos  = voraz(varilla, precios_x_cm)
    
    print(f"Ganancia total: {ganancia}")

    for seg in segmentos:
        print(f"Longitud: {seg['longitud']}, Precio: {seg['precio']}, Rendimiento: {seg['rendimiento']:.2f}")

#   SE PUEDE EVIDENCIAR QUE VORAZ CAPTURA INICIALMENTE EL DE MAYOR VALOR, 
#   SI NO TIENE LA CAPACIDAD SIGUE CON EL SIGUIENTE DE MAYOR VALOR

