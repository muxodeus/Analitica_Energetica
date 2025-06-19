import { createApp } from 'vue'
import App from './App.vue'
import VueApexCharts from 'vue3-apexcharts'
import axios from 'axios'

axios.defaults.baseURL = '/api/'
createApp(App)
  .use(VueApexCharts)
  .mount('#app')
