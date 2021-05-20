import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    appName: "FinView",
    config: {},
    BASE_DIR: process.env.BASE_DIR || "/home/app",
    IMAGE_DIR: process.env.IMAGE_DIR || "/home/app/images",
    DATASET_DIR: process.env.DATASET_DIR || "/home/app/datasets",
    OUT_DIR: process.env.OUT_DIR || "/home/app/out",
    SYSTEM_DIR: process.env.SYSTEM_DIR || "/home/app/system",
    TASK_DIR: process.env.TASK_DIR || "/home/app/system/tasks",
    SERVER_HOST: process.env.VUE_APP_SERVER_HOST,
    NOTEBOOK_HOST: process.env.VUE_APP_NOTEBOOK_HOST,
    TASKS_HOST: process.env.VUE_APP_TASKS_HOST,
    CONTAINERS_HOST: process.env.VUE_APP_CONTAINERS_HOST,
    permittedFileFormats: ['csv', 'json'],
    permittedArchiveFormats: ['zip', 'tar'],
    permittedFileInputs: { "dir": "Directory", "image": "Image", "zip": "Zip", "tar": "Tar" },
    visualisationMethod: "umap"
  },
  mutations: {
    setConfig(state, config) {
      state.config = config;
    },
  },
  actions: {}
})
