<template>
<div>
    <h1>That's the dashboard!</h1>
    <p v-if="auth" >You should only get here if you're authenticated!</p>
    <p v-if="FullName">Your email address: {{ FullName }}</p>
    <button @click="onLogout" class="logout">Logout</button>
</div>
</template>

<script>
export default {
    created() {
        this.$store.dispatch('fetchUser')
    },
    computed: {
        FullName() {
            return !this.$store.getters.user ? false : this.$store.getters.user.FullName
        },
        auth() {
            return this.$store.getters.isAuthenticated
        }
    },
    methods: {
        onLogout() {
            this.$store.dispatch('logout')
        }
    }
}
</script>

<style scoped>

</style>
