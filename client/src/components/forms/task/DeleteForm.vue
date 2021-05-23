<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <h3>Please confirm task deletion: {{task.name}}</h3>
        <br/>
        <section>
            <div class="buttons">
                <b-button type="is-danger"
                    v-on:click="confirm"
                    icon-left="check">
                    Confirm
                </b-button>
            </div>
        </section>
    </section>
</template>

<script>
import file from '@/api/file/file'
import task from '@/api/file/task'

export default {
    name: 'DeleteForm',
    props: {
        task: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false,
        }
    },
    methods: {
        async confirm() {
            this.loading = true
            await task.cancel(this.$store.state.SERVER_HOST, this.task.id)
            await file.delete(this.$store.state.SERVER_HOST, [ this.task.file ])
            this.loading = false
            this.$buefy.snackbar.open({message: `Deleted ${this.task.name}`, duration: 2500, type: "is-success", position: "is-bottom"})
            this.$emit("update_task_list")
            this.$emit("close_modal")
        }
    }
}
</script>

<style scoped lang="css">
.group-header {
  color: #2c3e50;
  text-align: left;
}
</style>
