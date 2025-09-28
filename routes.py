#Definición de endpoints para el microservicio de catálogo de vehículos

from fastapi import APIRouter, HTTPException
from .models import Vehicle
from . import crud

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

#Ruta POST: Crear un nuevo vehículo
@router.post("/")
async def create_vehicle(vehicle: Vehicle):
    id = await crud.create_vehicle(vehicle)
    return {"id": id}

#Ruta GET: Obtener todos los vehículos
@router.get("/")
async def get_vehicles():
    return await crud.get_vehicles()

#Ruta GET: Obtener un vehículo por su ID
@router.get("/{id}")
async def get_vehicle(id: str):
    vehicle = await crud.get_vehicle(id)
    if vehicle:
        return vehicle
    elif not vehicle:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

#Ruta PUT: Actualizar un vehículo por su ID
@router.put("/{id}")
async def update_vehicle(id: str, vehicle: Vehicle):
    updated_vehicle = await crud.update_vehicle(id, vehicle.dict())
    if updated_vehicle:
        return updated_vehicle
    elif not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

#Ruta DELETE: Eliminar un vehículo por su ID
@router.delete("/{id}")
async def delete_vehicle(id: str):
    result = await crud.delete_vehicle(id)
    if result:
        return {"message": "Vehiculo eliminado"}
    elif not result:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")