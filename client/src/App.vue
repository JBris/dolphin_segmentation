<template>
  <div id="app">
    <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
    <Header/>
    <Body/>
    <Footer/>
  </div>
</template>

<script>
import Header from './components/layout/Header';
import Body from './components/body/Body';
import Footer from './components/layout/Footer';
import config from './config'

export default {
  name: 'App',
  components: {
    Header,
    Body,
    Footer
  },
  data() {
    return {
      loading: true,
      error: false,
    }
  },
  mounted() {
    this.getConfig()
    this.subscribeToTasks()
  },
  methods: {
    async getConfig() {
      try {
        const configuration = await config.get(this.$store.state.SERVER_HOST)
        this.$store.commit('setConfig', configuration)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    subscribeToTasks() {
      this.$store.subscribe((mutation, state) => {
        if(mutation.type === 'updateTaskStatus'){
            this.$buefy.snackbar.open({message: state.lastTaskStatus, duration: 2500, type: "is-primary", position: "is-bottom"})
        }
      })
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
</style>
