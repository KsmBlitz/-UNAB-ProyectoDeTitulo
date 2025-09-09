<script setup lang="ts">
defineOptions({
  name: 'SensorsTable'
});

// Definimos una 'interfaz' para nuestros datos para que TypeScript nos ayude
interface Sensor {
  name: string;
  lastReading: string;
  uid: string;
  location: string;
  status: 'Activo' | 'Inactivo';
}

// Datos de ejemplo
const sensors: Sensor[] = [
  { name: 'Puerta Embalse Salida', lastReading: '19 May, 2021 - 10:10 AM', uid: '251-661-5362', location: 'Lon: 47.4454121\nLat: 19.1120139', status: 'Activo' },
  { name: 'Puerta Embalse Entrada', lastReading: '18 May, 2021 - 3:12 PM', uid: '171-534-1262', location: 'Lon: 47.4454121\nLat: 19.1120139', status: 'Activo' },
  { name: 'Boya 1', lastReading: '17 May, 2021 - 2:15 PM', uid: '974-661-5110', location: 'Lon: 47.4454121\nLat: 19.1120139', status: 'Inactivo' },
  { name: 'Boya 2', lastReading: '23 Apr, 2021 - 1:15 PM', uid: '541-661-3042', location: 'Lon: 47.4454121\nLat: 19.1120139', status: 'Activo' },
];
</script>

<template>
  <div class="sensors-card">
    <div class="card-header">
      <h3>Sensores</h3>
      <i class="pi pi-cog settings-icon"></i>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Última Medición</th>
            <th>UID</th>
            <th>Ubicación</th>
            <th>Estado</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sensor in sensors" :key="sensor.uid">
            <td>{{ sensor.name }}</td>
            <td>{{ sensor.lastReading }}</td>
            <td>{{ sensor.uid }}</td>
            <td class="location-cell">{{ sensor.location }}</td>
            <td>
              <span class="status-pill" :class="{
                'status-active': sensor.status === 'Activo',
                'status-inactive': sensor.status === 'Inactivo'
              }">
                {{ sensor.status }}
              </span>
            </td>
            <td>
              <div class="action-links">
                <a href="#">Options</a>
                <a href="#">Details</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="pagination-footer">
      <button class="page-item active">1</button>
      <button class="page-item">2</button>
      <button class="page-item">...</button>
    </div>
  </div>
</template>

<style scoped>
.sensors-card {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.settings-icon {
  cursor: pointer;
  color: #6c757d;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
  white-space: pre-wrap;
}

thead th {
  color: #6c757d;
  font-weight: 500;
  font-size: 0.875rem;
  text-transform: uppercase;
}

tbody tr:last-child td {
  border-bottom: none;
}

.status-pill {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #e9ecef;
  color: #6c757d;
}

.action-links {
  display: flex;
  gap: 1rem;
}

.action-links a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.action-links a:hover {
  text-decoration: underline;
}

.pagination-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
  gap: 0.5rem;
}

.page-item {
  border: 1px solid #dee2e6;
  background-color: #ffffff;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
}

.page-item.active {
  background-color: #f1f1f1;
  font-weight: bold;
}
</style>
