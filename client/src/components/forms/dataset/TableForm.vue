<template>
    <section>
    <b-loading :is-full-page="true" v-model="loading" :can-cancel="true"></b-loading>
        <section>
            <b-table
                :data="data"
                :paginated="true"
                :per-page="perPage"
                :current-page.sync="currentPage"
                :pagination-simple="false"
                :pagination-position="paginationPosition"
                default-sort-direction="asc"
                :pagination-rounded="false"
                sort-icon="arrow-up"
                sort-icon-size="is-small"
                default-sort="index"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
                debounce-search="250"
                :sticky-header="true">

                <b-table-column field="index" label="Index" width="40" sortable numeric v-slot="props">
                    {{ props.row.index }}
                </b-table-column>

                <b-table-column field="name" label="Name" sortable v-slot="props" searchable>
                    {{ props.row.name }}
                </b-table-column>

                <b-table-column field="file" label="File" sortable v-slot="props" searchable>
                    {{ props.row.file }}
                </b-table-column>

                <b-table-column field="x" label="x" sortable numeric v-slot="props">
                    {{ props.row.x }}
                </b-table-column>

                <b-table-column field="y" label="y" sortable numeric v-slot="props">
                    {{ props.row.y }}
                </b-table-column>

                <b-table-column field="class" label="Class" sortable v-slot="props" searchable>
                    {{ props.row.class }}
                </b-table-column>

                <b-table-column field="probability" label="Probability" sortable v-slot="props">
                    {{ props.row.probability }}
                </b-table-column>

                <b-table-column field="outlier" label="Outlier" sortable v-slot="props">
                    {{ props.row.outlier }}
                </b-table-column>
            </b-table>
        </section>
    </section>
</template>

<script>
import file from '@/api/file/file'

export default {
    name: 'TableForm',
    props: {
        file: {
            type: Object,
            required: true
        },
    },
    data() {
        return {
            loading: false,
            data: [],
            currentPage: 1,
            perPage: 20,
            paginationPosition: 'bottom',
        }
    },
    mounted() {
        this.getTable()
    },
    methods: {
        async getTable() {
            this.loading = true
            this.data = await file.viewDataset(this.$store.state.SERVER_HOST, this.file.file, this.file.type)
            this.loading = false
        } 
    }
}
</script>
