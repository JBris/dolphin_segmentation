<template>
    <content>
        <div class="columns">
            <div class="column">
                <section class="image-dir-path level-left">
                    <a v-for="(dir, index) in imageDirList" :key=index
                        @click="getFileList(joinImageDirList(imageDirList, index))">
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
        <hr>
        <section>
            <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
            <p v-if="!this.fileList.length && !this.loading">No datasets currently available.</p>
            <div v-else>
                <section class="image-dir-path">
                    <div class="columns is-multiline">
                        <div v-for="(file, index) in paginatedItems" :key=index
                            class="column is-one-fifth  has-text-centered">
                              <ImageItem v-bind:file="file" v-bind:imagePath="imagePath" v-on:dir_selected="changeDir(file)"  v-on:file_selected="selectFile(file)"/>
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
import { IMAGE, IMAGES } from '@/api/endpoints'
import ImageItem from '@/components/body/ImageItem'
import ImageForm from '@/components/forms/ImageForm'

export default {
  name: 'ImageList',
  components: {
    ImageItem
  },
  data() {
    return {
      loading: true,
      error: false,
      imageDir: "",
      fileName: "",
      fileList: [],
      current: 1,
      perPage: 20,
    }
  },
  computed: {
    imagePath() {
        return `${this.$store.state.SERVER_HOST}/${IMAGE}`
    },
    imageDirList() {
      return this.imageDir.split("/").filter(ele => ele != "")
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
  },
  mounted() {
    this.getFileList()
  },
  methods: {
    async getFileList(imageDir = this.$store.state.OUT_DIR, loading = true) {
      this.loading = loading
      try {
        this.imageDir = imageDir
        this.fileList = await collection.getAll(this.$store.state.SERVER_HOST, IMAGES, this.imageDir)
        this.error = false
      } catch (e) { this.error = true }
      this.loading = false
    },
    async changeDir(file) {
      return this.getFileList(file.file)
    },
    joinImageDirList(imageDirList, index) {
      return `/${imageDirList.slice(0, index + 1).join("/")}`
    },
    selectFile(file) {
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
          update_file_list: () => this.getFileList(this.$store.state.OUT_DIR, false)
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