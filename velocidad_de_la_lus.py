import math
k=(10**290)
c = 299792458
año_milisegundos = 365.2422*24*60*60*1000
eq1 = math.sqrt((c**2)-(((1/año_milisegundos)**2)*(c**2)))*k
eq2 = eq1/c
#print(f'Para que un año propio se mida como un milisegundo por un cuerpo externo, este tiene que viajar a {eq1}m/s o lo que es equivalente a {eq2} veces la velocidad de la luz')
v_integrer=int(round(eq1,0))
def dividir_a_mano(numerador,div):
    numerador=str(numerador)
    cuociente_lista=[]
    respuesta_temp=[]
    for n in numerador:
        respuesta_temp.append(n)
        numero_dividir=int("".join(respuesta_temp))
        cuocinete=numero_dividir//div
        if cuocinete == 0:
            continue
        cuociente_lista.append(str(cuocinete))
        respuesta_temp=[str(numero_dividir%div)]
    return "".join(cuociente_lista)
print(dividir_a_mano(v_integrer,c))

        

            


