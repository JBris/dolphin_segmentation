<template>
    <div class="modal-card ">
        <header class="modal-card-head">
            <h3>{{task.name}}</h3>
        </header>
        <section class="modal-card-body">
            <b-tabs position="is-centered" class="block" type="is-boxed" v-model="activeTab"> 

                <b-tab-item label="Visualise" icon="chart-line">
                    <div class="container" v-if="activeTab == 0">
                        <VisualiseForm v-bind:task="task" v-on:update_task_list="updateTaskList()"/>
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
            activeTab: 0,
        }
    },
    methods: {
        updateTaskList() {
            this.$emit("update_task_list")
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
