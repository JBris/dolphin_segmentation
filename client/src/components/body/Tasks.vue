<template>
    <content>
        <div class="columns">
            <div class="column">
                <section class="create-button level-left">
                  <b-button type="is-success"
                    v-on:click="create"
                    icon-left="plus">
                      Create
                  </b-button>
                </section>
            </div>
            <div class="column is-half">
                <b-field>
                    <b-autocomplete v-model="taskName" field="name" group-field="status" icon="magnify"
                        @select="option => selectTask(option)" :data="filteredTasks">
                        <template slot-scope="props">
                            <div class="media">
                              <div class="media-left">
                                <img width="32" v-if="props.option.status == 'complete'" :src="require('@/assets/images/task_complete.svg')" lazy>
                                <img width="32" v-else-if="props.option.status == 'failed'" :src="require('@/assets/images/task_failed.svg')" lazy>
                                <img width="32" v-else :src="require('@/assets/images/task_incomplete.svg')" lazy>
                              </div>
                              <div class="media-content">
                                  {{ props.option.name}}
                              </div>
                            </div>
                        </template>
                    </b-autocomplete>
                </b-field>
            </div>
        </div>
        <hr>
        <section>
            <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
            <p v-if="!this.taskList.length && !this.loading">No tasks currently available.</p>
            <div v-else>
                <section class="image-dir-path">
                    <div class="columns is-multiline">
                        <div v-for="(task, index) in paginatedItems" :key=index
                            class="column is-one-fifth  has-text-centered">
                              <TaskItem v-bind:task="task" v-on:task_selected="selectTask(task)"/>
                        </div>
                    </div>
                </section>
            </div>
        </section>
        <hr>
        <b-pagination
            :total="itemTotal"
            v-model="current"
            :per-page="perPage"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">
        </b-pagination>
    </content>
</template>

<script>
import collection from '@/api/file/collection'
import { TASKS } from '@/api/endpoints'
import TaskItem from '@/components/body/TaskItem'
import TaskCreateForm from '@/components/forms/task/TaskCreateForm'
import TaskForm from '@/components/forms/TaskForm'

export default {
  name: 'Tasks',
  components: {
    TaskItem
  },
  data() {
    return {
      loading: true,
      error: false,
      tasksDir: "",
      taskName: "",
      taskList: [],
      current: 1,
      perPage: 20,
    }
  },
  computed: {
    filteredTasks() {
      return this.taskList.filter(task => task.name.toLowerCase().indexOf(this.taskName.toLowerCase()) >= 0)
    },
    taskListNames() {
      return this.taskList.map(task => task.name)
    },
    paginatedItems() {
      let pageNumber = this.current-1
      return this.taskList.slice(pageNumber * this.perPage, (pageNumber + 1) * this.perPage);  
    },
    itemTotal() {
      return this.taskList.length
    },
  },
  mounted() {
    this.getTaskList()
    this.subscribeToTasks()
  },
  methods: {
    async getTaskList(tasksDir = this.$store.state.TASK_DIR, loading = true) {
      this.loading = loading
      try {
        this.tasksDir = tasksDir
        this.taskList = await collection.getAll(this.$store.state.SERVER_HOST, TASKS, this.tasksDir)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    create() {
      this.$buefy.modal.open({
        parent: this,
        component: TaskCreateForm,
        props: {
          taskListNames: this.taskListNames
        },
        hasModalCard: true,
        trapFocus: true,
        fullScreen: true,
        events: {
          update_task_list: () => this.getTaskList(this.$store.state.TASK_DIR, false)
        }
      })
    },
    selectTask(task) {
      if(task == null) return;
      this.$buefy.modal.open({
        parent: this,
        component: TaskForm,
        props: {
          task: task,
        },
        hasModalCard: true,
        trapFocus: true,
        fullScreen: true,
        events: {
          update_task_list: () => this.getTaskList(this.$store.state.TASK_DIR, false)
        }
      })
    },
    subscribeToTasks() {
      this.$store.subscribe(mutation => {
        if(mutation.type === 'updateTaskStatus'){
            this.getTaskList(this.$store.state.TASK_DIR, false)
        }
      })
    }
  }
}
</script>

<style scoped lang="css">
.create-button {
  padding-bottom: 1.5vh;
}

p:first-letter {
    text-transform:capitalize;
}

</style>