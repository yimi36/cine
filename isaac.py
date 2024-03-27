from clasesgenerals import *

#==========================================================================================================
# Reserves
#==========================================================================================================
def busca_cine(id: int) -> Cine: #acabada
    for cine in cines:
        if cine.id == id:
            return cine
    raise cine_no_trobat

    ''' Busca un cine pel seu id en la llista de cines.
    Si ela troba retorna el cine, sinó llança l'excepció 'cine_no_trobat'
    '''

#------------------------------------------------------------------------
def mostra_cine_i_sales() -> None: #acabada
    for cine in cines:
        print('---------------------------------------')
        print(f'CINE({str(cine.id)}).{str(cine.descripcio)}:')
        for sala in cine.sales:
            print(f'      SALA({str(sala.id)}).{str(sala.descripcio)}')

    ''' Mostra els cines (id i descripció) i les sales d'estos cines (id, descripció).
    '''

#------------------------------------------------------------------------
def selecciona_cine() -> Cine:#acabada
    cls()
    mostra_cine_i_sales()
    while True:
        try:
            id = input_type('selecciona un cine:','int')
            return busca_cine(id)
        except cine_no_trobat:
            print('cine no existeix')

    '''Mostra una llista de cines i les seues sales.
    Demana un id de cine i el busca. Si el troba retorna el cine.
    Si polsem intro llança l'excepció 'input_type_cancel·lat'.
    '''

#------------------------------------------------------------------------
def demana_sessio(sala:Sala) -> Sessio:#acabada
    while True:
        try:
            id = input_type('selecciona una sessió:','int')
            sessio = sala.busca_sessio(id)
            return sessio
        except sessio_no_trobada:
            print('sessio no trobada')
        
    ''' Demana l'id d'una sessió, la busca d'entre la llista de sessions de la sala i retorna la sessio.
    Si no la troba llança l'excepció 'sessio_no_trobada'. Si polsem intro llança l'excepció 'input_type_cancel·lat'.
    '''

#------------------------------------------------------------------------
def demana_seient(sala:Sala) -> tuple[int,int]:#acabada
    while True:
        fila = input_type('selecciona una fila:','int')
        seient = input_type('selecciona una seient:','int')
        if  fila > sala.files and fila <= 0:
            print('fila no valida')
            continue
        if  seient > sala.seients_per_fila and seient <= 0:
            print('seient no valid')
            continue
        return (fila,seient)
    
    ''' Demana una fila (int) i un seient (int). Estos valors es verifiquen contra 
        els valors de files i seient de la sala que li passem. Retorna una fila i
        seient vàlids per a la sala. Si polsem intro llança l'excepció 'input_type_cancel·lat'.
    '''
    
#==========================================================================================================
# Manteniment de sessions
#==========================================================================================================

def manteniment_sessions(cine:Cine) -> None:#progres
    while True:
        cls()
        mostra_sales_i_sessions(cine)
        sala = demana_sala(cine)
        print(f'MANTENIMENT DE SESSIONS: SALA({str(sala.id)}) {str(sala.descripcio)}')
        opcio = input_type(' 1-Crea 2-Modifica 3-Esborra 4-Reserves Opcio?','int')
        try:
            if opcio == 1:
                crea_sessio(sala)
            elif opcio == 2:
                modifica_sessio(sala)
            elif opcio == 3:
                esborra_sessio(sala)
            elif opcio == 4:
                mateniment_reserves(cine,sala)
        except input_type_cancel·lat:
            continue

    ''' Mostra la informació de les sales i les seues sessions del cine indicat.
    Demana l'id d'una sala i mostra una menú amb les opciones de crear, modificar, esborrar i mantinedre les reserves
    per a esta sala seleccionada. 
    '''

#------------------------------------------------------------------------
def mostra_sales_i_sessions(cine:Cine) -> None:#acabada
    print(f'CINE({str(cine.id)}).{str(cine.descripcio)}:')
    for sala in cine.sales:
        print('--------------------------------')
        print(f'      SALA({str(sala.id)}).{str(sala.descripcio)}:')
        if sala.sessions:
            for sessio in sala.sessions:
                print(f'       SESSIÓ({str(sessio.id)})[{str(sessio.data_hora)}].{str(sessio.pel_licula.info)}({str(sessio.preu_entrada)}€)')
        else:
            print('       NO HI HAN SESSIONS')

    ''' Mostra informació del cine que li passem com a paràmetre (id i descripció).
    A continuació, mostra informaciño de les sales del cine (id i descripció) i de cadascuna de les
    seues sessions (id, data y hora, info de la pel·licula y el preu).
    '''

#------------------------------------------------------------------------
def demana_sala(cine:Cine) -> Sala:#acabada
    while True:
        try:
            id = input_type('selecciona una sala','int')
            sala = cine.busca_sala(id)
            return sala
        except sala_no_trobada:
            print('sala no trobada')
            continue

    ''' Demana l'id d'un sala, la busca d'entre la llista de sales del cine i retorna la sala.
    Si no la troba llança l'excepció 'sala_no_trobada'. Si polsem intro llança l'excepció 'input_type_cancel·lat'
    '''

#------------------------------------------------------------------------
def crea_sessio(sala:Sala) -> None:#acabada
    print('---------CREACIÓ DE SESSIONS---------')
    data = obtin_data_hora()
    id = demana_pel_licula()
    preu = input_type('Preu € de la pel·licula','float')
    Sessio(sala,data,id,preu)
    while True:
        if input('Fet, intro per a continuar') == '':
            break

    ''' Crea un objete sessió. Demana data y hora de la sessió, l'id de la pel·lícula que es projecta i el preu de l'entrada.
    La sessió s'afegix a llista de sessions de la sala que li passem. Si polsem intro eixim i es cancel·la la creació.
    '''

#------------------------------------------------------------------------
def modifica_sessio(sala:Sala) -> None:#acabada
    print('---------MODIFICACIÓ DE SESSIONS---------')
    sessio = demana_sessio(sala)
    data_nova = obtin_data_hora()
    pel_licula_nova = demana_pel_licula()
    preu_nou = input_type('Preu € de la pel·licula','float')
    sessio.data_hora = data_nova
    sessio.pel_licula = pel_licula_nova
    sessio.preu_entrada = preu_nou
    while True:
        if input('Fet, intro per a continuar') == '':
            break

    ''' Modica una de les sessions de la sala que li passem.
    Demana l'id d'una sessio i la busca en la sala. A continuació la modifiquem, preguntant data y hora de la sessió,
    l'id de la pel·lícula que es projecta i el preu d'entrada. Es graven els canvis en disc.
    Si polsem intro es cancel·la la modificació de la sessió.
    '''

#------------------------------------------------------------------------
def esborra_sessio(sala:Sala) -> None:#acabada
    print('---------ESBORRA SESSIONS---------')
    sessio = demana_sessio(sala)
    sala.sessions.remove(sessio)
    while True:
        if input('Fet, intro per a continuar') == '':
            break
    ''' Esborra una de les sessions de la sala que li passem.
    Demana l'id d'una sessio i la busca en la sala. A continuació l'esborra. Es graven els canvis en disc.
    Si polsem intro es cancel·la l'esborrat de la sessió.
    '''

#------------------------------------------------------------------------
def demana_dades_reserva() -> Reserva:
    dni = input_type('dni per a la reserva:','str')
    return Reserva(dni)
    ''' Demna un dni i crea una Reseerva amb ell. Retorna la reserva.
    '''

#------------------------------------------------------------------------
def mateniment_reserves(cine:Cine, sala:Sala) -> None:
    while True:
        print('---------LLISTA DE RESERVES---------')
        print(f'Cine:{str(cine.descripcio)} - Sala:{str(sala.descripcio)}\n')
        for sessio in sala.sessions:
            print(f'SESSIO({str(sessio.id)}) [{str(sessio.data_hora)}]. {str(sessio.pel_licula.info)} ({str(sessio.preu_entrada)}€)')
            nombre_fila = 0
            for file in sessio.reserves:
                print(f'fila {str(nombre_fila)}: {str(file)}')
                nombre_fila += 1
        try:
            sessio = demana_sessio(sala)
            fila,seient = demana_seient(sala)
            if not sessio.reserves[fila][seient]:
                input_type(f'reservar {str(fila)},{str(seient)} (s/ )?')
                sessio.reserves[fila][seient] = demana_dades_reserva()
            elif sessio.reserves[fila][seient]:
                input_type(f'Eliminar la reserva {str(fila)},{str(seient)} (s/ )?')
                sessio.reserves[fila][seient] = None
        except input_type_cancel·lat:
            break
    ''' Recorrer les sessions de la sala indicada i mostra de cadascuna d'elles l'estat de les reserves.
    A continuació, demana l'id d'una de le sessions, busca la sessió que correspon a este id, i demana
    un fila i seient. Si la fila/seient ja està reservada pregunta si volem esborrar-la i, si constestem que S, 
    l'esborra i grava els canvis en disc. Per contra, si la fila/seient no està reservada, demana un dni
    amb què crea una reserva per a esta fila/seient i grava els canvis. Si polsem intro al demanar 
    l'id de sessió, fila, seient, dni ens eixim.
    '''