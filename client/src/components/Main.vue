<script setup lang="ts">
import { onMounted } from 'vue';
import LastCardapio from './dataComponent/LastCardapio.vue';
import Count from './dataComponent/Count.vue';
import DayDistribution from './dataComponent/DayDistribution.vue';
import LongestAbsence from './dataComponent/LongestAbsence.vue';
import Catalogue from './dataComponent/Catalogue.vue';
import store from '../store';

onMounted(async () => {
  store.getStats();
});
</script>

<template>
    <main>
        <div class="pt-10 mb-5">
            <h1>RU Stats</h1>
        </div>
        <div v-if="store.cardapio">
            <LastCardapio></LastCardapio>
            <Count></Count>
            <DayDistribution></DayDistribution>
            <LongestAbsence></LongestAbsence>
            <Catalogue></Catalogue>
        </div>
    </main>
</template>

<style scoped></style>