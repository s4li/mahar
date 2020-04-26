<template>
<div>
    <Header title="لطفا پایه مورد نظر خود را انتخاب کنید"></Header>
    <div class="btn-box">
        <router-link :class="{disabled:!grad.unlock}" class="btn btn-warning" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">{{grad.title}}</router-link>
        <button @click="onLogout" class="logout">Logout</button>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
    components: {
        Header
    },
    //<p v-if="FullName">Your email address: {{ FullName }}</p>
    //"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    created() {
        this.$store.dispatch('fetchUser')
    },
    data() {
        return {
            grads: [{
                title: 'هفتم',
                id: 7,
                unlock:true
            }, {
                title: 'هشتم',
                id: 8,
                unlock:true
            }, {
                title: 'نهم',
                id: 9,
                unlock:true
            }, {
                title: 'دهم',
                id: 10,
                unlock:false
            }, {
                title: 'یازدهم',
                id: 11,
                unlock:false
            }, {
                title: 'دوازدهم',
                id: 12,
                unlock:false
            }]
        }
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
.btn-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    padding: 15px;
    margin-top: 40%;
}

.btn-box a {
    width: 45%;
    margin: 20px 0 0;
    padding: 8px;
}
</style>
