<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { Chart } from 'chart.js' // Importamos el tipo ChartJS para mayor precisión

defineOptions({
  name: 'ReservoirCapacityChart'
});

ChartJS.register(ArcElement, Tooltip, Legend);

const capacityPercentage = 84;

const chartData = {
  datasets: [
    {
      data: [capacityPercentage, 100 - capacityPercentage],
      backgroundColor: ['#3498db', '#e9ecef'],
      borderColor: 'transparent',
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false, // Lo dejamos en false para que llene el espacio
  cutout: '80%',
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      enabled: false,
    }
  }
};

// Plugin actualizado para dibujar el texto
const centerTextPlugin = {
  id: 'centerText',
  afterDraw: (chart: Chart) => { // Usamos el tipo importado
    // Verificamos que el área del gráfico exista para evitar errores
    if (chart.chartArea) {
      const ctx = chart.ctx;

      // --- LA SOLUCIÓN AL TEXTO MÓVIL ---
      // Calculamos el centro usando el área real de dibujo del gráfico
      const centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
      const centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2;

      ctx.save();

      // 1. Dibuja el porcentaje
      ctx.font = 'bold 3rem sans-serif';
      ctx.fillStyle = '#2c3e50';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${capacityPercentage}%`, centerX, centerY - 25); // Lo subimos un poco

      // 2. Dibuja la primera línea del texto secundario
      ctx.font = '1rem sans-serif';
      ctx.fillStyle = '#6c757d';
      ctx.fillText('De su Capacidad', centerX, centerY + 20); // Lo ponemos debajo

      // 3. Dibuja la segunda línea del texto secundario
      ctx.fillText('Total', centerX, centerY + 40); // Y esta un poco más abajo

      ctx.restore();
    }
  }
};
</script>

<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>Capacidad del Embalse</h3>
    </div>
    <div class="chart-wrapper">
      <div class="chart-canvas-wrapper">
        <Doughnut :data="chartData" :options="chartOptions" :plugins="[centerTextPlugin]" />
      </div>
    </div>
  </div>
</template>


<style scoped>
.chart-container {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 0;

  height: 450px; /* Misma altura fija para la tarjeta */
  display: flex;
  flex-direction: column;
}

.chart-header {
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  text-align: center;
}

.chart-wrapper {
  position: relative;
  flex-grow: 1; /* Permite que este wrapper tome el espacio restante */
  min-height: 0; /* Asegura que se encoja bien */

  /* --- SOLUCIÓN: Damos al wrapper una altura explícita aquí --- */
  height: 100%; /* Ocupa el 100% del alto disponible de su padre */
}

/* .chart-canvas-wrapper no necesita cambios, ya estaba bien */
.chart-canvas-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
  display: flex; /* Para centrar el canvas si no ocupa todo el espacio */
  justify-content: center;
  align-items: center;
}

/* El canvas se auto-ajustará dentro de chart-canvas-wrapper */
/* No necesitamos !important aquí cuando maintainAspectRatio: false */
</style>
