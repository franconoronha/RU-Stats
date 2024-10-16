<script setup lang="ts">
import { ref } from 'vue';
import { ApexOptions } from 'apexcharts';

const series = ref([
  {
    name: 'Desktops',
    data: [10, 41, 35, 51, 49, 62, 69, 91, 148]
  }
]);

const options: ApexOptions = {
  chart: {
    type: 'line'
  },
  xaxis: {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
  }
};
</script>

<template>
  <div>
    <h1>RU-Stats</h1>
    <apexchart width="500" type="line" :options="options" :series="series"></apexchart>
  </div>
</template>

<style scoped>
</style>
