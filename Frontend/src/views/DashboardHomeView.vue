<script setup lang="ts">
import MetricCard from '@/components/MetricCard.vue';

defineOptions({
  name: 'DashboardHomeView'
});
</script>

<template>
  <div class="metrics-grid">
    <MetricCard
      title="Temperatura"
      value="14.2"
      unit="C°"
      changeText="-2.2 C° bajo lo esperado"
      :isPositive="true"
    />
    <MetricCard
      title="Oxígeno Disuelto"
      value="0.25"
      unit="PPM"
      changeText="-$2,201"
      :isPositive="false"
    />
    <MetricCard
      title="Salinidad"
      value="45"
      unit=""
      changeText="+5.39 sobre lo esperado"
      :isPositive="false"
    />
    <MetricCard
      title="Ph"
      value="7.0"
      unit=""
      changeText="-1.22 bajo lo esperado"
      :isPositive="true"
    />
  </div>
</template>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
</style>
