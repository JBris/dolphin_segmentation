<template>
    <div class="container">
        <b-navbar fixed-top=true centered=true shadow=true spaced=true>
            <template #start>
                <b-navbar-item href="#">
                    Images
                </b-navbar-item>
                <b-navbar-item href="#">
                    Datasets
                </b-navbar-item>
                <b-navbar-item href="#">
                    Workflows
                </b-navbar-item>
                <b-navbar-item :href="tasksUrl" target="_blank" rel="noopener noreferrer">
                    Tasks
                </b-navbar-item>
                <b-navbar-item :href="notebooksUrl" target="_blank" rel="noopener noreferrer">
                    Notebooks
                </b-navbar-item>
            </template>
            <template #end>
                <b-navbar-item href="#">
                <b-icon
                    pack="fas"
                    :type="{'is-success' : true}"
                    class="options-icon"
                    icon="cog">
                </b-icon>
                    Options
                </b-navbar-item>
            </template>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name:"Header",
    computed: {
        tasksUrl: {
            get() {
                return this.$store.state.config["TASKS_HOST"]
            }
        },
        notebooksUrl: {
            get() {
                return this.$store.state.config["NOTEBOOK_HOST"]
            }
        }
    }
}
</script>

<style scoped lang="css">
.navbar {
    box-shadow: 0.025em 0.025em 2.5px grey;
    border: 0.025em solid hsl(171, 100%, 41%);
}

.options-icon {
    padding-left: 2.5vw;
    padding-right: 2.5vw;
}

</style>