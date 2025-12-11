// main.ts
import {createApp} from 'vue'
import App from './App.vue'

import './assets/main.css';

// Add the necessary CSS
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

const app = createApp(App)
app.mount('#app')
