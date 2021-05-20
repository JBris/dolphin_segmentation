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

        <b-field label="Format" type="is-success">
              <template #label>
                <h3 class="group-header">Format
                    <b-tooltip type="is-primary" position="is-right" label="The format of the archived file.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
            <b-autocomplete v-model="currentFormat" @select="onFormatSelect" open-on-focus :data="permittedFileFormats">
            </b-autocomplete>
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
    name: 'ArchiveForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    computed: {
        permittedFileFormats() { return this.$store.state.permittedArchiveFormats }
    },
    data() {
        return {
            loading: false,
            destination: "",
            currentFormat: "",
        }
    },
    mounted() {
        this.currentFormat = this.permittedFileFormats[0]
        this.destination = `${this.$store.state.OUT_DIR}/${this.file.file.substring(this.file.file.lastIndexOf("/") + 1)}`
        this.onFormatSelect(this.currentFormat)
    },
    methods: {
        onFormatSelect(format) {
            const ext = (format == "zip")? format: "tar.gz"
            let newDest, dest = this.destination 
            
            while(dest != "") {
                newDest = dest
                dest = dest.split('.').slice(0, -1).join('.')
            }
            this.destination = `${newDest}.${ext}`
        },
        async confirm() { 
            this.loading = true
            await file.archive(this.$store.state.SERVER_HOST, "archive", this.currentFormat, this.file.file, this.destination )
            this.loading = false
            this.$buefy.snackbar.open({message: `File archived to ${this.destination}`, duration: 2500, type: "is-success", position: "is-bottom"})
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
