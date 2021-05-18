import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    config: {},
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
  },
  actions: {}
})