<template>
     <div class="modal-card ">
        <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <header class="modal-card-head">
            <h3>Select File</h3>
        </header>
        <section class="modal-card-body">
            <div class="columns">
                <div class="column">
                    <section class="image-dir-path level-left">
                        <a v-for="(dir, index) in systemDirList" :key=index
                            @click="getFileList(joinSystemDirList(systemDirList, index))">
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
                                  <img width="32" v-if="props.option.type == 'image'" :src="`${imagePath}/${props.option.file}`" lazy>
                                  <img width="32" v-if="props.option.type == 'dir'" :src="require('@/assets/images/folder.png')" lazy>
                                  <img width="32" v-if="props.option.type == 'tar'" :src="require('@/assets/images/archive.png')" lazy>
                                  <img width="32" v-if="props.option.type == 'zip'" :src="require('@/assets/images/archive.png')" lazy>
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
            <section>
                <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
                <p v-if="!this.fileList.length && !this.loading">No datasets currently available.</p>
                <div v-else>
                    <section class="image-dir-path">
                        <div class="columns is-multiline">
                            <div v-for="(file, index) in fileList" :key=index
                                class="column is-one-fifth  has-text-centered">
                                <ImageItem v-bind:file="file" v-bind:imagePath="imagePath" v-on:dir_selected="changeDir(file)"  v-on:file_selected="selectFile(file)"/>
                            </div>
                        </div>
                    </section>
                </div>
            </section>        
        </section>
        <footer class="modal-card-foot">
            <b-button type="is-danger"
            label="Cancel"
            @click="$parent.close()"
            icon-left="close">
          </b-button>
        </footer>
    </div>
</template>

<script>
import collection from '@/api/file/collection'
import { IMAGE, IMAGES } from '@/api/endpoints'
import ImageItem from '@/components/body/ImageItem'

export default {
  name: 'FileSelectForm',
  components: {
    ImageItem
  },
  data() {
    return {
      loading: true,
      error: false,
      systemDir: "",
      fileName: "",
      fileList: [],
    }
  },
  computed: {
    imagePath() {
        return `${this.$store.state.SERVER_HOST}/${IMAGE}`
    },
    systemDirList() {
      return this.systemDir.split("/").filter(ele => ele != "")
    },
    filteredFiles() {
      return this.fileList
      .filter(file => file.name.toLowerCase().indexOf(this.fileName.toLowerCase()) >= 0)
    }
  },
  mounted() {
    this.getFileList()
  },
  methods: {
    async getFileList(systemDir = this.$store.state.BASE_DIR, loading = true) {
      this.loading = loading
      try {
        this.systemDir = systemDir
        this.fileList = await collection.getAll(this.$store.state.SERVER_HOST, IMAGES, this.systemDir)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    async changeDir(file) {
      return this.getFileList(file.file)
    },
    joinSystemDirList(systemDirList, index) {
      return `/${systemDirList.slice(0, index + 1).join("/")}`
    },
    selectFile(file) {
      if(file == null) return;
      this.$emit("file_selected", file)
      this.$parent.close()
    },
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

.image-dir-path {
  padding-top: 1.5vh;
  padding-bottom: 1.5vh;
}
</style>
