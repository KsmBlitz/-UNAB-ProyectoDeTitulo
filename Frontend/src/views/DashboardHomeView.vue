<script setup lang="ts">
import { ref, onMounted } from 'vue';
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue';

defineOptions({
  name: 'DashboardHomeView'
});

// Definimos la "forma" de nuestros datos
interface Metric {
  value: string | number;
  unit: string;
  changeText: string;
  isPositive: boolean;
}

// Creamos la variable reactiva para guardar los datos de la API
const metrics = ref<{
  temperatura: Metric;
  nitrogeno: Metric;
  electroconductividad: Metric;
  ph: Metric;
} | null>(null);
const error = ref<string | null>(null); // Variable para mostrar errores

onMounted(async () => {
  // Obtenemos el token guardado en el login
  const token = localStorage.getItem('userToken');

  if (!token) {
    error.value = "Error de autenticación: No se encontró el token.";
    return;
  }

  try {
    // --- CAMBIO CLAVE AQUÍ ---
    // Añadimos el objeto 'headers' a nuestra petición fetch
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

    <div class="main-widgets-grid">
      <WaterLevelChart />
      <ReservoirCapacityChart />
    </div>

    <div class="table-widget">
      <SensorsTable />
    </div>
  </div>
</template>

<style scoped>
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  text-align: center;
}
.dashboard-content{padding:2rem}.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem}.main-widgets-grid{margin-top:2rem;display:grid;grid-template-columns:2fr 1fr;gap:1.5rem;align-items:stretch}.table-widget{margin-top:2rem}@media (max-width:992px){.main-widgets-grid{grid-template-columns:1fr}}
</style>
