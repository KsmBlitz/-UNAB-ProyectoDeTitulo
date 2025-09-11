<script setup lang="ts">
import { ref, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import type { ChartData, ChartOptions } from 'chart.js';

defineOptions({
  name: 'WaterLevelChart'
});

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

// 1. Definimos las props que este componente espera recibir desde DashboardHomeView
const props = defineProps({
  chartData: {
    type: Object as () => { labels: string[]; real_level: number[]; expected_level: number[] },
    required: true
  }
});

// 2. Creamos una variable reactiva local para los datos del gráfico
const chartDataRef = ref<ChartData<'line'>>({ labels: [], datasets: [] });

// 3. Creamos las opciones del gráfico, incluyendo el tooltip interactivo
const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' as const, align: 'end' as const },
    tooltip: {
      mode: 'index',
      intersect: false,
    }
  },
  scales: {
    y: { beginAtZero: false }
  }
};

// 4. Usamos un 'watch' para reaccionar cuando los datos de la prop cambien
watch(() => props.chartData, (newData) => {
  if (newData && newData.labels.length > 0) {
    chartDataRef.value = {
      labels: newData.labels,
      datasets: [
        {
          label: 'Nivel Real',
          borderColor: '#3498db',
          backgroundColor: 'rgba(52, 152, 219, 0.2)',
          data: newData.real_level,
          fill: true,
          tension: 0.4
        },
        {
          label: 'Nivel Esperado',
          borderColor: '#95a5a6',
          borderDash: [5, 5],
          data: newData.expected_level,
          fill: false,
          tension: 0.4
        }
      ]
    };
  }
}, { immediate: true, deep: true }); // 'immediate' para la carga inicial, 'deep' para objetos
</script>

<template>
  <div class="chart-container">
    <div class="chart-wrapper">
      <Line v-if="chartData.labels.length > 0" :data="chartDataRef" :options="chartOptions" />
      <p v-else>No hay datos para mostrar en el rango seleccionado.</p>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  background-color: #ffffff;
  border-radius: 8px;
  /* El padding y la sombra ahora los maneja la sección en HomeView */
  height: 450px;
  display: flex;
  flex-direction: column;
}
.chart-wrapper {
  position: relative;
  flex-grow: 1;
  min-height: 0;
}
p {
  text-align: center;
  color: #6c757d;
  margin-top: 2rem;
}
</style>
