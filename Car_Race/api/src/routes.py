from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from src.database_connection import get_db
from src.models import Player, RaceParticipation
from src.game_logic import start_race, update_player_position, get_game_state, generar_pista

# Crear un enrutador de FastAPI
router = APIRouter()

# Modelos Pydantic

# Modelo para la solicitud de unirse a la carrera
class JoinRaceRequest(BaseModel):
    player_name: str
    vehicle: str

# Modelo para la respuesta de unirse a la carrera
class JoinRaceResponse(BaseModel):
    message: str
    player_id: str
    race_id: str

# Modelo para la respuesta de la pista
class TrackSectionResponse(BaseModel):
    section: List[List[str]]
    position: int

# Modelo para la solicitud de actualizar la posición del jugador
class UpdatePositionRequest(BaseModel):
    player_id: str
    race_id: str
    new_position: int

# Modelo para la respuesta del estado de la carrera
class RaceStateResponse(BaseModel):
    race_id: str
    players: List[dict]
    winner: Optional[str] = None

# Modelo para la respuesta de inicio de carrera
class StartRaceResponse(BaseModel):
    message: str
    race_id: str
    players: List[dict]

# Endpoints

# Endpoint para unirse a una carrera
@router.post("/join_race", response_model=JoinRaceResponse)
def join_race(request: JoinRaceRequest, db: Session = Depends(get_db)):
    """
    Permite a un jugador unirse a una carrera.
    """
    # Buscar o crear el jugador
    player = db.query(Player).filter_by(nombre_usuario=request.player_name).first()
    if not player:
        player = Player(nombre_usuario=request.player_name)
        db.add(player)
        db.commit()
        db.refresh(player)
    
    # Iniciar una nueva carrera si es necesario
    nueva_carrera = start_race(db)

    # Añadir participación del jugador en la carrera
    participacion = RaceParticipation(
        player_id=player.id,
        race_id=nueva_carrera.id,
        vehiculo_usado=request.vehicle,
        posicion_final=0  # Inicia en la posición 0
    )
    db.add(participacion)
    db.commit()

    return JoinRaceResponse(
        message="Te has unido a la carrera",
        player_id=player.id,
        race_id=nueva_carrera.id
    )

# Endpoint para obtener una sección de la pista para un jugador
@router.get("/race/{race_id}/track/{player_id}", response_model=TrackSectionResponse)
def get_track_section(race_id: str, player_id: str, db: Session = Depends(get_db)):
    """
    Devuelve la sección actual de la pista para el jugador.
    """
    participacion = db.query(RaceParticipation).filter_by(player_id=player_id, race_id=race_id).first()
    if not participacion:
        raise HTTPException(status_code=404, detail="Jugador no encontrado en la carrera")

    # Obtener la pista y la sección actual
    pista_json = db.query(RaceParticipation).filter_by(race_id=race_id).first().race.pista.estructura_pista
    seccion = pista_json["pista"][participacion.posicion_final : participacion.posicion_final + 5]

    return TrackSectionResponse(
        section=seccion,
        position=participacion.posicion_final
    )

# Endpoint para actualizar la posición de un jugador en la pista
@router.put("/race/{race_id}/player/{player_id}/position", response_model=TrackSectionResponse)
def update_position(request: UpdatePositionRequest, db: Session = Depends(get_db)):
    """
    Actualiza la posición del jugador en la pista y devuelve la nueva sección de pista.
    """
    try:
        nueva_seccion = update_player_position(db, request.player_id, request.race_id, request.new_position)
        return TrackSectionResponse(
            section=nueva_seccion,
            position=request.new_position
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para obtener el estado actual de la carrera
@router.get("/race/{race_id}/state", response_model=RaceStateResponse)
def get_race_state(race_id: str, db: Session = Depends(get_db)):
    """
    Devuelve el estado actual de la carrera, incluyendo posiciones de jugadores y si hay un ganador.
    """
    try:
        estado_carrera = get_game_state(db, race_id)
        return RaceStateResponse(
            race_id=estado_carrera["race_id"],
            players=estado_carrera["players"],
            winner=estado_carrera["winner"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para iniciar una nueva carrera
@router.post("/start_race", response_model=StartRaceResponse)
def start_new_race(db: Session = Depends(get_db)):
    """
    Inicia una nueva carrera y devuelve la información de los jugadores.
    """
    nueva_carrera = start_race(db)
    return StartRaceResponse(
        message="Carrera iniciada",
        race_id=nueva_carrera.id,
        players=[]
    )
