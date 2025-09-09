<script setup lang="ts">
defineOptions({
  name: 'TheHeader'
});

const userName = 'Usuario A';
const userRole = 'Administrador';
</script>

<template>
  <header class="header-container">
    <div class="header-left">
      <div class="location-selector">
        <i class="pi pi-map-marker"></i>
        <span>Ubicación</span>
        <i class="pi pi-chevron-down"></i>
      </div>
    </div>

    <div class="header-right">
      <div class="notifications">
        <i class="pi pi-bell notification-icon"></i>
        <span class="notification-badge">2</span>
      </div>
      <div class="user-profile">
        <div class="user-avatar">
          <i class="pi pi-user"></i>
        </div>
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
          <span class="user-role">{{ userRole }}</span>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background-color: #ffffff;
  border-bottom: 1px solid #e9ecef;
  flex-shrink: 0; /* Evita que el header se encoja */
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.location-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #ced4da;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.notifications {
  position: relative;
  cursor: pointer;
}

.notification-icon {
  font-size: 1.5rem;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #d9534f;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 0.75rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f1f1f1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.user-avatar .pi-user {
  font-size: 1.25rem;
  color: #555;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: bold;
  font-size: 0.875rem;
}

.user-role {
  font-size: 0.75rem;
  color: #6c757d;
}
</style>
