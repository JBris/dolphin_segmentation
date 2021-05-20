<template>
    <div class="modal-card">
        <header class="modal-card-head">
            <h3>{{file.name}}</h3>
        </header>
        <section v-if="file.type == 'image'" class="modal-card-body">
            <b-tabs position="is-left" vertical class="block" v-model="activeTab" :animated="false"> 
                <b-tab-item label="Visualise" icon="chart-line">
                    <VisualiseForm v-bind:file="file" v-bind:imagePath="imagePath" v-if="activeTab == 0" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Copy" icon="folder-swap">
                    <CopyForm v-bind:file="file" v-if="activeTab == 1" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Archive" icon="archive">
                    <ArchiveForm v-bind:file="file" v-if="activeTab == 2" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Delete" icon="delete">
                    <DeleteForm v-bind:file="file" v-if="activeTab == 3" v-on:update_file_list="updateFileList()" v-on:close_modal="$parent.close()"/>
                </b-tab-item>
            </b-tabs>
        </section>
        <section v-if="file.type == 'tar' || file.type == 'zip'" class="modal-card-body">
            <b-tabs position="is-left" vertical class="block" v-model="activeTab"> 
                <b-tab-item label="Copy" icon="folder-swap">
                    <CopyForm v-bind:file="file" v-if="activeTab == 0" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Extract" icon="folder-move">
                    <ExtractForm v-bind:file="file" v-if="activeTab == 1" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Delete" icon="delete">
                    <DeleteForm v-bind:file="file" v-if="activeTab == 2" v-on:update_file_list="updateFileList()" v-on:close_modal="$parent.close()"/>
                </b-tab-item>
            </b-tabs>
        </section>
        
        <section v-if="file.type == 'dir'" class="modal-card-body">
            <b-tabs position="is-left" vertical class="block" v-model="activeTab"> 
                <b-tab-item label="Copy" icon="folder-swap">
                    <CopyForm v-bind:file="file" v-if="activeTab == 0" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Archive" icon="archive">
                    <ArchiveForm v-bind:file="file" v-if="activeTab == 1" v-on:update_file_list="updateFileList()"/>
                </b-tab-item>
                <b-tab-item label="Delete" icon="delete">
                    <DeleteForm v-bind:file="file" v-if="activeTab == 2" v-on:update_file_list="updateFileList()" v-on:close_modal="$parent.close()"/>
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
import VisualiseForm from '@/components/forms/image/VisualiseForm'
import CopyForm from '@/components/forms/image/CopyForm'
import ArchiveForm from '@/components/forms/image/ArchiveForm'
import ExtractForm from '@/components/forms/image/ExtractForm'
import DeleteForm from '@/components/forms/image/DeleteForm'

export default {
    name: 'ImageForm',
    components:{
        VisualiseForm,
        CopyForm,
        ArchiveForm,
        ExtractForm,
        DeleteForm
    },
    props: {
        file: {
            type: Object,
            required: true
        },
        imagePath: {
            type: String,
            required: true
        }
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

