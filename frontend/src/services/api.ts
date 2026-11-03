// Dirección base donde se encuentra nuestro backend desarrollado con FastAPI.
const API_URL = 'http://127.0.0.1:8000'

// Función para realizar peticiones GET al backend.
export async function obtenerDatos<T>(endpoint: string): Promise<T> {
  // Realizamos la petición al endpoint indicado.
  const respuesta = await fetch(`${API_URL}${endpoint}`)

  // Comprobamos si el servidor respondió correctamente.
  if (!respuesta.ok) {
    throw new Error(`Error al consultar el servidor: ${respuesta.status}`)
  }

  // Convertimos la respuesta del servidor a formato JSON.
  return await respuesta.json() as T
}