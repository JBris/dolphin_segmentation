<template>
    <div class="modal-card ">
        <header class="modal-card-head">
            <h3>{{task.name}}</h3>
        </header>
        <section class="modal-card-body">
            <b-tabs position="is-centered" class="block" type="is-boxed" v-model="activeTab"> 

                <b-tab-item label="Visualise" icon="chart-line">
                    <div class="container" v-if="activeTab == 0">
                        <VisualiseForm 
                        v-bind:task="task" 
                        v-bind:taskBody="taskBody" 
                        v-bind:progress="progress" 
                        v-bind:value="progressPercent" 
                        v-on:update_task_list="updateTaskList()" 
                        v-on:close_modal="$parent.close()"/>
                    </div>
                </b-tab-item>

                <b-tab-item label="Delete" icon="delete">
                    <div class="container" v-if="activeTab == 1">
                        <DeleteForm v-bind:task="task" v-on:update_task_list="updateTaskList()" v-on:close_modal="$parent.close()"/>
                    </div>       
                </b-tab-item>

            </b-tabs>
        </section>
        <footer class="modal-card-foot">
          <b-button type="is-primary"
            label="Close"
            @click="$parent.close()"
            icon-left="close">
          </b-button>
        </footer>
    </div>
</template>

<script>
import task from '@/api/file/task'
import VisualiseForm from '@/components/forms/task/VisualiseForm'
import DeleteForm from '@/components/forms/task/DeleteForm'

export default {
    name: 'DatasetForm',
    components:{
        VisualiseForm,
        DeleteForm
    },
    props: {
        task: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            taskBody: {},
            progress: {},
            activeTab: 0,
            progressPercent: 0,
            watcher: null
        }
    },
    mounted() {
        this.loadTaskData()
        this.watcher = setInterval(() => {
            this.loadTaskData(false)
            this.getProgress()
        }, 1000)
    },
    beforeDestroy() {
        clearInterval(this.watcher)
    },
    methods: {
        updateTaskList() {
            this.$emit("update_task_list")
        },
        async loadTaskData(loading = true) {
            this.loading = loading
            this.taskBody = await task.get(this.$store.state.SERVER_HOST, this.task.name)
            const keys =  ["module", "solver", "task"]
            keys.forEach(key => this.taskBody[key] = this.taskBody[key].replace("_", " "))
            this.loading = false
        },
        async getProgress(loading = true) {
            this.loading = loading
            this.progress = await task.getProgress(this.$store.state.SERVER_HOST, this.task.id)
            this.loading = false
            if(this.taskBody.status == "complete") { this.progressPercent = 100 }
            else if(this.taskBody.status == "progress") { this.progressPercent =  undefined }            
            else this.progressPercent = 0
        }
    }
}
</script>

<style scoped lang="css">
h3 {
    color: #2c3e50;
}

.modal-card {
    width: auto;
}

.modal-card-head {
    box-shadow: 0.02em 0.02em 1.5px grey;
    border: 0.02em solid hsl(171, 100%, 41%);
    background-color: white;
    height: 7.5vh;
    justify-content: center;
}
</style>
