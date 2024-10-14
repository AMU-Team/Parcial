import random
from sqlalchemy.orm import Session
from src.models import Player, Race, Track, RaceParticipation

# Función para iniciar una nueva carrera
def start_race(db: Session):
    # Generar una nueva carrera, generar la pista y asignar a los jugadores
    nueva_carrera = Race(
        num_jugadores=0,  # Se irán añadiendo
        num_vueltas=random.randint(3, 5),  # Generar un número aleatorio de vueltas
        longitud_pista=random.randint(500, 1000)  # Longitud aleatoria de la pista
    )
    db.add(nueva_carrera)
    db.commit()
    db.refresh(nueva_carrera)

    # Generar la pista (esto es solo un ejemplo de generación)
    pista_json = generar_pista(nueva_carrera.longitud_pista)
    pista = Track(race_id=nueva_carrera.id, estructura_pista=pista_json)
    db.add(pista)
    db.commit()

    return nueva_carrera

# Función para generar una pista aleatoria
def generar_pista(longitud_pista):
    pista = []
    for i in range(longitud_pista):
        fila = [" " for _ in range(5)]  # 5 carriles en la pista
        if random.random() < 0.2:  # Probabilidad del 20% de generar un obstáculo
            obstaculo = random.choice(["O", "A"])  # "O" para otros autos, "A" para barreras
            fila[random.randint(0, 4)] = obstaculo
        pista.append(fila)
    return {"pista": pista}

# Función para actualizar la posición de un jugador
def update_player_position(db: Session, player_id: str, race_id: str, new_position: int):
    # Obtener la participación del jugador en la carrera
    participacion = db.query(RaceParticipation).filter_by(player_id=player_id, race_id=race_id).first()
    
    if not participacion:
        raise Exception("El jugador no está en esta carrera")

    # Actualizar la posición del jugador
    participacion.posicion_final = new_position
    db.commit()

    # Devolver la nueva sección de la pista que el jugador verá
    pista = db.query(Track).filter_by(race_id=race_id).first().estructura_pista
    return pista["pista"][new_position : new_position + 5]  # Enviar las próximas 5 secciones de la pista

# Función para obtener el estado actual de la carrera
def get_game_state(db: Session, race_id: str):
    # Obtener la carrera
    carrera = db.query(Race).filter_by(id=race_id).first()
    if not carrera:
        raise Exception("La carrera no existe")

    # Obtener la participación de los jugadores
    participaciones = db.query(RaceParticipation).filter_by(race_id=race_id).all()

    # Formatear el estado del juego
    jugadores = [{"player_id": p.player_id, "posicion": p.posicion_final} for p in participaciones]
    
    # Comprobar si hay un ganador
    ganador = None
    for p in participaciones:
        if p.posicion_final >= carrera.longitud_pista * carrera.num_vueltas:
            ganador = p.player_id
            break

    return {
        "race_id": carrera.id,
        "players": jugadores,
        "winner": ganador
    }
