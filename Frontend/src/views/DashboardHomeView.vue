<script setup lang="ts">
import { ref, onMounted } from 'vue';
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue';
import type { Metric } from '@/types'; // Asumiendo que tienes esta interfaz en types/index.ts

defineOptions({
  name: 'DashboardHomeView'
});

// --- Lógica para las Tarjetas de Métricas ---
const metrics = ref<{
  temperatura: Metric;
  nitrogeno: Metric;
  electroconductividad: Metric;
  ph: Metric;
} | null>(null);
const errorMetrics = ref<string | null>(null);

// --- Lógica para el Gráfico Interactivo ---
const chartData = ref({ labels: [], real_level: [], expected_level: [] });
const isLoadingChart = ref(true);
const errorChart = ref<string | null>(null);
const selectedDateRange = ref('last_30');
const customStartDate = ref('');
const customEndDate = ref('');

onMounted(async () => {
  await fetchMetrics();
  await fetchWaterLevelData({ limit: 30 }); // Carga inicial de los últimos 30 registros
});

async function fetchMetrics() {
  const token = localStorage.getItem('userToken');
  try {
    const response = await fetch('http://127.0.0.1:8000/api/metrics/latest', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!response.ok) throw new Error('Error al cargar métricas');
    metrics.value = await response.json();
  } catch (e) {
    console.error(e);
    errorMetrics.value = "No se pudieron cargar las métricas.";
  }
}

async function fetchWaterLevelData(params: { startDate?: string, endDate?: string, limit?: number } = {}) {
  isLoadingChart.value = true;
  errorChart.value = null;
  const token = localStorage.getItem('userToken');
  const queryParams = new URLSearchParams();
  if (params.startDate) queryParams.append('start_date', params.startDate);
  if (params.endDate) queryParams.append('end_date', params.endDate);
  if (params.limit) queryParams.append('limit', String(params.limit));

  const apiUrl = `http://127.0.0.1:8000/api/charts/water-level?${queryParams.toString()}`;

  try {
    const response = await fetch(apiUrl, { headers: { 'Authorization': `Bearer ${token}` } });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error al obtener datos del gráfico.');
    }
    chartData.value = await response.json();
  } catch (e: unknown) {
    if (e instanceof Error) {
      errorChart.value = e.message;
    } else {
      errorChart.value = String(e);
    }
    chartData.value = { labels: [], real_level: [], expected_level: [] };
  } finally {
    isLoadingChart.value = false;
  }
}

function changeDateRange(range: string) {
  selectedDateRange.value = range;
  const now = new Date();
  const start = new Date();

  if (range === 'last_24_hours') {
    start.setTime(now.getTime() - 24 * 60 * 60 * 1000);
    fetchWaterLevelData({ startDate: start.toISOString(), endDate: now.toISOString() });
  } else if (range === 'last_7_days') {
    start.setDate(now.getDate() - 7);
    fetchWaterLevelData({ startDate: start.toISOString(), endDate: now.toISOString() });
  } else if (range === 'last_30') {
    fetchWaterLevelData({ limit: 30 });
  }
}

function applyCustomDateRange() {
  if (customStartDate.value && customEndDate.value) {
    selectedDateRange.value = 'custom';
    const start = new Date(customStartDate.value);
    const end = new Date(customEndDate.value);
    fetchWaterLevelData({ startDate: start.toISOString(), endDate: end.toISOString() });
  } else {
    alert('Por favor, selecciona una fecha de inicio y de fin.');
  }
}
</script>

<template>
  <div class="dashboard-content">
    <header class="view-header">
      <h1>Dashboard del Embalse</h1>
      <p>Vista general y análisis de los datos más recientes del sistema.</p>
    </header>

    <section class="dashboard-section">
      <h2 class="section-title">Última Medición Registrada</h2>
      <div v-if="errorMetrics" class="error-message">{{ errorMetrics }}</div>
      <div v-else-if="!metrics"><p>Cargando métricas...</p></div>
      <div v-else class="metrics-grid">
        <MetricCard title="Temperatura" :value="String(metrics.temperatura.value)" :unit="metrics.temperatura.unit" :changeText="metrics.temperatura.changeText" :isPositive="metrics.temperatura.isPositive" />
        <MetricCard title="Nitrógeno" :value="String(metrics.nitrogeno.value)" :unit="metrics.nitrogeno.unit" :changeText="metrics.nitrogeno.changeText" :isPositive="metrics.nitrogeno.isPositive" />
        <MetricCard title="Electroconductividad" :value="String(metrics.electroconductividad.value)" :unit="metrics.electroconductividad.unit" :changeText="metrics.electroconductividad.changeText" :isPositive="metrics.electroconductividad.isPositive" />
        <MetricCard title="Ph" :value="String(metrics.ph.value)" :unit="metrics.ph.unit" :changeText="metrics.ph.changeText" :isPositive="true" />
      </div>
    </section>

    <section class="dashboard-section chart-card">
      <div class="chart-controls">
        <h2 class="section-title no-border">Análisis Histórico y Capacidad</h2>
        <div class="filters">
          <div class="date-range-selector">
            <button @click="changeDateRange('last_24_hours')" :class="{ active: selectedDateRange === 'last_24_hours' }">24h</button>
            <button @click="changeDateRange('last_7_days')" :class="{ active: selectedDateRange === 'last_7_days' }">7d</button>
            <button @click="changeDateRange('last_30')" :class="{ active: selectedDateRange === 'last_30' }">30 Días</button>
          </div>
          <div class="custom-date-range">
            <input type="datetime-local" v-model="customStartDate" />
            <span>-</span>
            <input type="datetime-local" v-model="customEndDate" />
            <button @click="applyCustomDateRange">Aplicar</button>
          </div>
        </div>
      </div>

      <div class="main-widgets-grid">
        <div class="water-level-container">
          <div v-if="isLoadingChart" class="loading-state">Cargando gráfico...</div>
          <div v-else-if="errorChart" class="error-message">{{ errorChart }}</div>
          <WaterLevelChart v-else :chartData="chartData" title="Nivel de Agua" />
        </div>
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
.dashboard-content{padding:1.5rem 2rem}.view-header{margin-bottom:2rem}.view-header h1{font-size:2rem;font-weight:700;margin:0 0 .25rem;color:#2c3e50}.view-header p{font-size:1.1rem;color:#6c757d;margin:0}.dashboard-section{margin-bottom:2rem}.section-title{font-size:1.25rem;font-weight:600;color:#34495e;margin-bottom:1rem;padding-bottom:.5rem;border-bottom:1px solid #dee2e6}.section-title.no-border{border-bottom:none;margin-bottom:0}.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.5rem}.main-widgets-grid{display:grid;grid-template-columns:2fr 1fr;gap:1.5rem;align-items:stretch}.table-widget{}@media (max-width:992px){.main-widgets-grid{grid-template-columns:1fr}}.chart-card{background-color:#fff;border-radius:8px;padding:1.5rem;box-shadow:0 2px 4px rgba(0,0,0,.05)}.chart-controls{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;margin-bottom:1rem}.filters{display:flex;align-items:center;gap:1rem;flex-wrap:wrap}.date-range-selector button{margin-right:.5rem;padding:.5rem 1rem;border:1px solid #dee2e6;background-color:#fff;border-radius:6px;cursor:pointer;transition:all .2s}.date-range-selector button.active{background-color:#007bff;color:#fff;border-color:#007bff}.custom-date-range{display:flex;align-items:center;gap:.5rem}.custom-date-range input{padding:.5rem;border:1px solid #ced4da;border-radius:6px}.custom-date-range button{padding:.5rem 1rem;border:none;background-color:#28a745;color:#fff;border-radius:6px;cursor:pointer}.loading-state,.error-message{text-align:center;padding:2rem;color:#6c757d}
</style>
