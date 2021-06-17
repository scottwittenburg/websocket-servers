<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <input type="button" value="Connect" v-on:click="connect" :disabled="connected === true">
    <input type="button" value="Disconnect" v-on:click="disconnect" :disabled="connected === false">
    <label for="msgsReceivedArea">Received Messages</label>
    <textarea id="msgsReceivedArea" readonly rows=10 cols=100 v-model="messageList"></textarea>
    <input type="text" size="100" v-on:keydown.enter="sendMessage" v-model="messageToSend">
    <input type="button" value="Send" v-on:click="sendMessage" :disabled="connected === false">
    <input type="button" value="Expensive Operation" v-on:click="customEndpoint">
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      ws: null,
      connected: false,
      msgsReceived: [],
      messageToSend: '',
    }
  },
  computed: {
    messageList() {
      return this.msgsReceived.join('\n');
    },
  },
  methods: {
    connect() {
      this.ws = new WebSocket("ws://localhost:8080/ws");
      const self = this;
      this.ws.onopen = () => {
        self.connected = true;
        self.ws.send("Hello server");
      };
      this.ws.onmessage = function (evt) {
         self.msgsReceived.unshift(evt.data);
      };
      this.ws.onerror = function (evt) {
        console.log('client websocket error handler');
        console.log(evt);
      };
      this.ws.onclose = function (evt) {
        console.log('client websocket close handler');
        console.log(evt);
        self.cleanup();
      };
    },
    disconnect() {
      this.ws.close();
      this.cleanup();
    },
    sendMessage() {
      this.ws.send(this.messageToSend);
      this.messageToSend = '';
    },
    cleanup() {
      this.connected = false;
      this.msgsReceived = [];
      this.messageToSend = '';
      this.ws = null;
    },
    customEndpoint() {
      console.log('Sending request to /slow');
      axios.get('/slow')
        .then(function (response) {
          // handle success
          alert(response.data)
          console.log(response);
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        });
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
