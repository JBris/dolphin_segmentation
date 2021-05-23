<template>
    <content>
        <div class="columns">
            <div class="column">
                <section class="image-dir-path level-left">
                    <a v-for="(dir, index) in datasetDirList" :key=index
                        @click="getFileList(joinDatasetDirList(datasetDirList, index))">
                        /{{dir}}
                    </a>
                </section>
            </div>
            <div class="column is-half">
                <b-field>
                    <b-autocomplete v-model="fileName" group-field="type" field="name" icon="magnify"
                        @select="option => selectFile(option)" :data="filteredFiles">
                        <template slot-scope="props">
                            <div class="media">
                                <div class="media-left">
                                    <img width="32" v-if="props.option.type != 'dir'" :src="require(`@/assets/images/${props.option.type}.png`)" lazy>
                                    <img width="32" v-if="props.option.type == 'dir'" :src="require('@/assets/images/folder.png')" lazy>
                                </div>
                                <div class="media-content">
                                    {{ props.option.name}}
                                </div>
                            </div>
                        </template>
                    </b-autocomplete>
                </b-field>
            </div>
        </div>
        <hr>
        <section>
            <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
            <p v-if="!this.fileList.length && !this.loading">No datasets currently available.</p>
            <div v-else>
                <section class="image-dir-path">
                    <div class="columns is-multiline">
                        <div v-for="(file, index) in paginatedItems" :key=index
                            class="column is-one-fifth  has-text-centered">
                            <DatasetItem v-bind:file="file" v-if="file.type != 'dir'" 
                                v-on:dir_selected="changeDir(file)" v-on:file_selected="selectFile(file)" />
                            <ImageItem v-bind:file="file" v-bind:imagePath="imagePath" v-if="file.type == 'dir'" 
                                v-on:dir_selected="changeDir(file)" v-on:file_selected="selectDir(file)" />
                        </div>
                    </div>
                </section>
            </div>
        </section>
        <hr>
        <b-pagination
            :total="itemTotal"
            v-model="current"
            :per-page="perPage"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page">
        </b-pagination>
    </content>
</template>

<script>
import collection from '@/api/file/collection'
import { DATASETS, IMAGE } from '@/api/endpoints'
import DatasetItem from '@/components/body/DatasetItem'
import DatasetForm from '@/components/forms/DatasetForm'
import ImageItem from '@/components/body/ImageItem'
import ImageForm from '@/components/forms/ImageForm'

export default {
  name: 'Datasets',
  components: {
    DatasetItem,
    ImageItem
  },
  data() {
    return {
      loading: true,
      error: false,
      datasetDir: "",
      fileName: "",
      fileList: [],
      current: 1,
      perPage: 20,
    }
  },
  props:{
    path: {
      type: String,
      required: false,
      default: ''
    }
  },
  computed: {
    datasetDirList() {
      return this.datasetDir.split("/").filter(ele => ele != "")
    },
    filteredFiles() {
      return this.fileList
      .filter(file => file.name.toLowerCase().indexOf(this.fileName.toLowerCase()) >= 0)
    },
    paginatedItems() {
      let pageNumber = this.current-1
      return this.fileList.slice(pageNumber * this.perPage, (pageNumber + 1) * this.perPage);  
    },
    itemTotal() {
      return this.fileList.length
    },
    imagePath() {
      return `${this.$store.state.SERVER_HOST}/${IMAGE}`
    },
  },
  mounted() {
    if(this.path != "") { this.getFileList(this.path) }
    else{ this.getFileList() }
  },
  methods: {
    async getFileList(datasetDir = this.$store.state.DATASET_DIR, loading = true) {
      this.loading = loading
      try {
        this.datasetDir = datasetDir
        this.fileList = await collection.getAll(this.$store.state.SERVER_HOST, DATASETS, this.datasetDir)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    async changeDir(file) {
      return this.getFileList(file.file)
    },
    joinDatasetDirList(datasetDirList, index) {
      return `/${datasetDirList.slice(0, index + 1).join("/")}`
    },
    selectFile(file) {
      if(file == null) return;
      if(file.type == "dir"){ return this.selectDir(file) }
      this.$buefy.modal.open({
        parent: this,
        component: DatasetForm,
        props: {
          file
        },
        hasModalCard: true,
        trapFocus: true,
        fullScreen: true,
        events: {
          update_file_list: () => this.getFileList(this.$store.state.DATASET_DIR, false)
        }
      })
    },
    selectDir(file) {
      if(file == null) return;
      this.$buefy.modal.open({
        parent: this,
        component: ImageForm,
        props: {
          file,
          imagePath: this.imagePath
        },
        hasModalCard: true,
        trapFocus: true,
        fullScreen: true,
        events: {
          update_file_list: () => this.getFileList(this.$store.state.DATASET_DIR, false)
        }
      })
    }
  }
}
</script>

<style scoped lang="css">
  .image-dir-path {
    padding-top: 1.5vh;
    padding-bottom: 1.5vh;
  }
</style>



