operador = input("¿Qué quieres hacer? sumar, restar, multiplicar, dividir, exit: ")


while operador != "exit":
    numero1 = float(input("Introduzca un numero: "))
    numero2 = float(input("Introduzca un numero: "))

    if operador == "sumar":
        resultado = numero1 + numero2
        if resultado % 1 == 0:
            resultado = int(resultado)
        print(f"El resultado es: {resultado}")

    elif operador == "restar":
        resultado = numero1 - numero2
        print(f"El resultado es: {resultado}")

    elif operador == "multiplicar":
        resultado = numero1 * numero2
        print(f"El resultado es: {resultado}")

    elif operador == "dividir":
        if numero2 == 0:
            print("Error: no se puede dividir entre 0.")
        else:
            resultado = numero1 / numero2
            print(f"El resultado es: {resultado}")
    operador = input("¿Qué quieres hacer? sumar, restar, multiplicar, dividir, exit: ")
print("Terminado")