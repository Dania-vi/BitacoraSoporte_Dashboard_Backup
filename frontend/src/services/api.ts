
// Dirección base donde se encuentra nuestro backend desarrollado con FastAPI.
const API_URL = 'http://127.0.0.1:8000'

// Función para realizar peticiones GET al backend.
// Se utiliza para consultar información del sistema.
export async function obtenerDatos<T>(endpoint: string): Promise<T> {

  // Realizamos la petición GET al endpoint indicado.
  const respuesta = await fetch(`${API_URL}${endpoint}`)

  // Comprobamos si el servidor respondió correctamente.
  if (!respuesta.ok) {
    throw new Error(`Error al consultar el servidor: ${respuesta.status}`)
  }

  // Convertimos la respuesta del servidor a formato JSON.
  return await respuesta.json() as T
}

// Función para enviar información al backend mediante POST.
// Se utiliza para registrar nuevos mantenimientos.
export async function enviarDatos<T, R>(
  endpoint: string,
  datos: T
): Promise<R> {

  // Realizamos la petición POST enviando los datos en formato JSON.
  const respuesta = await fetch(`${API_URL}${endpoint}`, {
    method: 'POST',

    // Indicamos que el contenido enviado será JSON.
    headers: {
      'Content-Type': 'application/json',
    },

    // Convertimos el objeto recibido a una cadena JSON.
    body: JSON.stringify(datos),
  })

  // Comprobamos si ocurrió algún error durante el envío.
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => null)

    throw new Error(
      error?.detail || `Error al enviar información: ${respuesta.status}`
    )
  }

  // Devolvemos los datos que respondió el backend.
  return await respuesta.json() as R
}

// Función para actualizar información mediante PUT.
// Se utilizará para modificar mantenimientos existentes.
export async function actualizarDatos<T, R>(
  endpoint: string,
  datos: T
): Promise<R> {

  // Realizamos la petición PUT enviando los nuevos datos.
  const respuesta = await fetch(`${API_URL}${endpoint}`, {
    method: 'PUT',

    // Indicamos que el contenido enviado será JSON.
    headers: {
      'Content-Type': 'application/json',
    },

    // Convertimos los datos a formato JSON.
    body: JSON.stringify(datos),
  })

  // Comprobamos si el backend respondió correctamente.
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => null)

    throw new Error(
      error?.detail || `Error al actualizar información: ${respuesta.status}`
    )
  }

  // Devolvemos el registro actualizado.
  return await respuesta.json() as R
}

// Función para eliminar información mediante DELETE.
// Se utilizará para eliminar registros de mantenimiento.
export async function eliminarDatos<R>(endpoint: string): Promise<R> {
  // Realizamos la petición DELETE al endpoint indicado.
  const respuesta = await fetch(`${API_URL}${endpoint}`, {
    method: 'DELETE',
  })

  // Comprobamos si el backend respondió correctamente.
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => null)
    throw new Error(
      error?.detail || `Error al eliminar información: ${respuesta.status}`
    )
  }

  // Devolvemos la respuesta del backend.
  return await respuesta.json() as R
}