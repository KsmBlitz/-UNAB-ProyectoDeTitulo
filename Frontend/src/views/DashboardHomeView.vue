<script setup lang="ts">
import { ref, onMounted } from 'vue'; // <-- 1. Importar ref y onMounted
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue';

defineOptions({
  name: 'DashboardHomeView'
});

// 2. Definimos la "forma" de nuestros datos con TypeScript
interface Metric {
  value: string | number;
  unit: string;
  changeText: string;
  isPositive: boolean;
}

// 3. Creamos una variable reactiva para guardar los datos que vienen de la API
//    Le damos un estado inicial de "Cargando..."
const metrics = ref<{
  temperatura: Metric;
  oxigeno_disuelto: Metric;
  salinidad: Metric;
  ph: Metric;
} | null>(null);

// 4. onMounted es un "hook" de Vue que se ejecuta justo cuando el componente se ha montado en la página
onMounted(async () => {
  try {
    // 5. Usamos 'fetch' para hacer una petición GET a nuestro backend FastAPI
    const response = await fetch('http://127.0.0.1:8000/api/metrics/latest');

    if (!response.ok) {
      throw new Error('Error al obtener los datos de la API');
    }

    // 6. Convertimos la respuesta a JSON y la guardamos en nuestra variable reactiva
    metrics.value = await response.json();
    console.log('Datos de métricas recibidos desde FastAPI:', metrics.value);

  } catch (error) {
    console.error('Hubo un problema con la petición fetch:', error);
    // Aquí podríamos establecer un estado de error para mostrarlo en la UI
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
        title="Oxígeno Disuelto"
        :value="String(metrics.oxigeno_disuelto.value)"
        :unit="metrics.oxigeno_disuelto.unit"
        :changeText="metrics.oxigeno_disuelto.changeText"
        :isPositive="metrics.oxigeno_disuelto.isPositive"
      />
      <MetricCard
        title="Salinidad"
        :value="String(metrics.salinidad.value)"
        :unit="metrics.salinidad.unit"
        :changeText="metrics.salinidad.changeText"
        :isPositive="metrics.salinidad.isPositive"
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
.dashboard-content {
  padding: 2rem;
}
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
.main-widgets-grid {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
  align-items: stretch;
}
.table-widget {
  margin-top: 2rem;
}
@media (max-width: 992px) {
  .main-widgets-grid {
    grid-template-columns: 1fr;
  }
}
</style>
