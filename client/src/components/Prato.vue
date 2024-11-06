<template v-if="prato">
    <div class="text-[#FEFEFE] tracking-wider text-lg">
        <p class="text-primary text-center">{{ categoryTitle }}</p>
        <button :popovertarget="`popover-${prato?.id}`"
                class="prato card relative border border-primary m-1 p-2 rounded bg-primary"
                :style="`anchor-name: --popover-${prato?.id}`">
            <p>{{ prato?.nome.prettify() }}</p>
            <p>{{ prato?.calorias }}cal / {{ porcao }}</p>
        </button>
        <div popover :id="`popover-${prato?.id}`"
             :style="`position-anchor: --popover-${prato?.id}`" 
             class="popover p-2 rounded shadow-2xl border border-primary border-dashed">
            {{ prato?.composicao }}
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
    prato: Prato | undefined | null;
    category: string;
}>();

const categoryTitle = computed(() => props.category.replace('_', ' '));
const porcao = computed(() => props.prato?.porcao.replace('gramas', 'g').replace(' ', ''));
</script>

<style scoped>
.prato {
    width: 300px;
}

.popover {
    margin: 1rem;
    max-width: 400px;
    position-area: bottom;
}
</style>