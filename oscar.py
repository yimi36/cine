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
    pelicula.id= input_type("Introdueix nova descripció")
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

