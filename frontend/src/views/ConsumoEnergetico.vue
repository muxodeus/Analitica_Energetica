<template>
  <div class="dashboard-consumo-avanzado">
    <header class="header">
      <h2>Dashboard de Consumo de Energía Avanzado</h2>
      <div class="controls">
        <label>Desde:</label>
        <input type="date" v-model="desde" />
        <label>Hasta:</label>
        <input type="date" v-model="hasta" />
        <button @click="analizar">Analizar</button>
      </div>
    </header>
    
    <!-- Panel de KPIs Avanzados -->
    <section class="kpi-panel">
      <div class="card">
        <h3>Total de Consumo</h3>
        <p class="value">{{ totalConsumo }} kWh</p>
      </div>
      <div class="card">
        <h3>Consumo Promedio</h3>
        <p class="value">{{ promedioConsumo }} kWh</p>
      </div>
      <div class="card">
        <h3>Consumo Máximo</h3>
        <p class="value">{{ maxConsumo }} kW</p>
      </div>
      <div class="card">
        <h3>Desviación Estándar</h3>
        <p class="value">{{ desviacionConsumo }} kWh</p>
      </div>
      <div class="card">
        <h3>Coeficiente de Variación</h3>
        <p class="value">{{ coefVariacion }}%</p>
      </div>
      <div class="card">
        <h3>Predicción Siguiente Día</h3>
        <p class="value">{{ prediccion }} kWh</p>
      </div>
    </section>
    
    <!-- Gráficos -->
    <section class="charts">
      <!-- Tendencia con EMA -->
      <div class="chart-item">
        <h3>Tendencia con EMA</h3>
        <ApexChart type="line" height="300" :options="trendChartOptions" :series="trendChartSeries" />
      </div>
      
      <!-- Histograma de Distribución -->
      <div class="chart-item">
        <h3>Histograma de Consumo</h3>
        <ApexChart type="bar" height="300" :options="histChartOptions" :series="histChartSeries" />
      </div>
      
      <!-- Forecast para Próximas 24 Horas -->
      <div class="chart-item">
        <h3>Forecast 24h</h3>
        <ApexChart type="area" height="300" :options="forecastChartOptions" :series="forecastChartSeries" />
      </div>
      
      <!-- Gráfica de Barras de Consumo Diario -->
      <div class="chart-item">
        <h3>Consumo Diario (kWh)</h3>
        <ApexChart type="bar" height="300" :options="dailyBarOptions" :series="dailyBarSeries" />
      </div>
      
      <!-- Box Plot Diario -->
      <div class="chart-item">
        <h3>Box Plot Diario</h3>
        <ApexChart type="boxPlot" height="300" :options="boxPlotOptions" :series="boxPlotSeries" />
      </div>
      
      <!-- Heatmap de Consumo por Hora -->
      <div class="chart-item">
        <h3>Heatmap de Consumo por Hora</h3>
        <ApexChart type="heatmap" height="300" :options="heatmapOptions" :series="heatmapSeries" />
      </div>
      
      <!-- Scatter de Outliers -->
      <div class="chart-item">
        <h3>Scatter de Outliers</h3>
        <ApexChart type="scatter" height="300" :options="scatterChartOptions" :series="scatterChartSeries" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import dayjs from 'dayjs'
import ApexChart from 'vue3-apexcharts'

// Controles de fecha
const desde = ref(dayjs().subtract(7, 'day').format('YYYY-MM-DD'))
const hasta = ref(dayjs().format('YYYY-MM-DD'))

// KPIs
const totalConsumo = ref(0)
const promedioConsumo = ref(0)
const maxConsumo = ref(0)
const desviacionConsumo = ref(0)
const coefVariacion = ref(0)
const prediccion = ref(0)

// Gráfico: Tendencia con EMA
const trendChartSeries = ref([])
const trendChartOptions = ref({
  chart: { id: 'trend-chart' },
  xaxis: { type: 'datetime', labels: { datetimeUTC: false } },
  title: { text: 'Tendencia de Consumo (EMA)' }
})

// Gráfico: Histograma
const histChartSeries = ref([])
const histChartOptions = ref({
  chart: { id: 'hist-chart' },
  xaxis: { categories: [] },
  title: { text: 'Histograma del Consumo' }
})

// Gráfico: Forecast de Consumo
const forecastChartSeries = ref([])
const forecastChartOptions = ref({
  chart: { id: 'forecast-chart' },
  xaxis: { type: 'datetime', labels: { datetimeUTC: false } },
  title: { text: 'Forecast para Próximas 24 Horas' }
})

// Gráfico: Box Plot Diario
const boxPlotSeries = ref([])
const boxPlotOptions = ref({
  chart: { id: 'boxplot-chart' },
  title: { text: 'Box Plot Diario' }
})

// Gráfico: Heatmap de Consumo por Hora
const heatmapSeries = ref([])
const heatmapOptions = ref({
  chart: { id: 'heatmap-chart' },
  plotOptions: { heatmap: { shadeIntensity: 0.5, radius: 4 } },
  dataLabels: { enabled: false },
  xaxis: { type: 'category', categories: Array.from({ length: 24 }, (_, i) => `${i}h`) },
  title: { text: 'Heatmap de Consumo por Hora' }
})

// Gráfico: Scatter de Outliers
const scatterChartSeries = ref([])
const scatterChartOptions = ref({
  chart: { id: 'scatter-chart' },
  xaxis: { title: { text: 'Tiempo' } },
  yaxis: { title: { text: 'Consumo (kWh)' } },
  title: { text: 'Scatter de Outliers' }
})

// Nuevo: Gráfico de Barras de Consumo Diario
const dailyBarSeries = ref([])
const dailyBarOptions = ref({
  chart: { id: 'daily-bar-chart', type: 'bar' },
  xaxis: { categories: [] },
  title: { text: 'Consumo Diario (kWh)' }
})

function analizar() {
  // Simulación de datos horarios entre 'desde' y 'hasta'
  const startDate = dayjs(desde.value)
  const endDate = dayjs(hasta.value)
  const numDays = endDate.diff(startDate, 'day') + 1
  const consumptionData = []  // Cada registro: { timestamp, value }
  
  for (let d = 0; d < numDays; d++) {
    for (let h = 0; h < 24; h++) {
      const timestamp = startDate.add(d, 'day').hour(h).minute(0).second(0).valueOf()
      // Consumo simulado: base 50 kWh ± 15
      const value = +(50 + (Math.random() * 30 - 15)).toFixed(1)
      consumptionData.push({ timestamp, value })
    }
  }
  
  // KPIs
  totalConsumo.value = consumptionData.reduce((sum, d) => sum + d.value, 0).toFixed(1)
  promedioConsumo.value = (totalConsumo.value / consumptionData.length).toFixed(1)
  maxConsumo.value = Math.max(...consumptionData.map(d => d.value)).toFixed(1)
  const mean = promedioConsumo.value
  const variance = consumptionData.reduce((acc, d) => acc + Math.pow(d.value - mean, 2), 0) / consumptionData.length
  desviacionConsumo.value = Math.sqrt(variance).toFixed(1)
  coefVariacion.value = ((desviacionConsumo.value / promedioConsumo.value) * 100).toFixed(1)
  // Predicción: aumentar el promedio en un 10%
  prediccion.value = (promedioConsumo.value * 1.1).toFixed(1)
  
  // Tendencia: Serie de consumo y cálculo de EMA (ventana de 12 períodos)
  const trendData = consumptionData.map(d => ({ x: d.timestamp, y: d.value }))
  let emaData = []
  const period = 12
  const alpha = 2 / (period + 1)
  let emaPrev = trendData[0].y
  emaData.push({ x: trendData[0].x, y: emaPrev })
  for (let i = 1; i < trendData.length; i++) {
    const emaCurrent = alpha * trendData[i].y + (1 - alpha) * emaPrev
    emaData.push({ x: trendData[i].x, y: +emaCurrent.toFixed(1) })
    emaPrev = emaCurrent
  }
  trendChartSeries.value = [
    { name: 'Consumo Real', data: trendData },
    { name: 'EMA', data: emaData }
  ]
  
  // Histograma: Agrupar consumos en intervalos de 5 kWh
  const buckets = {}
  consumptionData.forEach(d => {
    const bucket = Math.floor(d.value / 5) * 5
    buckets[bucket] = (buckets[bucket] || 0) + 1
  })
  const bucketCategories = Object.keys(buckets).sort((a, b) => a - b)
  const bucketData = bucketCategories.map(bucket => buckets[bucket])
  histChartOptions.value.xaxis.categories = bucketCategories.map(b => `${b}-${+b + 5}`)
  histChartSeries.value = [{ name: 'Frecuencia', data: bucketData }]
  
  // Forecast: Predecir para las próximas 24 horas usando 'prediccion'
  const forecastData = []
  const lastTimestamp = consumptionData[consumptionData.length - 1].timestamp
  for (let h = 1; h <= 24; h++) {
    forecastData.push({ x: lastTimestamp + h * 3600000, y: +prediccion.value })
  }
  forecastChartSeries.value = [{ name: 'Forecast', data: forecastData }]
  
  // Box Plot: Agrupar datos por día y calcular [min, Q1, mediana, Q3, max]
  const dailyData = []
  for (let d = 0; d < numDays; d++) {
    const dayValues = consumptionData.filter(item =>
      dayjs(item.timestamp).isSame(startDate.add(d, 'day'), 'day')
    ).map(item => item.value)
    dailyData.push(dayValues)
  }
  boxPlotSeries.value = dailyData.map((values, index) => {
    values.sort((a, b) => a - b)
    const q1 = values[Math.floor(values.length * 0.25)]
    const median = values[Math.floor(values.length * 0.5)]
    const q3 = values[Math.floor(values.length * 0.75)]
    const min = values[0]
    const max = values[values.length - 1]
    return { x: startDate.add(index, 'day').format('YYYY-MM-DD'), y: [min, q1, median, q3, max] }
  })
  
  // Heatmap: Para hasta 7 días, contar por cada hora los registros con consumo > 60 kWh
  const heatmapData = []
  const daysHeatmap = Math.min(numDays, 7)
  for (let d = 0; d < daysHeatmap; d++) {
    const hourlyData = []
    for (let h = 0; h < 24; h++) {
      const count = consumptionData.filter(item =>
        dayjs(item.timestamp).isSame(startDate.add(d, 'day'), 'day') &&
        dayjs(item.timestamp).hour() === h &&
        item.value > 60
      ).length
      hourlyData.push({ x: `${h}h`, y: count })
    }
    heatmapData.push({ name: `Día ${d + 1}`, data: hourlyData })
  }
  heatmapSeries.value = heatmapData
  
  // Scatter: Outliers (más de 2 desviaciones estándar de la media)
  const scatterData = consumptionData.filter(d =>
    d.value > (mean + 2 * desviacionConsumo.value) || d.value < (mean - 2 * desviacionConsumo.value)
  ).map(d => ({ x: d.timestamp, y: d.value }))
  scatterChartSeries.value = [{ name: 'Outliers', data: scatterData }]
  
  // Nuevo: Consumo Diario en kWh (suma de consumos por día)
  const dailyConsumption = []
  for (let d = 0; d < numDays; d++) {
    const dayTotal = consumptionData.filter(item =>
      dayjs(item.timestamp).isSame(startDate.add(d, 'day'), 'day')
    ).reduce((acc, item) => acc + item.value, 0)
    dailyConsumption.push(+dayTotal.toFixed(1))
  }
  dailyBarSeries.value = [{ name: 'Consumo Diario', data: dailyConsumption }]
  dailyBarOptions.value.xaxis.categories = Array.from({ length: numDays }, (_, i) => startDate.add(i, 'day').format('YYYY-MM-DD'))
}

analizar()
</script>

<style scoped>
.dashboard-consumo-avanzado {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.controls label {
  font-weight: bold;
}

.kpi-panel {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.card {
  background: #fff;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  flex: 1;
  text-align: center;
}

.card .value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1rem;
}

.chart-item {
  background: #fff;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.advanced-analysis {
  margin-top: 2rem;
}
</style>
