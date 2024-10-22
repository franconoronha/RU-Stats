interface Prato {
    id: number;
    nome: string;
    porcao: string;
    composicao: string;
    calorias: number;
}

interface Cardapio {
    data: string;
    acompanhamento: number;
    arroz_branco: number;
    arroz_integral: number;
    feijao: number;
    fruta: number; 
    proteina_animal: number;
    proteina_vegetal: number;
    salada_cozida: number;
    salada_crua: number;
    salada_folhosa: number;
}

type PratoMap = { [id: number]: Prato };
type CardapioMap = { [data: string]: Cardapio };

interface Stats {
    prato: PratoMap;
    cardapio: CardapioMap;
}