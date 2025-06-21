// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'

const app = createApp(App)
app.use(router)
// Se registra globalmente el componente ApexChart
app.component('ApexChart', VueApexCharts)
app.mount('#app')
