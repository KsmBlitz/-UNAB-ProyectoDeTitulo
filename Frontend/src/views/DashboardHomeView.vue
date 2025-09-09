<script setup lang="ts">
import { ref, onMounted } from 'vue';
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue';

defineOptions({
  name: 'DashboardHomeView'
});

// Definimos la nueva "forma" de nuestros datos
interface Metric {
  value: string | number;
  unit: string;
  changeText: string;
  isPositive: boolean;
}

// Actualizamos la variable reactiva para que coincida con la nueva estructura de la API
const metrics = ref<{
  temperatura: Metric;
  nitrogeno: Metric; // <-- CAMBIO AQUÍ
  electroconductividad: Metric; // <-- CAMBIO AQUÍ
  ph: Metric;
} | null>(null);

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/metrics/latest');
    if (!response.ok) throw new Error('Error al obtener los datos de la API');
    metrics.value = await response.json();
  } catch (error) {
    console.error('Hubo un problema con la petición fetch:', error);
  }
});
</script>

<template>
  <div class="dashboard-content">
    <div v-if="metrics" class="metrics-grid">
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
    <div v-else>
      <p>Cargando métricas...</p>
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
/* Los estilos se mantienen igual que antes */
.dashboard-content{padding:2rem}.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem}.main-widgets-grid{margin-top:2rem;display:grid;grid-template-columns:2fr 1fr;gap:1.5rem;align-items:stretch}.table-widget{margin-top:2rem}@media (max-width:992px){.main-widgets-grid{grid-template-columns:1fr}}
</style>
