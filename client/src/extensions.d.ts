export {};

declare global {
    interface String {
        prettify(): string;
        capitalize(): string;
        toYyyyMmDd(): string;
        toDdMmYyyy(): string;
    }
    interface Array<T> {
        last(): T | undefined;
    }
}