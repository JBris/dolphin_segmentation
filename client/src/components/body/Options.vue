<template>
  <section>
    <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>

    <section>
      <b-field grouped label="Modules">
        <template #label>
          <h3 class="group-header">Modules
            <b-tooltip type="is-primary" label="Enable and disable application modules.">
              <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
            </b-tooltip>
          </h3>
        </template>
      <div v-for="(props, key) in config.modules" :key="key">
        <b-checkbox v-if="props.editable" v-model="props.enabled" type="is-success">{{ props.name }}</b-checkbox>
        <b-checkbox v-else :value="Boolean(props.enabled)" type="is-success" disabled>{{ props.name }}</b-checkbox>
      </div>
    </b-field>
  </section>
    
    <br/>

    <section>
      <b-field grouped label="Features">
        <template #label>
          <h3 class="group-header">Features
            <b-tooltip type="is-primary" label="Enable and disable different features such as image classification and identification.">
              <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
            </b-tooltip>
          </h3>
        </template>
        <div v-for="(props, key) in config.features" :key="key">
          <b-checkbox v-if="props.editable" v-model="props.enabled" type="is-success">{{ props.name }}</b-checkbox>
          <b-checkbox v-else :value="Boolean(props.enabled)" type="is-success" disabled>{{ props.name }}</b-checkbox>
        </div>
        </b-field>
    </section>
    
    <br/>
    
    <section>
      <b-field grouped label="Solvers">
        <template #label>
          <h3 class="group-header">Solvers
            <b-tooltip type="is-primary" label="Enable and disable image processing solvers for tasks such as identification and classification.">
              <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
            </b-tooltip>
          </h3>
      </template>
      <div v-for="(props, key) in config.solvers" :key="key">
        <b-checkbox v-if="props.editable" v-model="props.enabled" type="is-success">{{ props.name }}</b-checkbox>
        <b-checkbox v-else :value="Boolean(props.enabled)" type="is-success" disabled>{{ props.name }}</b-checkbox>
      </div>
      </b-field>
    </section>
    
    <br/>

    <section>
      <b-field horizontal label="Cache Duration">
      <template #label>
        <h3 class="group-header">Cache Duration
          <b-tooltip type="is-primary" label="The default cache duration (in seconds) for processed datasets">
            <b-icon icon="help-circle-outline" type="is-success" size="is-small"></b-icon>
          </b-tooltip>
        </h3>
      </template>
      <b-numberinput min="1" max="999999" v-model="config.cache_duration_default"  type="is-success"></b-numberinput>
    </b-field>
    </section>

    <br/>

    <section>
      <b-field>
        <b-checkbox v-model="config.autodownload_default" type="is-success">
            Autodownload Datasets
        </b-checkbox>
        <b-tooltip label="Automatically download datasets upon task completion." position="is-right" type="is-primary">
            <b-icon
            :type="{'is-success' : true}"
            class="help-icon"
            icon="help-circle-outline"
            size="is-small">
          </b-icon>
        </b-tooltip>
      </b-field>

      <b-field>
        <b-checkbox v-model="config.hide_tasks" type="is-success">
            Hide Task Dashboard
        </b-checkbox>
        <b-tooltip label="Hide the task dashboard option in the header bar." position="is-right" type="is-primary">
          <b-icon
            :type="{'is-success' : true}"
            class="help-icon"
            icon="help-circle-outline"
            size="is-small">
          </b-icon>
        </b-tooltip>
      </b-field>

      <b-field>
        <b-checkbox v-model="config.hide_notebooks" type="is-success">
             Hide Notebooks
        </b-checkbox>
        <b-tooltip label="Hide the notebooks option in the header bar." position="is-right" type="is-primary">
          <b-icon
            :type="{'is-success' : true}"
            class="help-icon"
            icon="help-circle-outline"
            size="is-small">
          </b-icon>
        </b-tooltip>
      </b-field>

      <b-field>
        <b-checkbox v-model="config.hide_containers" type="is-success">
             Hide Containers
        </b-checkbox>
        <b-tooltip label="Hide the containers option in the header bar." position="is-right" type="is-primary">
          <b-icon
            :type="{'is-success' : true}"
            class="help-icon"
            icon="help-circle-outline"
            size="is-small">
          </b-icon>
        </b-tooltip>
      </b-field>
    </section>

    <br/>

    <section>
      <div class="buttons">
        <b-button type="is-success"
          v-on:click="save"
          icon-left="check">
            Save
          </b-button>

          <b-button type="is-danger"
            v-on:click="cancel"
            icon-left="close">
              Cancel
          </b-button>

          <b-button type="is-primary"
            v-on:click="reset"
            icon-left="refresh">
              Reset
          </b-button>

      </div>
    </section>
  </section>
</template>

<script>
import config from '../../config'

  export default {
    name: 'Options',
    data() {
        return {
          loading: true,
          error: false,
        }
      },
    computed: {
        config: {
            get() {
                return this.$store.state.config
            },
            set(config) {
              this.$store.commit('setConfig', config)
            }
        },
    },
    mounted() {
      this.getConfig()
    },
    destroyed () {
    this.getConfig()
  },
    methods: {
      async getConfig() {
        this.loading = true
        try {
            const configuration = await config.get(this.$store.state.SERVER_HOST)
            this.config = configuration
            this.error = false
        } catch (e) { this.error = true }
        this.loading = false
      },
      async save() {
        this.loading = true
        const configuration = await config.confirm(this.$store.state.SERVER_HOST, this.config)
        this.config = configuration
        this.loading = false
        this.$buefy.snackbar.open({message: 'Saved options.', duration: 2500, type: "is-success", position: "is-bottom"})
      },
      cancel() {
        this.loading = true
        setTimeout(() => {
          this.loading = false
          this.$router.push("/")
        }, 250);
      },
      async reset() {
        this.loading = true
        const configuration = await config.reset(this.$store.state.SERVER_HOST)
        this.config = configuration
        this.loading = false
        this.$buefy.snackbar.open({message: 'Options reset.', duration: 2500, type: "is-success", position: "is-bottom"})
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