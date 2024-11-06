import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import VueApexCharts from "vue3-apexcharts";
import './prototypes.ts';

const app = createApp(App);
app.use(VueApexCharts);
app.mount('#app');
