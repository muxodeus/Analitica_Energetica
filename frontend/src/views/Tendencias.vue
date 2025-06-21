<template>
  <div class="tendencias-dashboard">
    <header class="barra-superior">
      <h2>Tendencias históricas</h2>
      <div class="filtros">
        <Picklist
          v-model="variable"
          label="Variable"
          :options="[
            { value: 'energia', label: 'Energía activa (kWh)' },
            { value: 'potencia', label: 'Potencia (kW)' }
          ]"
        />
        <Picklist
          v-model="dispositivo"
          label="Dispositivo"
          :options="[
            { value: 'todos', label: 'Todos' },
            { value: 'medidor1', label: 'Medidor 1' },
            { value: 'medidor2', label: 'Medidor 2' }
          ]"
        />
        <div class="fechas">
          <label>Desde</label>
          <input type="date" v-model="desde" />
          <label>Hasta</label>
          <input type="date" v-model="hasta" />
        </div>
        <button @click="filtrar">Filtrar</button>
      </div>
    </header>

    <section class="selector-intervalo">
      <button @click="setInterval(7)">Últimos 7 días</button>
      <button @click="setInterval(15)">Últimos 15 días</button>
      <button @click="setInterval(30)">Últimos 30 días</button>
    </section>

    <section class="grafico-linea">
      <h3>Comportamiento por fecha</h3>
      <ApexChart
        type="line"
        height="320"
        :options="lineOptions"
        :series="lineSeries"
      />
    </section>

    <section class="grafico-heatmap">
      <h3>Mapa de consumo horario</h3>
      <ApexChart
        type="heatmap"
        height="320"
        :options="heatmapOptions"
        :series="heatmapSeries"
      />
    </section>
  </div>
</template>

<script setup>
import Picklist from '../components/Picklist.vue'
import { ref, onMounted } from 'vue'
import dayjs from 'dayjs'

const variable = ref('energia')
const dispositivo = ref('todos')
const desde = ref(dayjs().subtract(7, 'day').format('YYYY-MM-DD'))
const hasta = ref(dayjs().format('YYYY-MM-DD'))

const lineSeries = ref([
  { name: 'Actual', type: 'line', data: [] },
  { name: 'Histórico Promedio', type: 'area', data: [] }
])

const lineOptions = ref({
  chart: {
    id: 'tendencias-linea',
    toolbar: { tools: { zoom: true, reset: true, pan: true }},
    zoom: { enabled: true, type: 'x' }
  },
  colors: ['#007bff', '#b0c4de'],
  stroke: { curve: 'smooth' },
  xaxis: { type: 'datetime' },
  fill: {
    type: 'area',
    gradient: { opacityFrom: 0.2, opacityTo: 0 }
  },
  tooltip: { x: { format: 'yyyy-MM-dd' }}
})

const heatmapSeries = ref([])
const heatmapOptions = ref({
  chart: { id: 'tendencias-heatmap' },
  dataLabels: { enabled: false },
  xaxis: {
    type: 'category',
    categories: Array.from({ length: 24 }, (_, i) =>
      `${i.toString().padStart(2, '0')}h`
    )
  },
  colors: ['#e0f3f8', '#a6bddb', '#74a9cf', '#2b8cbe', '#045a8d'],
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      radius: 4,
      useFillColorAsStroke: false
    }
  }
})

function generarSeriesLine() {
  const inicio = dayjs(desde.value)
  const dias = dayjs(hasta.value).diff(inicio, 'day') + 1
  const actual = []
  const historico = []

  for (let i = 0; i < dias; i++) {
    const fecha = inicio.add(i, 'day').valueOf()
    actual.push({ x: fecha, y: +(Math.random() * 30 + 20).toFixed(2) })
    historico.push({ x: fecha, y: +(Math.random() * 10 + 25).toFixed(2) })
  }

  lineSeries.value[0].data = actual
  lineSeries.value[1].data = historico
}

function generarHeatmap() {
  const series = []
  for (let d = 1; d <= 7; d++) {
    const dia = `Día ${d}`
    const data = []
    for (let h = 0; h < 24; h++) {
      data.push({
        x: `${h.toString().padStart(2, '0')}h`,
        y: +(Math.random() * 8 + 2).toFixed(1)
      })
    }
    series.push({ name: dia, data })
  }
  heatmapSeries.value = series
}

function filtrar() {
  generarSeriesLine()
  generarHeatmap()
}

function setInterval(dias) {
  desde.value = dayjs().subtract(dias, 'day').format('YYYY-MM-DD')
  hasta.value = dayjs().format('YYYY-MM-DD')
  filtrar()
}

onMounted(() => {
  filtrar()
})
</script>

<style scoped>
.tendencias-dashboard {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.barra-superior {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filtros {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
}

.fechas {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.selector-intervalo {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
.selector-intervalo button {
  background: #e0e4ef;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
}
.selector-intervalo button:hover {
  background-color: #cfd4e2;
}
.grafico-linea,
.grafico-heatmap {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 1rem;
}
</style>
