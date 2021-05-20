<template>
     <div class="modal-card ">
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <header class="modal-card-head">
            <h3>Create Task</h3>
        </header>
        <section class="modal-card-body">

    <div class="columns">
        <div class="column is-three-quarters">
            <b-field label="Name">
            <template #label>
                <h3 class="group-header">Name
                    <b-tooltip type="is-primary" position="is-right" label="The name of the task.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
            <b-input v-model="name" required></b-input>
        </b-field>
        </div>
    </div>

            <div class="columns">
                <div class="column is-centered">
                    <b-field grouped label="Modules">
                        <template #label>
                            <h3 class="group-header">Modules
                                <b-tooltip type="is-primary" position="is-right" label="The application module.">
                                    <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                                </b-tooltip>
                            </h3>
                        </template>
                        <div v-for="(props, key) in config.modules" :key="key">
                            <b-radio  v-if="props.enabled" v-model="module" :native-value="key" type="is-success">{{ props.name }}</b-radio>
                        </div>
                    </b-field>
                </div>
                <div class="column is-centered">
                    <b-field grouped label="Task">
                        <template #label>
                            <h3 class="group-header">Task
                                <b-tooltip type="is-primary" position="is-right" label="The image processing task type.">
                                    <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                                </b-tooltip>
                            </h3>
                        </template>
                        <div v-for="(props, key) in config.features" :key="key">
                            <b-radio  v-if="props.enabled" v-model="task" :native-value="key" type="is-success">{{ props.name }}</b-radio>
                        </div>
                    </b-field>
                </div>
            </div>


    <div class="columns">
        <div class="column is-centered">
            <b-field grouped label="Solver">
                    <template #label>
                        <h3 class="group-header">Solver
                            <b-tooltip type="is-primary" position="is-right" label="The image processing solver.">
                                <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                            </b-tooltip>
                        </h3>
                    </template>
                    <div v-for="(props, key) in config.solvers" :key="key">
                        <b-radio  v-if="props.enabled" v-model="solver" :native-value="key" type="is-success">{{ props.name }}</b-radio>
                    </div>
                </b-field>
        </div>
        <div class="column is-centered">
                <b-field grouped label="File Type">
                    <template #label>
                        <h3 class="group-header">File Type
                            <b-tooltip type="is-primary" position="is-right" label="The supplied file type.">
                                <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                            </b-tooltip>
                        </h3>
                    </template>
                    <div v-for="(value, key) in permittedFileInputs" :key="key">
                        <b-radio v-model="fileType" :native-value="key" type="is-success">{{ value  }}</b-radio>
                    </div>
                </b-field>
        </div>
    </div>


    <div class="columns">
        <div class="column is-three-quarters">
            <b-field label="File" horizontal>
                <template #label>
                    <h3 class="group-header">File
                        <b-tooltip type="is-primary" position="is-right" label="The file for image processing.">
                            <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                        </b-tooltip>
                    </h3>
                </template>
            <b-input v-model="file"></b-input>
            </b-field>
        </div>
        <div class="column">
            <b-button type="is-primary"
                v-on:click="selectFile"
                icon-left="file">
                Select File
            </b-button>
        </div>
    </div>

    <div class="columns">
        <div class="column is-three-quarters">
            <b-field label="Destination">
                <template #label>
                <h3 class="group-header">Destination
                    <b-tooltip type="is-primary" position="is-right" label="The extracted location of zip and tar files.">
                        <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                    </b-tooltip>
                </h3>
            </template>
        <b-input v-model="out" :disabled="fileType == 'dir' || fileType == 'image' || fileType == ''"></b-input>
        </b-field>
        </div>
    </div>

    <div class="columns">
        <div class="column is-three-quarters">
        <b-field label="Cache Duration">
            <template #label>
                <h3 class="group-header">Cache Duration
                <b-tooltip type="is-primary" position="is-right" label="The cache duration (in seconds) for the processed dataset">
                    <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
                </b-tooltip>
                </h3>
            </template>
        <b-numberinput min="1" max="999999" v-model="cacheDuration" type="is-success"></b-numberinput>
        </b-field>    
        
        </div>
    </div>

        <b-field>
            <b-checkbox v-model="autodownload" type="is-success">
                Autodownload Dataset
            </b-checkbox>
            <b-tooltip label="Automatically download the processed dataset upon task completion." position="is-right" type="is-primary">
                <b-icon
                :type="{'is-success' : true}"
                class="help-icon"
                icon="help-circle-outline"
                size="is-small">
            </b-icon>
            </b-tooltip>
        </b-field>

        </section>
        <footer class="modal-card-foot">
            <b-button type="is-success"
                v-on:click="confirm"
                icon-left="check">
                Confirm
            </b-button>
            <b-button type="is-danger"
            label="Cancel"
            @click="$parent.close()"
            icon-left="close">
          </b-button>
        </footer>
    </div>
</template>

<script>
import task from '@/api/file/task'
import FileSelectForm from '@/components/forms/FileSelectForm'

export default {
    name: 'TaskCreateForm',
    computed: {
        config() { return this.$store.state.config },
        permittedFileInputs() { return this.$store.state.permittedFileInputs }
    },
    data() {
        return {
            loading: false,
            error: false,
            name: "",
            task: "",
            module: "",
            solver: "",
            fileType: "",
            file: "",
            out: "",
            cacheDuration: 0,
            autodownload: true
        }
    },
    props: {
        taskListNames: {
            type: Array,
            required: true
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            this.task = Object.keys(this.config.features)[0]
            this.module = Object.keys(this.config.modules)[0]
            this.solver = Object.keys(this.config.solvers)[0]
            this.out = this.$store.state.OUT_DIR
            this.cacheDuration = this.config.cache_duration_default
            this.autodownload = this.config.autodownload_default
        },
        selectFile() {
            this.$buefy.modal.open({
                parent: this,
                component: FileSelectForm,
                hasModalCard: true,
                trapFocus: true,
                fullScreen: true,
                events: {
                    file_selected: file => {
                        this.file = file.file
                        this.fileType = file.type
                    }
                }
            })
        },
        async confirm() {
            if(!this.validate()) {return}

            const fileType = (this.fileType == "image")? "images" : this.fileType 
            this.loading = true
            await task.select(
                this.$store.state.SERVER_HOST, this.name, this.task, this.module, this.solver, fileType, this.file, this.out, this.cacheDuration, this.autodownload
            )
            this.loading = false
            this.$buefy.snackbar.open({message: `Task ${this.name} created`, duration: 2500, type: "is-success", position: "is-bottom"})
            this.$emit("update_file_list")
            this.$parent.close()
        },
        validate() {
            if(this.name == "") {
                this.$buefy.snackbar.open({message: 'Name field cannot be empty.', duration: 2500, type: "is-danger", position: "is-bottom"})
                return false
            }
            for(let task in this.taskListNames) {
                if(this.name.trim() !== task) { continue }
                this.$buefy.snackbar.open({message: `Duplicate task name. ${this.name.trim()} already exists.`, duration: 2500, type: "is-danger", position: "is-bottom"})
                return false
            }

            if(this.name == "") {
                this.$buefy.snackbar.open({message: 'Name field cannot be empty.', duration: 2500, type: "is-danger", position: "is-bottom"})
                return false
            }

            if(this.file == "") {
                this.$buefy.snackbar.open({message: 'File field cannot be empty.', duration: 2500, type: "is-danger", position: "is-bottom"})
                return false
            }
            if(this.fileType == "zip" && this.fileType == "tar" && this.out == "") {
                this.$buefy.snackbar.open({message: 'Destination field cannot be empty when selecting zip or tar files.', duration: 2500, type: "is-danger", position: "is-bottom"})
                return false
            }
            return true
        }
    }
}
</script>

<style scoped lang="css">
h3 {
    color: #2c3e50;
}

.modal-card {
    width: auto;
}

.modal-card-head {
    box-shadow: 0.02em 0.02em 1.5px grey;
    border: 0.02em solid hsl(171, 100%, 41%);
    background-color: white;
    height: 7.5vh;
    justify-content: center;
}

.modal-card-body{
    padding-left:5vw;
    padding-right:5vw;
}

.group-header {
  color: #2c3e50;
  text-align: left;
}
</style>