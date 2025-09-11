<script setup lang="ts">
import { ref, onMounted } from 'vue';
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue';

defineOptions({
  name: 'DashboardHomeView'
});

// ... (toda la lógica del script se mantiene exactamente igual) ...
interface Metric {
  value: string | number;
  unit: string;
  changeText: string;
  isPositive: boolean;
}

const metrics = ref<{
  temperatura: Metric;
  nitrogeno: Metric;
  electroconductividad: Metric;
  ph: Metric;
} | null>(null);
const error = ref<string | null>(null);

onMounted(async () => {
  const token = localStorage.getItem('userToken');
  if (!token) {
    error.value = "Error de autenticación: No se encontró el token.";
    return;
  }
  try {
    const response = await fetch('http://127.0.0.1:8000/api/metrics/latest', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al obtener los datos de la API');
    }
    metrics.value = await response.json();
  } catch (e: unknown) {
    if (e instanceof Error) {
      error.value = e.message;
      console.error('Hubo un problema con la petición fetch:', e);
    } else {
      error.value = String(e);
      console.error('Hubo un problema con la petición fetch:', e);
    }
  }
});
</script>

<template>
  <div class="dashboard-content">
    <header class="view-header">
      <h1>Dashboard del Embalse</h1>
      <p>Vista general y análisis de los datos más recientes del sistema.</p>
    </header>

    <section class="dashboard-section">
      <h2 class="section-title">Última Medición Registrada</h2>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-else-if="!metrics">
        <p>Cargando métricas...</p>
      </div>
      <div v-else class="metrics-grid">
        <MetricCard
          title="Temperatura"
          :value="String(metrics.temperatura.value)"
          :unit="metrics.temperatura.unit"
          :changeText="metrics.temperatura.changeText"
          :isPositive="metrics.temperatura.isPositive"
        />
        <MetricCard
          title="Nitrógeno"
          :value="String(metrics.nitrogeno.value)"
          :unit="metrics.nitrogeno.unit"
          :changeText="metrics.nitrogeno.changeText"
          :isPositive="metrics.nitrogeno.isPositive"
        />
        <MetricCard
          title="Electroconductividad"
          :value="String(metrics.electroconductividad.value)"
          :unit="metrics.electroconductividad.unit"
          :changeText="metrics.electroconductividad.changeText"
          :isPositive="metrics.electroconductividad.isPositive"
        />
        <MetricCard
          title="Ph"
          :value="String(metrics.ph.value)"
          :unit="metrics.ph.unit"
          :changeText="metrics.ph.changeText"
          :isPositive="true"
        />
      </div>
    </section>

    <section class="dashboard-section">
      <h2 class="section-title">Análisis Histórico y Capacidad</h2>
      <div class="main-widgets-grid">
        <WaterLevelChart />
        <ReservoirCapacityChart />
      </div>
    </section>

    <section class="dashboard-section">
      <h2 class="section-title">Estado de Sensores</h2>
      <div class="table-widget">
        <SensorsTable />
      </div>
    </section>
  </div>
</template>

<style scoped>
.dashboard-content {
  padding: 1.5rem 2rem; /* Más padding a los lados, menos arriba/abajo */
}

/* Estilos para el nuevo encabezado de la vista */
.view-header {
  margin-bottom: 2rem;
}

.view-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.view-header p {
  font-size: 1.1rem;
  color: #6c757d;
  margin: 0;
}

/* Estilos para las nuevas secciones y sus títulos */
.dashboard-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #34495e;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

/* Estilos existentes (sin cambios) */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.main-widgets-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  align-items: stretch;
}

.table-widget {
  /* No necesita margen superior porque la sección ya lo tiene */
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 992px) {
  .main-widgets-grid {
    grid-template-columns: 1fr;
  }
}
</style>
