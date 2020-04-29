<template>
<div>

</div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            Courses: [],
            CoursesType: this.$route.params.Type,
        }
    },
    methods: {
        getCourses() {
            axios.get('/courses')
                .then((res) => {
                    this.Courses = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.getCourses();
    },
}
</script>

<style lang="css">

</style>
