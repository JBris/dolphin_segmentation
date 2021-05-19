<template>
  <content>
    <section class="image-dir-path level-left">
      <a v-for="(dir, index) in datasetDirList" :key=index @click="getFileList(joinDatasetDirList(datasetDirList, index))">
        /{{dir}}
      </a>         
    </section>
    <div class="tile is-ancestor">
      <div class="tile is-3 is-vertical is-parent">
        <div class="tile is-child">
          <b-field>
              <b-autocomplete
                  v-model="fileName"
                  group-field="type"
                  field="file"
                  icon="magnify"
                  @select="option => selectFile(option)"
                  :data="filteredFiles">
                  <template slot-scope="props">
                    <div class="media">
                        <div class="media-left">
                            <img width="32" :src="require(`@/assets/images/${props.option.type}.png`)">
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
      <div class="tile is-vertical is-parent">
        <div class="tile is-child">
          <section>
            <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
            <p v-if="!this.fileList.length && !this.loading">No datasets currently available.</p>
            <div v-else>
            <section class="image-dir-path">
              <div class="columns is-multiline">
                <div v-for="(file, index) in fileList" :key=index class="column is-one-fifth  has-text-centered">
                  <DatasetItem v-bind:file="file" v-bind:datasetPath="datasetPath" v-on:dir_selected="changeDir(file)" v-on:file_selected="selectFile(file)" />
                </div>
              </div>  
              </section>    
            </div>
          </section>          
        </div>
      </div>
    </div>
  </content>
</template>

<script>
import collection from '@/api/file/collection'
import { DATASETS } from '@/api/endpoints'
import DatasetItem from '@/components/body/DatasetItem'

export default {
  name: 'ImageList',
  components: {
    DatasetItem,
  },
  data() {
    return {
      loading: true,
      error: false,
      datasetDir: "",
      fileName: "",
      selectedFile: null,
      fileList: [],
    }
  },
  computed: {
    datasetPath() {
      return `${this.$store.state.SERVER_HOST}/${DATASETS}`
    },
    datasetDirList() {
      return this.datasetDir.split("/").filter(ele => ele != "")
    },
    filteredFiles() {
      return this.fileList
      .filter(file => file.type != "dir")
      .filter(file => file.file.toLowerCase().indexOf(this.fileName.toLowerCase()) >= 0)
    }
  },
  mounted() {
    this.getFileList()
  },
  methods: {
    async getFileList(datasetDir = this.$store.state.DATASET_DIR) {
      this.loading = true
      try {
        this.datasetDir = datasetDir
        console.log(this.datasetDir )
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
      this.fileName = file.file
      this.selectedFile = file
      this.$buefy.toast.open({
        duration: 2000,
        message: file.file,
        position: 'is-bottom',
        type: 'is-success'
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



