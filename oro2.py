nombre = input("introduce tu nombre: ")
print("Bienvenido(a), ", nombre)
cuenta = int(input("coloca la cantidad de cuentas a sumar y procesar: "))
X=1
total=0
while X <=cuenta:
    total += int(input(f"introduce la cantidad a sumar de oro de la cuenta {X}: "))
    print ("total de oro acumulado es ", total)
    X+=1
total *= 0.95
pregunta = input("desea introducir el valor por oro/$?, S/N: ")
pregunta = pregunta.lower()
if pregunta == 's' :
    precio_oro = float(input("valor del oro por $: "))
    precio_oro = precio_oro / 1000
    print ('Oro total acumulado: ', total)
    print (round(total*precio_oro,2), "$/G")
elif pregunta == 'n' :
    print ('Oro total acumulado: ', total)
    print (total*0.00084, "$/G")