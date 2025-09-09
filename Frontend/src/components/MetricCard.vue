<script setup lang="ts">
import { computed } from 'vue';

defineOptions({
  name: 'MetricCard'
});

const props = defineProps<{
  title: string;
  value: string;
  unit: string;
  changeText: string;
  isPositive: boolean;
}>();

const changeClass = computed(() => {
  return props.isPositive ? 'change-positive' : 'change-negative';
});
</script>

<template>
  <div class="metric-card">
    <div class="card-header">
      <span class="title">{{ title }}</span>
      <i class="pi pi-check-circle status-icon"></i>
    </div>
    <div class="card-body">
      <span class="value">{{ value }}</span>
      <span class="unit">{{ unit }}</span>
    </div>
    <div class="card-footer">
      <span :class="changeClass">{{ changeText }}</span>
    </div>
  </div>
</template>

<style scoped>
.metric-card{background-color:#fff;border-radius:8px;padding:1.5rem;box-shadow:0 2px 4px rgba(0,0,0,.05);display:flex;flex-direction:column}.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem}.title{font-size:1rem;color:#6c757d;font-weight:500}.status-icon{color:#28a745;font-size:1.25rem}.card-body{display:flex;align-items:baseline;gap:.5rem;margin-bottom:.5rem}.value{font-size:2.5rem;font-weight:600;color:#333}.unit{font-size:1.5rem;font-weight:500;color:#6c757d}.card-footer{font-size:.875rem}.change-positive{color:#28a745}.change-negative{color:#dc3545}
</style>
