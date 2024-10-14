from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid
import datetime

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

# Clase para representar los jugadores
class Player(Base):
    __tablename__ = 'players'

    id = Column(String, primary_key=True, default=generate_uuid)
    nombre_usuario = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    puntaje_total = Column(Integer, default=0)
    carreras_jugadas = Column(Integer, default=0)
    victorias = Column(Integer, default=0)

    participaciones = relationship("RaceParticipation", back_populates="player")

# Clase para representar las carreras
class Race(Base):
    __tablename__ = 'races'

    id = Column(String, primary_key=True, default=generate_uuid)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    num_jugadores = Column(Integer, nullable=False)
    num_vueltas = Column(Integer, nullable=False)
    longitud_pista = Column(Integer, nullable=False)  # Longitud de cada vuelta
    ganador_id = Column(String, ForeignKey('players.id'))
    duracion_carrera = Column(Float)  # Duración en segundos

    ganador = relationship("Player", foreign_keys=[ganador_id])
    participaciones = relationship("RaceParticipation", back_populates="race")
    pista = relationship("Track", uselist=False, back_populates="race")

# Clase para representar las pistas generadas (JSON con la estructura)
class Track(Base):
    __tablename__ = 'tracks'

    id = Column(String, primary_key=True, default=generate_uuid)
    race_id = Column(String, ForeignKey('races.id'))
    estructura_pista = Column(JSON, nullable=False)  # Almacena la pista completa con obstáculos

    race = relationship("Race", back_populates="pista")

# Clase para representar la participación de los jugadores en las carreras
class RaceParticipation(Base):
    __tablename__ = 'race_participation'

    id = Column(String, primary_key=True, default=generate_uuid)
    race_id = Column(String, ForeignKey('races.id'))
    player_id = Column(String, ForeignKey('players.id'))
    vehiculo_usado = Column(String, nullable=False)
    puntaje = Column(Integer, default=0)
    posicion_final = Column(Integer)
    tiempo_total = Column(Float)  # Tiempo total que tomó completar la carrera

    player = relationship("Player", back_populates="participaciones")
    race = relationship("Race", back_populates="participaciones")

# Clase para representar los vehículos (opcional)
class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(String, primary_key=True, default=generate_uuid)
    nombre_vehiculo = Column(String, nullable=False)
    velocidad_maxima = Column(Float, nullable=False)
    aceleracion = Column(Float, nullable=False)
    manejo = Column(Float, nullable=False)
    jugador_id = Column(String, ForeignKey('players.id'))