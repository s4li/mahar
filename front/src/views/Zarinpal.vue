<template>
<div>
    wait a minute
    <p>{{this.$route.query.Status}}</p><p>{{this.$route.query.Authority}}</p>
</div>
</template>

<style lang="stylus" scoped>

</style>

<script>
import axios from 'axios'
export default {
    methods: {
        sendcallbackdata() {
            axios.get('/zarinpal-callback', {
                    params: {
                        Status: this.$route.query.Status,
                        Authority: this.$route.query.Authority,
                    }
                })
                .then(() => {})
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.sendcallbackdata();
    },
}
</script>
