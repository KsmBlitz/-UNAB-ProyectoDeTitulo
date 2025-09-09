<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

defineOptions({
  name: 'WaterLevelChart'
});

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const chartData = {
  labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
  datasets: [
    {
      label: 'Nivel Real',
      borderColor: '#3498db',
      backgroundColor: 'rgba(52, 152, 219, 0.2)',
      data: [65, 75, 90, 80, 70],
      fill: true,
      tension: 0.4
    },
    {
      label: 'Nivel Esperado',
      borderColor: '#95a5a6',
      borderDash: [5, 5],
      data: [70, 72, 80, 82, 75],
      fill: false,
      tension: 0.4
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      align: 'end' as const,
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
};
</script>

<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>Nivel de Agua</h3>
      <i class="pi pi-cog settings-icon"></i>
    </div>
    <div class="chart-wrapper">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
<style scoped>
.chart-container {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  /* Añadido: Asegura que el contenedor principal no se estire indefinidamente */
  min-width: 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.settings-icon {
  cursor: pointer;
  color: #6c757d;
}

.chart-wrapper {
  height: 350px;
  overflow: hidden;
}

.chart-canvas-container {
  position: relative;
  height: 100%;
  width: 100%;
}
</style>
