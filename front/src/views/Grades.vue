<template>
<div>
    <h1>That's the dashboard!</h1>
    <p>You should only get here if you're authenticated!</p>
    <p v-if="FullName">Your email address: {{ FullName }}</p>
</div>
</template>

<script>

export default {
    computed: {
        FullName() {
            return !this.$store.getters.user ? false : this.$store.getters.user.FullName
        }
    },
    created() {
        this.$store.dispatch('fetchUser')
    }
}
</script>

<style scoped>

</style>
