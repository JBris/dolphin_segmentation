import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from './components/Home.vue'
import ImageList from './components/body/ImageList.vue'
import Datasets from './components/body/Datasets.vue'
import Outputs from './components/body/Outputs.vue'
import Tasks from './components/body/Tasks.vue'
import Options from './components/body/Options.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/images', name: 'Images', component: ImageList, props: true },
  { path: '/datasets', name: 'Datasets', component: Datasets, props: true },
  { path: '/outputs', name: 'Outputs', component: Outputs, props: true },
  { path: '/tasks', name: 'Tasks', component: Tasks },
  { path: '/options', name: 'Options', component: Options }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router