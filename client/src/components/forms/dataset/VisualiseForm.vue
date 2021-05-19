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

        <b-field label="Format" type="is-success">
              <template #label>
                <h3 class="group-header">Format
                    <b-tooltip type="is-primary" position="is-right" label="The format of the copied file.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
            <b-autocomplete v-model="currentFormat" @select="onSelect" open-on-focus :data="permittedFileFormats">
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
    name: 'VisualiseForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false
        }
    },
    mounted() {
        this.currentFormat = this.permittedFileFormats[0]
        this.destination = `${this.file.file.split('.').slice(0, -1).join('.')}_copy.${this.currentFormat}`
    },
    methods: {
        onSelect(format) {
            this.destination = `${this.destination.split('.').slice(0, -1).join('.')}.${format}`
        },
        async confirm() {
            this.loading = true
            await file.copy(this.$store.state.SERVER_HOST, this.file.file, this.file.type, this.destination, this.currentFormat )
            this.loading = false
            this.$buefy.snackbar.open({message: `File copied to ${this.destination}`, duration: 2500, type: "is-success", position: "is-bottom"})
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
