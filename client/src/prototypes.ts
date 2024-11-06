String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

String.prototype.prettify = function() {
    let str = this.replace(/_/g, ' ').toLocaleLowerCase();
    return str.split(' ').map((word: string) => {
        return word.capitalize();
    }).join(' ');
}

String.prototype.toYyyyMmDd = function() {
    return this.split('/').reverse().join('-');
}

String.prototype.toDdMmYyyy = function() {
    return this.split('-').reverse().join('/');
}

Array.prototype.last = function() {
    return this[this.length - 1];
}