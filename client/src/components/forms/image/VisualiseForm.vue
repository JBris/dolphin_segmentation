<template>
    <section position="is-right">
        <b-image
            :src="`${imagePath}/${file.file}`"
            :lazy="true"
            class="image is-inline-block"
            position="is-right"
        ></b-image>
    </section>
</template>

<script>
export default {
    name: 'VisualiseForm',
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
    
}
</script>

<style scoped lang="css">
.image {
    width: 65vw;
    height: 65vh;
}

.group-header {
  color: #2c3e50;
  text-align: left;
}
</style>
