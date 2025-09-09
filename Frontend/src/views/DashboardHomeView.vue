<script setup lang="ts">
import MetricCard from '@/components/MetricCard.vue';
import WaterLevelChart from '@/components/WaterLevelChart.vue';
import ReservoirCapacityChart from '@/components/ReservoirCapacityChart.vue';
import SensorsTable from '@/components/SensorsTable.vue'; // <-- 1. Importar

defineOptions({
  name: 'DashboardHomeView'
});
</script>

<template>
  <div class="dashboard-content">
    <div class="metrics-grid">
      <MetricCard title="Temperatura" value="14.2" unit="C°" changeText="-2.2 C° bajo lo esperado" :isPositive="true"/>
      <MetricCard title="Oxígeno Disuelto" value="0.25" unit="PPM" changeText="-$2,201" :isPositive="false"/>
      <MetricCard title="Salinidad" value="45" unit="" changeText="+5.39 sobre lo esperado" :isPositive="false"/>
      <MetricCard title="Ph" value="7.0" unit="" changeText="-1.22 bajo lo esperado" :isPositive="true"/>
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

/* 3. Estilo para el contenedor de la tabla */
.table-widget {
  margin-top: 2rem;
}

/* Para pantallas más pequeñas, los gráficos y la tabla se apilan */
@media (max-width: 992px) {
  .main-widgets-grid {
    grid-template-columns: 1fr;
  }
}
</style>
