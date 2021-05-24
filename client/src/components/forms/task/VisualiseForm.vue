<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <div class="content">
            <h3> Task {{taskBody.status}}</h3>
            <p class="upper">Module: {{taskBody.module}}</p>
            <p class="upper">Action: {{taskBody.task}}</p>
            <p class="upper">Solver: {{taskBody.solver}}</p>
            <p>Destination: <router-link :to="{ name: destination, params: { path: taskBody.out }}" v-on:click.native="close">{{taskBody.out}}</router-link></p>
        </div>

        <div >
            <hr>
            <h3>Progress</h3>
            <h3 v-if="progress.step">Step: {{progress.step}}</h3>
            <b-progress v-if="progress.status == 'progress'" type="is-success"></b-progress>
            <b-progress v-else type="is-success" :value="value"></b-progress>
        </div>
    </section>
</template>

<script>

export default {
    name: 'VisualiseForm',
    props: {
        task: {
            type: Object,
            required: true
        },
        taskBody: {
            type: Object,
            required: true          
        },
        progress: {
            type: Object,
            required: true          
        },
        value: {
            type: Number,
            required: false,
            default: 0
        }
    },
    data() {
        return {
            loading: false,
        }
    },
    computed: {
        destination() {
            if(!this.taskBody.out) { return "" }
            if(this.taskBody.out.startsWith(this.$store.state.DATASET_DIR)) { return "Datasets" }
            if(this.taskBody.out.startsWith(this.$store.state.OUT_DIR)) { return "Outputs" }
            if(this.taskBody.out.startsWith(this.$store.state.IMAGE_DIR)) { return "Images" }
            return ""
        }
    },
    methods: {
        close(){
            this.$emit('close_modal')
        }
    }
}
</script>

<style scoped lang="css">

h3{
    padding-bottom: 3vh;
}

section {
    color: #2c3e50;
    padding-left:2.5vw;
}

.upper {
    text-transform:capitalize;
}
 
</style>
