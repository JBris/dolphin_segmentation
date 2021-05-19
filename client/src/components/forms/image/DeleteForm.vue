<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <h3>Please confirm file deletion: {{file.file}}</h3>
        <br/>
        <section>
            <div class="buttons">
                <b-button type="is-danger"
                    v-on:click="confirm"
                    icon-left="cancel">
                    Confirm
                </b-button>
            </div>
        </section>
    </section>
</template>

<script>
import file from '@/api/file/file'

export default {
    name: 'DeleteForm',
    props: {
        file: {
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
            await file.delete(this.$store.state.SERVER_HOST, [ this.file.file ])
            this.loading = false
            this.$buefy.snackbar.open({message: `Deleted ${this.file.file}`, duration: 2500, type: "is-success", position: "is-bottom"})
            this.$emit("update_file_list")
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
