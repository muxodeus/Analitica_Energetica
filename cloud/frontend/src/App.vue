<template>
  <div>
    <h1>Monitoreo Energético</h1>
    <realtime-chart/>
    <history-chart/>
    <stats-panel/>
  </div>
</template>
<script>
import RealtimeChart from './components/RealtimeChart.vue'
import HistoryChart  from './components/HistoryChart.vue'
import StatsPanel    from './components/StatsPanel.vue'
export default { components:{RealtimeChart,HistoryChart,StatsPanel} }
</script>
