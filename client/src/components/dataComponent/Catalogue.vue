<template>
    <div class="flex text-4xl font-bold gap-8 justify-center">
        <p>
            <span class="text-5xl">{{ store.cardapio?.length }}</span> dias coletados
        </p>
        <p>
            <span class="text-5xl">{{ Object.keys(store.pratos).length }}</span> pratos coletados
        </p>
    </div>
</template>

<script setup lang="ts">
import store from '../../store';
</script>

<style scoped>
</style>
