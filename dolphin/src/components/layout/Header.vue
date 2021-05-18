<template>
    <div class="container">
        <b-navbar :fixed-top="true" :centered="true" :shadow="true" :spaced="true">
            <template #start>
                <b-navbar-item tag="router-link" :to="{ name: 'Home' }">
                    <b-icon
                        pack="fas"
                        :type="{'is-success' : true}"
                        class="header-icon"
                        icon="home">
                    </b-icon>
                    Home
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ name: 'Images' }">
                    Images
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ name: 'Datasets' }">
                    Datasets
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ name: 'Outputs' }">
                    Outputs
                </b-navbar-item>
                <b-navbar-item tag="router-link" :to="{ name: 'Pipelines' }">
                    Pipelines
                </b-navbar-item>
                <b-navbar-item v-if="!config.hide_tasks" :href="tasksUrl" target="_blank" rel="noopener noreferrer">
                    Tasks
                </b-navbar-item>
                <b-navbar-item v-if="!config.hide_notebooks" :href="notebooksUrl" target="_blank" rel="noopener noreferrer">
                    Notebooks
                </b-navbar-item>
            </template>
            <template #end>
                <b-navbar-item tag="router-link" :to="{ name: 'Options' }">
                    <b-icon
                        pack="fas"
                        :type="{'is-success' : true}"
                        class="header-icon"
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
        config: {
            get() {
                return this.$store.state.config
            }
        },
        tasksUrl: {
            get() {
                return this.$store.state.TASKS_HOST
            }
        },
        notebooksUrl: {
            get() {
                return this.$store.state.NOTEBOOK_HOST
            }
        },
    }
}
</script>

<style scoped lang="css">
.navbar {
    box-shadow: 0.025em 0.025em 2.5px grey;
    border: 0.025em solid hsl(171, 100%, 41%);
}

.header-icon {
    padding-left: 1.5vw;
    padding-right: 1.5vw;
}
</style>