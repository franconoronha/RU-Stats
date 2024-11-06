<template>
    <div v-if="lastCardapio && store.cardapio?.length"
         class="p-10 rounded-2xl flex flex-col items-center">
         <input type="date"
                ref="useDate"
                @change="changeCardapio"
                class="font-bold text-5xl text-center"
                :min="store.cardapio[0].data.toYyyyMmDd()"
                :max="store.cardapio.last()?.data.toYyyyMmDd()">
        <!-- <h3 class="text-center"> {{ lastCardapio?.data }}</h3> -->
        <div class="flex flex-wrap gap-1 mt-4 justify-center" v-if="cardapio">
            <Prato 
                v-for="pratoType in store.getKeys(cardapio)"
                :prato="store.getPrato(cardapio[pratoType])"
                :category="pratoType">
            </Prato>
        </div>
        <div class="mt-10"v-else>
            <p class="font-bold text-4xl">Sem dados para o dia selecionado.</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, useTemplateRef } from 'vue';
import Prato from '../Prato.vue';
import store from '../../store';

const useDate = useTemplateRef('useDate');
const cardapio = ref(); 
const lastCardapio = computed(() => store.cardapio ? store.cardapio[store.cardapio.length - 1] : null);

onMounted(() => {
    if (useDate.value)
        useDate.value.value = lastCardapio.value?.data.toYyyyMmDd() ?? "";
    if (lastCardapio.value)
        cardapio.value = lastCardapio.value;
});

const changeCardapio = (event: Event) => {
    const inputDate = (event.target as HTMLInputElement).value?.toDdMmYyyy();
    if (!inputDate) return;
    cardapio.value = store.cardapio?.find(c => c.data === inputDate);
}
</script>

<style scoped>
input[type="date"] {
  -webkit-text-fill-color: var(--primary);
}
</style>