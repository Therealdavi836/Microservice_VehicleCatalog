from locust import HttpUser, task, constant
import random

def random_vehicle():
    return {
        "brand": random.choice(["Toyota", "Mazda", "Chevrolet", "Ford", "Nissan"]),
        "model": f"{random.choice(['S', 'R', 'T'])}{random.randint(100, 999)}",
        "year": random.randint(2010, 2025),
        "price": random.randint(30000, 200000),
        "color": random.choice(["rojo", "azul", "negro", "blanco", "gris"])
    }

class CatalogoCapacityTest(HttpUser):
    """
    Prueba de CAPACIDAD para el microservicio de Catálogo de Vehículos.
    Mide hasta qué punto puede procesar solicitudes antes de degradarse.
    """
    wait_time = constant(0.5)  # tráfico continuo
    
    def on_start(self):
        self.vehicle_ids = []

    # -------------------- MÉTODOS DE PRUEBA --------------------

    @task(3)
    def obtener_vehiculos(self):
        """GET / — Obtener todos los vehículos"""
        response = self.client.get("/")
        if response.status_code == 200:
            data = response.json()
            if data:
                self.vehicle_ids = [v.get("id") for v in data if v.get("id")]

    @task(2)
    def crear_vehiculo(self):
        """POST / — Crear un vehículo"""
        vehicle = random_vehicle()
        response = self.client.post("/", json=vehicle)
        if response.status_code == 200:
            vid = response.json().get("id")
            if vid:
                self.vehicle_ids.append(vid)

    @task(2)
    def obtener_vehiculo_por_id(self):
        """GET /{id} — Consultar vehículo específico"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            self.client.get(f"/{vid}")

    @task(2)
    def actualizar_vehiculo(self):
        """PUT /{id} — Actualizar vehículo"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            data = {"price": random.randint(35000, 170000)}
            self.client.put(f"/{vid}", json=data)

    @task(1)
    def eliminar_vehiculo(self):
        """DELETE /{id} — Eliminar vehículo"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            self.client.delete(f"/{vid}")