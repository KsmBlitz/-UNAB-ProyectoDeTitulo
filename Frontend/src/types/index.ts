export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  disabled: boolean;
}

// Nueva interfaz para las tarjetas de métricas
export interface Metric {
  value: string | number;
  unit: string;
  changeText: string;
  isPositive: boolean;
}
