<template>
    <section>
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <b-field label="Destination">
              <template #label>
                <h3 class="group-header">Destination
                    <b-tooltip type="is-primary" position="is-right" label="The destination of the file.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
            <b-input v-model="destination"></b-input>
        </b-field>
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
    name: 'ExtractForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false,
            destination: "",
        }
    },
    mounted() {
        let dest = `${this.$store.state.OUT_DIR}/${this.file.file.substring(this.file.file.lastIndexOf("/") + 1)}`
        if(this.file.type == "zip") { dest = dest.replace(new RegExp('.zip' + '$'), '') } 
        if(this.file.type == "tar") { 
            dest = dest.replace(new RegExp('.gz' + '$'), '') 
            dest = dest.replace(new RegExp('.tar' + '$'), '') 
        }
        this.destination = dest
    },
    methods: {
        async confirm() { 
            this.loading = true
            await file.archive(this.$store.state.SERVER_HOST, "extract", this.file.type, this.file.file, this.destination )
            this.loading = false
            this.$buefy.snackbar.open({message: `File extracted to ${this.destination}`, duration: 2500, type: "is-success", position: "is-bottom"})
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
