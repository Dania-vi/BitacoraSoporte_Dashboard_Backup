
# Importamos las herramientas necesarias de FastAPI.
from fastapi import APIRouter, Depends, HTTPException

# Importamos la sesión de SQLAlchemy y el error de integridad.
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importamos la dependencia para obtener la conexión a la base de datos.
from app.database.dependencies import get_db

# Importamos el modelo de mantenimiento.
from app.models.mantenimiento import Mantenimiento

# Importamos los esquemas para registrar y actualizar mantenimientos.
from app.schemas.mantenimiento import MantenimientoCreate, MantenimientoUpdate


# Define las rutas relacionadas con los mantenimientos.
router = APIRouter(
    prefix="/api/mantenimientos",
    tags=["Mantenimientos"]
)


# CONSULTAR TODOS LOS MANTENIMIENTOS.
@router.get("/")
def obtener_mantenimientos(db: Session = Depends(get_db)):

    # Consultamos todos los registros de la tabla de mantenimientos.
    mantenimientos = db.query(Mantenimiento).all()

    # Convertimos los registros en datos que FastAPI puede devolver como JSON.
    return [
        {
            "id": mantenimiento.id,
            "equipo_id": mantenimiento.equipo_id,
            "tecnico_id": mantenimiento.tecnico_id,
            "fecha_mantenimiento": mantenimiento.fecha_mantenimiento,
            "tipo_mantenimiento": mantenimiento.tipo_mantenimiento,
            "problema_detectado": mantenimiento.problema_detectado,
            "solucion_aplicada": mantenimiento.solucion_aplicada,
            "tiempo_empleado_min": mantenimiento.tiempo_empleado_min,
            "observaciones": mantenimiento.observaciones,
        }
        for mantenimiento in mantenimientos
    ]


# REGISTRAR UN NUEVO MANTENIMIENTO.
@router.post("/")
def crear_mantenimiento(
    datos: MantenimientoCreate,
    db: Session = Depends(get_db)
):

    # Construimos el registro con los datos recibidos.
    nuevo_mantenimiento = Mantenimiento(
        equipo_id=datos.equipo_id,
        tecnico_id=datos.tecnico_id,
        tipo_mantenimiento=datos.tipo_mantenimiento,
        problema_detectado=datos.problema_detectado,
        solucion_aplicada=datos.solucion_aplicada,
        tiempo_empleado_min=datos.tiempo_empleado_min,
        observaciones=datos.observaciones,
    )

    # Agregamos el registro a la sesión de SQLAlchemy.
    db.add(nuevo_mantenimiento)

    try:
        # Intentamos guardar el mantenimiento en PostgreSQL.
        db.commit()

        # Recuperamos el ID y la fecha generados por la base de datos.
        db.refresh(nuevo_mantenimiento)

    except IntegrityError:
        # Revertimos la transacción si ocurre un problema de integridad.
        db.rollback()

        # Devolvemos un error controlado.
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo registrar el mantenimiento. "
                "Verifica que el equipo y el técnico existan "
                "y que los datos sean válidos."
            ),
        )

    # Devolvemos los datos del mantenimiento registrado.
    return {
        "id": nuevo_mantenimiento.id,
        "equipo_id": nuevo_mantenimiento.equipo_id,
        "tecnico_id": nuevo_mantenimiento.tecnico_id,
        "fecha_mantenimiento": nuevo_mantenimiento.fecha_mantenimiento,
        "tipo_mantenimiento": nuevo_mantenimiento.tipo_mantenimiento,
        "problema_detectado": nuevo_mantenimiento.problema_detectado,
        "solucion_aplicada": nuevo_mantenimiento.solucion_aplicada,
        "tiempo_empleado_min": nuevo_mantenimiento.tiempo_empleado_min,
        "observaciones": nuevo_mantenimiento.observaciones,
    }


# ACTUALIZAR UN MANTENIMIENTO EXISTENTE.
@router.put("/{mantenimiento_id}")
def actualizar_mantenimiento(
    mantenimiento_id: int,
    datos: MantenimientoUpdate,
    db: Session = Depends(get_db)
):

    # Buscamos el mantenimiento mediante su identificador.
    mantenimiento = db.query(Mantenimiento).filter(
        Mantenimiento.id == mantenimiento_id
    ).first()

    # Comprobamos si el mantenimiento existe.
    if mantenimiento is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el mantenimiento solicitado."
        )

    # Obtenemos los datos enviados por el frontend.
    datos_actualizados = datos.model_dump()

    # Actualizamos los campos del registro existente.
    for campo, valor in datos_actualizados.items():
        setattr(mantenimiento, campo, valor)

    try:
        # Guardamos los cambios en PostgreSQL.
        db.commit()

        # Recuperamos el registro actualizado.
        db.refresh(mantenimiento)

    except IntegrityError:
        # Revertimos los cambios si ocurre un problema de integridad.
        db.rollback()

        # Devolvemos un error controlado.
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo actualizar el mantenimiento. "
                "Verifica que el equipo y el técnico existan."
            )
        )

    # Devolvemos el registro actualizado.
    return {
        "id": mantenimiento.id,
        "equipo_id": mantenimiento.equipo_id,
        "tecnico_id": mantenimiento.tecnico_id,
        "fecha_mantenimiento": mantenimiento.fecha_mantenimiento,
        "tipo_mantenimiento": mantenimiento.tipo_mantenimiento,
        "problema_detectado": mantenimiento.problema_detectado,
        "solucion_aplicada": mantenimiento.solucion_aplicada,
        "tiempo_empleado_min": mantenimiento.tiempo_empleado_min,
        "observaciones": mantenimiento.observaciones,
    }


# ELIMINAR UN MANTENIMIENTO EXISTENTE.
@router.delete("/{mantenimiento_id}")
def eliminar_mantenimiento(
    mantenimiento_id: int,
    db: Session = Depends(get_db)
):

    # Buscamos el mantenimiento mediante su identificador.
    mantenimiento = db.query(Mantenimiento).filter(
        Mantenimiento.id == mantenimiento_id
    ).first()

    # Comprobamos si el mantenimiento existe.
    if mantenimiento is None:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el mantenimiento que deseas eliminar."
        )

    try:
        # Marcamos el registro para eliminarlo de la base de datos.
        db.delete(mantenimiento)

        # Confirmamos la eliminación en PostgreSQL.
        db.commit()

    except IntegrityError:
        # Revertimos la operación si existen restricciones que impiden eliminarlo.
        db.rollback()

        # Devolvemos un mensaje de error controlado.
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar el mantenimiento porque "
                "existen restricciones relacionadas con este registro."
            )
        )

    # Devolvemos la confirmación de eliminación.
    return {
        "mensaje": "El mantenimiento se eliminó correctamente.",
        "id": mantenimiento_id
    }
