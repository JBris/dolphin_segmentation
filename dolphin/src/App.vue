<template>
  <div id="app">
    <Header/>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <Footer/>
  </div>
</template>

<script>
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HelloWorld from './components/HelloWorld.vue'
import config from './config'

export default {
  name: 'App',
  components: {
    Header,
    HelloWorld,
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
  },
  methods: {
    async getConfig() {
      try {
        const configuration = await config.get()
        configuration["SERVER_HOST"] = process.env.VUE_APP_SERVER_HOST
        configuration["NOTEBOOK_HOST"] = process.env.VUE_APP_NOTEBOOK_HOST
        configuration["TASKS_HOST"] = process.env.VUE_APP_TASKS_HOST
        this.$store.commit('setConfig', configuration)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
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
  margin-top: 60px;
}
</style>
