from clasesgenerals import *


#==========================================================================================================
# Manteniment de pel·lícules
#==========================================================================================================
def menu_pel_licules() -> None:
    ''' Mostra la llista de pel·ícules y després un menú per al seu manteniment.
    El menú permet crear, modificar i esborrar pel·lícules. Si polsem intro tanquem el menú (return).
    No podrem esborrar una pel·lícula que s'estiga projectan en alguna sessió de qualsevol cine.
    '''

    while True:
        mostra_pel_licules()
        print("                [MENU]")
        print("1  Crea pelicula")
        print("2 Modifica pelicula")
        print("3 Esborra pelicula")
        input=input_type("Selecciona una opció vàlida")
        try:    
            if input=="1":
                crea_pel_licula()
            elif input=="2":
                modifica_pel_licula()
            elif input=="3":
                esborra_pel_licula()
        except input_type_cancel·lat:
            pass

    

          

#------------------------------------------------------------------------
def mostra_pel_licules() -> None:
    ''' Mostra informació de la llista de pel·lícules (id y info)
    '''
    for pel_licula in pel_licules:
        print(f"[{pel_licula.id}]     {pel_licula.info}")

#------------------------------------------------------------------------
def crea_pel_licula() -> None:
    ''' Crea una pel·licula i la grava. Demana la seua descripció.
    Si polsem intro llança l'excepció 'input_type_cancel·lat'. Grava els canvis.
    '''
    info=input_type("Afig una descripció")
    pel_licules.append(Pel_licula(info))
    grava_arxiu()


#------------------------------------------------------------------------
def modifica_pel_licula() -> None:
    ''' Modifica una pel·lícula. Primer demana un id de pel·licula a l'usuari i la busca entre la llista de pel·lícules.
    Demana a l'usuari una descripció nova i la reemplaça la descripció vella. Grava els canvis en disc.
    Si polsem intro llança l'excepció 'input_type_cancel·lat'.
    '''
    pelicula= demana_pel_licula()
    pelicula.info= input_type("Introdueix nova descripció")
    grava_arxiu()
#------------------------------------------------------------------------
def pel_licula_utilitzada_en_alguna_sessio(pelicula:Pel_licula) -> bool:
    '''No podem esborrar una pel·lícula si hi ha una sessió en qualsevol sala que la projecta.
    Retorna True si alguna sala la projecta, False si no.
    '''
    for cine in cines:
        for sala in cine.sales:
            for sesio in sala.sessions:
                if sesio.pel_licula == pelicula:
                    return True
    return False
#------------------------------------------------------------------------
def esborra_pel_licula():
    ''' Esborra una pel·lícula de la llista de pel·lícules. Demana l'id de la pel·licula a esborrar.
    La busca d'entre la llista de pel·lícules. Avisa si la pel·lícula es projecta en alguna sessió.
    Si polsem intro llança l'excepció 'input_type_cancel·lat'. Grava els canvis en disc.
    '''
    pelicula = demana_pel_licula()
    if pel_licula_utilitzada_en_alguna_sessio(pelicula):
        raise pel_licula_utilitzada_en_alguna_sessio
    else:
        pel_licules.remove(pelicula)
        grava_arxiu()


#==========================================================================================================
# Reserva d'una pel·lícula
#==========================================================================================================
@dataclass
class Resultat:
    '''Esta classe és una classe temporal que s'utilitza per a filtrar sessions'''
    cine: Cine
    sala: Sala
    sessio: Sessio

#------------------------------------------------------------------------
def busca_sessions_on_vore_pel_licula(pel_licula:Pel_licula, data:dt.date|None=None) -> list[Resultat]:
    ''' Recorre els cines i les seues sales buscant aquelles sessions on es projecta una pelicula determinada, de manera 
        opcional també es pot filtrar per una data determinada. El resultat es guarda en un lista de objectes
        Resultat que guarda el cine i la sessió que casen amb el filtre de pel·lícula i data/hora indicats.
        Retorna esta llista de (cine, sessió)
    '''
    lista=[]
    for cine in cines:
        for sala in cine.sales:
            for sesio in sala.sessions:
                if sesio.pel_licula==pel_licula:

                    if not data:
                        lista.append(Resultat(cine,sala,sesio)) 
                        pass                   
                    elif sesio.data_hora.date() ==data:
                        lista.append(Resultat(cine,sala,sesio))

    return lista
print(busca_sessions_on_vore_pel_licula(demana_pel_licula))

#------------------------------------------------------------------------
def selecciona_sessio_on_vore_pel_licula(pel_licula:Pel_licula, data:dt.date|None) -> tuple[Sala,Sessio]:
    ''' Busca i mostrar els cines i les sesions que projecten la pel·lícula indicada i, opcionalment, en la data indicada.
    A continuació, sol·licita l'id d'una d'este sessions. Retorna la sala i la sessió seleccionades.
    Si polsem intro llança l'excepció 'input_type_cancel·lat'.
    '''
    
    i=0
    lista = busca_sessions_on_vore_pel_licula(pel_licula,data)
    for resultat in lista:
        print(f"{resultat.cine.descripcio}        Sesió [{resultat.sessio.id}]")
        i+=1
    if i== 0:
        print("No s'han trobat sesions disponibles en aquestes condicions")
        
    id =input_type("Selecciona una opció","int")
    for resultat in lista:
        if resultat.sessio.id == id:
            return resultat.sala , resultat.sessio
#------------------------------------------------------------------------
def reserva_pel_licula() -> None:
    ''' Mostra la llista de pel·lícules.
    Demana l'id d'una pel·lícula i una data (ddmmaa).
    Busca en totes les sales aquelles sessions que projecten la pel·lícula i, opcionalment, en la data indicada.
    Pregunta que seleccionem la sessió en què volem fer una reserva. 
    Fa una reserva en esta sessió. Per a fer-la mostra una llista de les reserves, demana una fila i un seient.
    Demana un dni per a la reserva i assigna la reserva a la fila/seient indicades. Grava els canvis en disc.
    Si polsem intro eixem del procés de reserva.
    '''
    mostra_pel_licules()
    pelicula= demana_pel_licula()
    if input_type("Filtrar per data? (Y/N)").upper() == "Y":
        data= obtin_data()
    else:
        data= None
    sala, sesio = selecciona_sessio_on_vore_pel_licula(pelicula,data)
    reserva_pel_licula_en_sessio(sala,sesio)

#------------------------------------------------------------------------
def reserva_pel_licula_en_sessio(sala:Sala, sessio:Sessio) -> None:
    ''' Mostra una llista de reserves de la sessió indicada.
    Demana fila i seient on volem fer la reserva. Si la fila/seient ja estan reservats mostra un missate indicant-ho.
    Si la fila/seient esta lliures, demana un dni, crea la reserva i l'assigna a la fila/seient.
    Grava els canvis en disc. Si polsem intro eixem del procés de reserva.
    '''
    sessio.mostra_reserves()
    try:
        fila,seient = demana_seient(sala)
        if not sessio.reserves[fila][seient]:
            input_type(f'reservar ({str(fila)},{str(seient)}) (s/ )?')
            sessio.reserves[fila][seient] = demana_dades_reserva()
        elif sessio.reserves[fila][seient]:
            while True:
                input_type('Aquesta posició ja està reservada')            
        grava_arxiu()
    except input_type_cancel·lat:
        pass