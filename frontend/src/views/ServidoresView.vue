
<script setup lang="ts">
// Importamos las herramientas reactivas de Vue.
import { computed, onMounted, ref } from 'vue'

// Importamos la función que consulta nuestro backend.
import { obtenerDatos } from '../services/api'

// Definimos la estructura que tiene cada servidor.
interface Servidor {
  id: number
  nombre_host: string
  direccion_ip: string
  sistema_operativo: string
  estado_actual: string
  ultima_conexion: string | null
}

// Guardamos los servidores que recibimos del backend.
const servidores = ref<Servidor[]>([])

// Calculamos la cantidad total de servidores registrados.
const totalServidores = computed(() => servidores.value.length)

// Contamos los servidores cuyo estado actual es Activo.
const servidoresActivos = computed(() =>
  servidores.value.filter(
    (servidor) => servidor.estado_actual.toLowerCase() === 'activo',
  ).length,
)

// Contamos los servidores cuyo estado actual es Inactivo.
const servidoresInactivos = computed(() =>
  servidores.value.filter(
    (servidor) => servidor.estado_actual.toLowerCase() === 'inactivo',
  ).length,
)

// Indicamos si la información se está cargando.
const cargando = ref(true)

// Guardamos un posible mensaje de error.
const error = ref('')

// Consultamos los servidores registrados en el backend.
async function cargarServidores() {
  try {
    // Activamos el indicador de carga.
    cargando.value = true

    // Limpiamos cualquier error anterior.
    error.value = ''

    // Solicitamos la lista de servidores a la API.
    servidores.value = await obtenerDatos<Servidor[]>('/api/servidores/')
  } catch (err) {
    // Mostramos un mensaje si ocurre algún problema.
    error.value = 'No fue posible cargar los servidores. Verifica que el backend esté funcionando.'
    console.error('Error al cargar servidores:', err)
  } finally {
    // Desactivamos el indicador de carga.
    cargando.value = false
  }
}

// Formateamos la fecha de la última conexión.
function formatearFecha(fecha: string | null): string {
  // Si no existe una fecha, mostramos un mensaje.
  if (!fecha) return 'Sin registro'

  // Convertimos la fecha a un formato legible.
  return new Date(fecha).toLocaleString('es-MX')
}

// Consultamos los servidores cuando se abre esta pantalla.
onMounted(() => {
  cargarServidores()
})
</script>

<template>
  <section class="servidores-view">

    <!-- Encabezado de la pantalla. -->
    <div class="page-header">
      <div>
        <h1>Servidores</h1>
        <p>Consulta los equipos registrados en el sistema.</p>
      </div>

      <!-- Botón para volver a consultar los servidores. -->
      <button class="refresh-button" @click="cargarServidores">
        Actualizar
      </button>
    </div>

    <!-- Mensaje mientras se consultan los datos. -->
    <div v-if="cargando" class="message">
      Cargando servidores...
    </div>

    <!-- Mensaje cuando ocurre un error. -->
    <div v-else-if="error" class="message error">
      {{ error }}
    </div>

    <!-- Contenido cuando la consulta termina correctamente. -->
    <template v-else>

      <!-- Indicadores generales de los servidores. -->
      <div class="summary-grid">

        <!-- Total de servidores registrados. -->
        <div class="summary-card">
          <span class="summary-label">Total de servidores</span>
          <strong>{{ totalServidores }}</strong>
        </div>

        <!-- Servidores que aparecen como activos. -->
        <div class="summary-card">
          <span class="summary-label">Servidores activos</span>
          <strong class="active-number">{{ servidoresActivos }}</strong>
        </div>

        <!-- Servidores que aparecen como inactivos. -->
        <div class="summary-card">
          <span class="summary-label">Servidores inactivos</span>
          <strong class="inactive-number">{{ servidoresInactivos }}</strong>
        </div>

      </div>

      <!-- Mensaje cuando todavía no hay servidores registrados. -->
      <div v-if="servidores.length === 0" class="message">
        No hay servidores registrados.
      </div>

      <!-- Tabla con los servidores recibidos del backend. -->
      <div v-else class="table-container">
        <table>
          <thead>
            <tr>
              <th>Nombre del servidor</th>
              <th>Dirección IP</th>
              <th>Sistema operativo</th>
              <th>Estado</th>
              <th>Última conexión</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="servidor in servidores" :key="servidor.id">
              <td>{{ servidor.nombre_host }}</td>
              <td>{{ servidor.direccion_ip }}</td>
              <td>{{ servidor.sistema_operativo }}</td>
              <td>
                <span
                  class="status"
                  :class="servidor.estado_actual.toLowerCase()"
                >
                  {{ servidor.estado_actual }}
                </span>
              </td>
              <td>{{ formatearFecha(servidor.ultima_conexion) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Aviso para identificar el origen de los registros actuales. -->
      <p class="data-notice">
        Los registros mostrados corresponden a datos de prueba del proyecto.
      </p>

    </template>
  </section>
</template>

<style scoped>
/* Contenedor principal de la pantalla. */
.servidores-view {
  padding: 25px;
}

/* Encabezado y botón de actualización. */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.page-header h1 {
  margin: 0 0 8px;
  color: #1e293b;
  font-size: 25px;
}

.page-header p {
  margin: 0;
  color: #64748b;
}

/* Botón para actualizar la información. */
.refresh-button {
  padding: 10px 18px;
  border: none;
  border-radius: 7px;
  background-color: #2563eb;
  color: white;
  cursor: pointer;
}

.refresh-button:hover {
  background-color: #1d4ed8;
}

/* Mensajes de carga, error o ausencia de registros. */
.message {
  padding: 25px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  text-align: center;
}

.error {
  color: #b91c1c;
}

/* Distribución de las tarjetas de resumen. */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 25px;
}

/* Diseño individual de cada tarjeta. */
.summary-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

/* Texto descriptivo de cada indicador. */
.summary-label {
  color: #64748b;
  font-size: 14px;
}

/* Número principal de cada tarjeta. */
.summary-card strong {
  color: #1e293b;
  font-size: 28px;
}

/* Color para servidores activos. */
.summary-card .active-number {
  color: #16a34a;
}

/* Color para servidores inactivos. */
.summary-card .inactive-number {
  color: #dc2626;
}

/* Contenedor que permite desplazar la tabla en pantallas pequeñas. */
.table-container {
  overflow-x: auto;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
}

/* Estilos generales de la tabla. */
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th,
td {
  padding: 15px;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}

th {
  background-color: #f8fafc;
  color: #475569;
  font-size: 13px;
}

td {
  color: #334155;
  font-size: 14px;
}

/* Etiquetas que identifican el estado del servidor. */
.status {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  background-color: #e2e8f0;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
}

/* Apariencia para servidores activos. */
.status.activo {
  background-color: #dcfce7;
  color: #166534;
}

/* Apariencia para servidores inactivos. */
.status.inactivo {
  background-color: #fee2e2;
  color: #991b1b;
}

/* Aviso sobre los datos mostrados. */
.data-notice {
  margin-top: 18px;
  color: #64748b;
  font-size: 12px;
}

/* Adaptación de las tarjetas para pantallas pequeñas. */
@media (max-width: 700px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
