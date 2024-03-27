from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import os
import platform
import pickle



#==========================================================================================================
# Excepcions
#==========================================================================================================
class pelicula_no_trobada(Exception):           # type: ignore
    pass
class sessio_no_trobada(Exception):
    pass
class sala_no_trobada(Exception):
    pass
class cine_no_trobat(Exception):
    pass
class input_type_cancel·lat(Exception):
    pass
class pel_licula_utilitzada_en_una_sessio(Exception):
    pass
class data_invalida(Exception):
    pass
class hora_invalida(Exception):
    pass
#==========================================================================================================
# VARIABLES GLOBALS
#==========================================================================================================
pel_licules:list[Pel_licula] = []
cines:list[Cine] = []

#==========================================================================================================
# CLASSES
#==========================================================================================================
class Reserva:
    def __init__(self, dni:str) -> None:
        self.dni = dni

    def __str__(self) -> str:
        return self.dni
    
    __repr__ = __str__

#==========================================================================================================
class Pel_licula:
    id:int = 1
    def __init__(self, info:str) -> None:
        self.id = Pel_licula.id
        Pel_licula.id += 1
        self.info = info

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Pel_licula):
            return False
        return obj.id==self.id
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['id_'] = Pel_licula.id
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        Pel_licula.id = state ['id_']

#==========================================================================================================
class Cine:
    id:int = 1
    def __init__(self, descripcio:str) -> None:
        self.id = Cine.id
        Cine.id += 1
        self.descripcio = descripcio
        self.sales:list[Sala] = []

    def busca_sala(self, id_sala:int) -> Sala:
        '''Busca una sala pel seu id en la llista de sales del cine.
        Si la troba retorna la llista, sinó llança l'excepció 'sala_no_trobada'
        '''
        for sala in self.sales:
            if sala.id == id_sala:
                return sala
        raise sala_no_trobada
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['id_'] = Cine.id
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        Cine.id = state['id_']

#==========================================================================================================
class Sala:
    id:int = 1
    def __init__(self, cine: Cine, descripcio:str, files: int, seients_per_fila:int) -> None:
        self.id = Sala.id
        Sala.id += 1
        self.descripcio = descripcio
        self.files = files
        self.seients_per_fila = seients_per_fila
        self.sessions:list[Sessio] = []
        cine.sales.append(self)
    
    def busca_sessio(self, id_sessio: int) -> Sessio:
        ''' Busca una sessio pel seu id en la llista de sessions de la sala.
        Si la troba retorna la sala, sinó llança l'excepció 'sessio_no_trobada'
        '''
        for sessio in self.sessions:
            if sessio.id==id_sessio:
                return sessio
        raise sessio_no_trobada
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['id_'] = Sala.id
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        Sala.id = state['id_']

#==========================================================================================================
class Sessio:
    id:int = 1
    def __init__(self, sala:Sala, data_hora:dt.datetime, pel_licula:Pel_licula, preu_entrada:float) -> None:
        self.id = Sessio.id
        Sessio.id += 1
        self.data_hora:dt.datetime = data_hora
        self.pel_licula = pel_licula
        self.preu_entrada = preu_entrada
        self.reserves:list[list[Reserva|None]] = [[None] * sala.seients_per_fila for _ in range(sala.files)]
        sala.sessions.append(self)
    
    def mostra_reserves(self) -> None:
        '''Mostra per pantalla les reserves de la sessió per fila '''
        for i, fila in enumerate(self.reserves):
            print(f'fila {i}: {fila}')
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state['id_'] = Sessio.id
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        Sessio.id = state['id_']
           
#==========================================================================================================
# Persistència de dades.
#==========================================================================================================
def grava_arxiu() -> None:
    '''Grava en arxiu.pkl la llista de pel·licules i la de cines'''
    with open('arxiu.pkl', 'wb') as fd:
        pickle.dump(pel_licules, fd)
        pickle.dump(cines, fd)

def llig_arxiu() -> tuple[list[Pel_licula], list[Cine]]:
    ''' Si arxiu.pkl no existix el crea y grava en ell la llista de pel·licules i la de cines.
    Si arxiu.pkl existix el sobreescriu amb les llistes de pel·licules i de cines.
    '''
    if not os.path.exists('arxiu.pkl'):
        grava_arxiu()
    with open('arxiu.pkl', 'rb') as fd:
        pel_licules = pickle.load(fd)
        cines = pickle.load(fd)
        return  pel_licules, cines
def input_type(text:str, type:str='str', excepcio:bool=True, intro_cancellar:bool=True) -> int|str|float|None:
    '''Funció ampliació de l'input de Python. Demana a l'usuari un valor que convertix a un tipus de dada determinat
    segons el valor del paràmetre type, el qual pot ser 'int','str' o 'float'. Si l'usuari no introduix res (intro)
    segon el valor del paràmetre excepcio generarà l'excepció 'input_type_cancel·lat' o retonarà ''.
    Al fer l'input mostra de manera automàtica el text (Intro=cancel·lar). Este text es pot ocultar amb el parametre intro_cancellar=False.
    '''
    while True:
        try:
            txt_intro = '(Intro=cancel·lar) ' if intro_cancellar else ''
            cadena = input(f'{txt_intro}{text} ')
            if cadena=='':
                if excepcio:
                    raise input_type_cancel·lat
                return ''
            elif type=='int':
                return int(cadena)
            elif type=='str':
                return cadena
            elif type=='float':
                return float(cadena)
        except ValueError:
            print('Valor incorrecte')


#------------------------------------------------------------------------
def obtin_data() -> dt.date|None:
    ''' Pregunta a l'usuari una data. Verifica que es correcta i avisa si no ho és.
    Retorna una data o None si l'usuari no n'ha introduit cap (fa intro).
    '''
    try:
        data=input_type(" Introdueix una data en format ddmmaa:")
        int(data)
        if len(data) != 6:
            raise data_invalida
        year= int("20"+data[4]+data[5])
        month= int(data[2]+data[3])
        day= int(data[0]+data[1])
        return dt.date(year,month,day)
    except input_type_cancel·lat:
        return None
    
    except:
        print("Data no vàlida")
        return obtin_data()
#------------------------------------------------------------------------
def obtin_hora() ->   dt.time|None:
    ''' Pregunta a l'usuari una hora. Verifica que es correcta i avisa si no ho és.
    Retorna una hora o None si l'usuari no n'ha introduit cap (fa intro).
    '''
       
    try:
        hora=input_type("(Intro=cancel·lar) Introdueix una hora en format hhmm:")
        int(hora)
        if len(hora) != 4:
            raise hora_invalida
        hour=int(hora[:2])
        minute= int(hora[2:])
        return dt.time(hour,minute)
    
    except input_type_cancel·lat:
        return None
    
    except:
        print("Hora no vàlida")
        return obtin_hora()

#------------------------------------------------------------------------
def obtin_data_hora() -> dt.datetime:
    ''' Pregunta a l'usuari una data en forma ddmmaa i una hora en forma hhmm.
    Verifica que es la i l'hora són correctes i avisa si no ho és.
    Retorna el datetime corresponent. Si polsem intro llança l'excepció 'input_type_cancel·lat'
    '''
    data= obtin_data()
    hora= obtin_hora()
    if not ( data or hora):
        raise input_type_cancel·lat
    return dt.datetime.combine(data,hora)

def cls(txt:str|None=None):
    comando = 'cls' if platform.system()=='Windows' else 'clear'
    os.system(comando)
    if txt:
        print(txt)

#------------------------------------------------------------------------
def busca_pel_licula(id: int) -> Pel_licula:
    ''' Busca una pel·lícula pel seu id en la llista de pel·lícules.
    Si la troba retorna la pel·lícula, sinó llança l'excepció 'pelicula_no_trobada'
    '''
    for pelicula in pel_licules:
        if pelicula.id == id:
            return pelicula
    raise pelicula_no_trobada
#------------------------------------------------------------------------
def demana_pel_licula() -> Pel_licula:
    ''' Demana l'id d'una pel·lícula, la busca en la llista de pel·lícules i retorna la Pel·lícula.
    Si polsem intro llança l'excepció 'input_type_cancel·lat' 
    '''
    id=input_type("Introdueix id")
    try:
        pelicula= busca_pel_licula(int(id))
        return pelicula
    except pelicula_no_trobada:
        print("No s'ha trobat la pelicula")
        return demana_pel_licula()
