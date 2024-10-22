<script setup lang="ts">
import { onMounted, ref } from 'vue';
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

let proteinas_animal = ref<number[]>([]);
let proteinas_vegetal = ref<number[]>([]);

onMounted(async () => {
  const stats = await fetch('/db.json').then(res => res.json()) as Stats;
  const cardapio = Object.keys(stats.cardapio).map(key => stats.cardapio[Number(key)]);
  const pratos = Object.keys(stats.prato).map(key => stats.prato[Number(key)]);

  proteinas_animal.value = cardapio.map(item => item.proteina_animal);
  proteinas_vegetal.value = cardapio.map(item => item.proteina_vegetal);

  console.log(proteinas_animal.value);
});
</script>

<template>
    <main>
        <div class="pt-5">
            <h1>RU Stats</h1>
        </div>
        <apexchart width="500" type="line" :options="options" :series="series"></apexchart>
        <div>
            <p v-for="proteina in proteinas_animal">
                {{ proteina }}
            </p>
        </div>
    </main>
</template>

<style scoped></style>