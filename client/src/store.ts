import { reactive } from "vue";

interface Store {
    cardapio: Cardapio[] | null;
    pratos: PratoMap;
    getStats(): Promise<void>;
    getPrato(id: number | string): Prato | undefined | null;
    // getPratoId(cardapio: Cardapio, key: PratoTypes): number;
    getKeys(cardapio: Cardapio): CardapioKeys[];
}

const store = reactive<Store>({
    cardapio: null,
    pratos: {} as PratoMap,

    async getStats() {
        const stats = await fetch('/db.json').then(res => res.json()) as Stats;
        this.cardapio = Object.values(stats.cardapio);
        this.pratos = stats.prato;
    },

    getPrato(id: number | string) {
        if (typeof id === 'string') {
            return null;
        }
        return this.pratos[id];   
    },

    // getPratoId(cardapio: Cardapio, key: ) { 
    //     return cardapio[key];
    // },

    getKeys(cardapio?: Cardapio) {
        if (!cardapio) return [];
        console.log(cardapio);
        return Object.keys(cardapio).filter(key => key !== 'data') as CardapioKeys[];
    }
});

export default store;