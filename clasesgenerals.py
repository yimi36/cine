from __future__ import annotations
import datetime as dt



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
        Pel_licula.id = state['id_']

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