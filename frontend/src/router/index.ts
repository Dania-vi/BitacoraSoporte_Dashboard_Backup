
// Importamos las funciones necesarias de Vue Router.
import { createRouter, createWebHistory } from 'vue-router'

// Importamos la vista principal del dashboard.
import DashboardView from '../views/DashboardView.vue'

// Importamos la vista que mostrará el listado de servidores.
import ServidoresView from '../views/ServidoresView.vue'

// Definimos las rutas de navegación de nuestra aplicación.
const routes = [
  {
    // Página principal del sistema.
    path: '/',
    name: 'dashboard',
    component: DashboardView,
  },
  {
    // Página que mostrará los servidores registrados.
    path: '/servidores',
    name: 'servidores',
    component: ServidoresView,
  },
]

// Creamos la instancia del enrutador.
const router = createRouter({
  // Configuramos el historial de navegación del navegador.
  history: createWebHistory(import.meta.env.BASE_URL),

  // Registramos las rutas disponibles.
  routes,
})

// Exportamos el enrutador para utilizarlo en main.ts.
export default router
