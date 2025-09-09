<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
/* NOTA: Esta etiqueta <style> NO tiene la palabra "scoped".
   Eso significa que estos estilos son GLOBALES y se aplican a toda la página.
*/
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background-color: #f4f6f9;
}
</style>
