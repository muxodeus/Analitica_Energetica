// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Reportes from '../views/Reportes.vue'
import Configuracion from '../views/Configuracion.vue'
import Tendencias from '../views/Tendencias.vue'
import Anomalias from '../views/Anomalias.vue'
import Estadisticas from '../views/Estadisticas.vue'
import FactorCarga from '../views/FactorCarga.vue'
import Patrones from '../views/Patrones.vue'
import ConsumoEnergetico from '../views/ConsumoEnergetico.vue'



const routes = [
  { path: '/', component: Dashboard },
  { path: '/reportes', component: Reportes },
  { path: '/configuracion', component: Configuracion },
  { path: '/consumo', component: ConsumoEnergetico },
  { path: '/historicos/tendencias', component: Tendencias },
  { path: '/historicos/estadisticas', component: Estadisticas },  // ← esta línea
  { path: '/historicos/factor-carga', component: FactorCarga },
  { path: '/historicos/anomalias', component: Anomalias },
  { path: '/historicos/patrones', component: Patrones },
  { path: '/consumo', component: ConsumoEnergetico },

]


export default createRouter({
  history: createWebHistory(),
  routes
})
