import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    appName: "FinView",
    config: {},
    IMAGE_DIR: process.env.IMAGE_DIR || "/home/app/images",
    DATASET_DIR: process.env.DATASET_DIR || "/home/app/datasets",
    OUT_DIR: process.env.OUT_DIR || "/home/app/out",
    SERVER_HOST: process.env.VUE_APP_SERVER_HOST,
    NOTEBOOK_HOST: process.env.VUE_APP_NOTEBOOK_HOST,
    TASKS_HOST: process.env.VUE_APP_TASKS_HOST,
    permittedFileFormats: ['csv', 'json']
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
  },
  actions: {}
})
