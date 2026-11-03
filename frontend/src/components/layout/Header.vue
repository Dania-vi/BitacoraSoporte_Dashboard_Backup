
<script setup lang="ts">
// Importamos computed para calcular el título según la ruta actual.
import { computed } from 'vue'

// Importamos useRoute para conocer en qué sección estamos.
import { useRoute } from 'vue-router'

// Obtenemos la ruta actual de la aplicación.
const route = useRoute()

// Relacionamos cada ruta con el título que aparecerá en el encabezado.
const pageTitles: Record<string, string> = {
  '/': 'Dashboard',
  '/servidores': 'Servidores',
  '/alertas': 'Alertas',
  '/historial': 'Historial',
  '/mantenimientos': 'Mantenimientos',
  '/respaldos': 'Respaldos',
}

// Calculamos el título automáticamente cuando cambia la ruta.
const pageTitle = computed(() => {
  return pageTitles[route.path] || 'Bitácora de Soporte'
})
</script>

<template>
  <!-- Encabezado principal -->
  <header class="header">

    <!-- Título de la sección actual -->
    <div class="header-title">
      <h1>{{ pageTitle }}</h1>
      <p>Bitácora de soporte técnico y monitoreo</p>
    </div>

    <!-- Indicador del estado general -->
    <div class="header-status">
      <span class="status-dot"></span>
      <span>Panel de monitoreo</span>
    </div>

  </header>
</template>

<style scoped>
/* Distribución general del encabezado */
.header {
  width: 100%;
  min-height: 85px;
  padding: 18px 30px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

/* Título de la sección */
.header-title h1 {
  margin: 0 0 5px;
  color: #172033;
  font-size: 22px;
  font-weight: 700;
}

.header-title p {
  margin: 0;
  color: #64748b;
  font-size: 12px;
}

/* Indicador del panel */
.header-status {
  display: flex;
  align-items: center;
  gap: 9px;
  color: #64748b;
  font-size: 12px;
}

/* Punto indicador */
.status-dot {
  width: 9px;
  height: 9px;
  background-color: #22c55e;
  border-radius: 50%;
}
</style>
