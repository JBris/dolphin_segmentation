<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <b-field label="Destination">
              <template #label>
                <h3 class="group-header">Destination
                    <b-tooltip type="is-primary" position="is-right" label="The destination of the copied file.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
            <b-input v-model="destination"></b-input>
        </b-field>
        <br/>
        <section>
            <div class="buttons">
                <b-button type="is-success"
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

export default {
    name: 'SortForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false,
            destination: ""
        }
    },
    mounted() {
        const fileName = this.file.file.substring(this.file.file.lastIndexOf("/") + 1)
        this.destination = `${this.$store.state.OUT_DIR}/${fileName.split('.').slice(0, -1).join('.')}`
    },
    methods: {
        async confirm() {
            this.loading = true
            await file.sort(this.$store.state.SERVER_HOST, this.file.file, this.file.type, this.destination)
            this.loading = false
            this.$buefy.snackbar.open({message: `Files sorted to ${this.destination}`, duration: 2500, type: "is-success", position: "is-bottom"})
            this.$emit("update_file_list")
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
