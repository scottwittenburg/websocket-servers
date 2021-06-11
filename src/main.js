import { createApp } from 'vue'
import axios from 'axios';
import App from './App.vue'

console.log('Sending initial request to /custom')
axios.get('/custom')
  .then(function (response) {
    // handle success
    console.log(response);
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })

createApp(App).mount('#app')
