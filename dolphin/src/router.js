import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/Home.vue'
import Images from './components/body/Images.vue'
import Datasets from './components/body/Datasets.vue'
import Outputs from './components/body/Outputs.vue'
import Pipelines from './components/body/Pipelines.vue'
import Options from './components/body/Options.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/images', name: 'Images', component: Images },
  { path: '/datasets', name: 'Datasets', component: Datasets },
  { path: '/outputs', name: 'Outputs', component: Outputs },
  { path: '/pipelines', name: 'Pipelines', component: Pipelines },
  { path: '/options', name: 'Options', component: Options }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router