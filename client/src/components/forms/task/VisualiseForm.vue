<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <div id="dataset-visualisation"></div>
    </section>
</template>

<script>
import file from '@/api/file/file'

export default {
    name: 'VisualiseForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false,
            plot: {}
        }
    },
    mounted() {
        this.loadPlot()
    },
    methods: {
        async loadPlot() {
            this.loading = true
            this.plot = await file.visualise(this.$store.state.SERVER_HOST, this.file.file, this.file.type, this.$store.state.visualisationMethod)
            window.Bokeh.embed.embed_item(this.plot, "dataset-visualisation")
            this.loading = false
        },
    }
}
</script>

<style scoped lang="css">
.group-header {
  color: #2c3e50;
  text-align: left;
}
</style>
