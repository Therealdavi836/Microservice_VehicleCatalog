from locust import HttpUser, task, between
import random
import string

def random_vehicle():
    """Genera datos aleatorios para un vehículo de prueba"""
    return {
        "brand": random.choice(["Toyota", "Mazda", "Chevrolet", "Ford", "Nissan"]),
        "model": f"{random.choice(['A', 'B', 'C'])}{random.randint(100, 999)}",
        "year": random.randint(2010, 2025),
        "price": random.randint(30000, 150000),
        "color": random.choice(["rojo", "azul", "negro", "blanco", "gris"])
    }

class CatalogoLoadTest(HttpUser):
    """
    Prueba de CARGA para el microservicio de Catálogo de Vehículos.
    Simula uso típico por parte de usuarios y administradores.
    """
    wait_time = between(1, 3)
    
    def on_start(self):
        self.vehicle_ids = []

    # -------------------- MÉTODOS DE PRUEBA --------------------

    @task(3)
    def obtener_vehiculos(self):
        """GET / — Consultar todos los vehículos"""
        response = self.client.get("/")
        if response.status_code == 200:
            data = response.json()
            if data:
                self.vehicle_ids = [v.get("id") for v in data if v.get("id")]

    @task(2)
    def crear_vehiculo(self):
        """POST / — Crear un nuevo vehículo"""
        vehicle = random_vehicle()
        response = self.client.post("/", json=vehicle)
        if response.status_code == 200:
            vid = response.json().get("id")
            if vid:
                self.vehicle_ids.append(vid)

    @task(2)
    def obtener_vehiculo_por_id(self):
        """GET /{id} — Obtener un vehículo por ID"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            self.client.get(f"/{vid}")

    @task(1)
    def actualizar_vehiculo(self):
        """PUT /{id} — Actualizar un vehículo existente"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            update_data = {"price": random.randint(35000, 170000)}
            self.client.put(f"/{vid}", json=update_data)

    @task(1)
    def eliminar_vehiculo(self):
        """DELETE /{id} — Eliminar un vehículo"""
        if self.vehicle_ids:
            vid = random.choice(self.vehicle_ids)
            self.client.delete(f"/{vid}")

    # ------------------------------------------------------------