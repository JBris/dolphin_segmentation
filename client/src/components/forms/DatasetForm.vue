<template>
    <div class="modal-card">
        <header class="modal-card-head">
            <h3>{{file.name}}</h3>
        </header>
        <section class="modal-card-body">
            <b-tabs position="is-left" vertical class="block" v-model="activeTab"> 

                <b-tab-item label="Copy" icon="folder-swap">
                    <CopyForm v-bind:file="file" v-if="activeTab == 0" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>

                <b-tab-item label="Visualise" icon="chart-line">
                    <VisualiseForm v-bind:file="file" v-if="activeTab == 1" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>

                <b-tab-item label="Sort" icon="sort">
                    <SortForm v-bind:file="file" v-if="activeTab == 2" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>

                <b-tab-item label="Archive" icon="archive">
                    <ArchiveForm v-bind:file="file" v-if="activeTab == 3" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>

                <b-tab-item label="Delete" icon="delete">
                    <DeleteForm v-bind:file="file" v-if="activeTab == 4" v-on:update_file_list="updateFileList()" v-on:close_modal="$parent.close()"/>
                </b-tab-item>

            </b-tabs>
        </section>
        <footer class="modal-card-foot">
          <b-button type="is-primary"
            label="Close"
            @click="$parent.close()"
            icon-left="close">
          </b-button>
        </footer>
    </div>
</template>

<script>
import CopyForm from '@/components/forms/dataset/CopyForm'
import VisualiseForm from '@/components/forms/dataset/VisualiseForm'
import SortForm from '@/components/forms/dataset/SortForm'
import ArchiveForm from '@/components/forms/dataset/ArchiveForm'
import DeleteForm from '@/components/forms/dataset/DeleteForm'

export default {
    name: 'DatasetForm',
    components:{
        CopyForm,
        VisualiseForm,
        SortForm,
        ArchiveForm,
        DeleteForm
    },
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            activeTab: 0,
        }
    },
    methods: {
        updateFileList() {
            this.$emit("update_file_list")
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
}

</style>

