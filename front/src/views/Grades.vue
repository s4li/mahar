<template>
<div>
    <Header title="پایه مورد نظر خود را انتخاب کنید"></Header>
    <b-alert class="shakeError text-center mt-2" variant="success" :show="5">خوش آمدید</b-alert>
    <div class="btn-box">
            <router-link class="btn btn-warning" :class="{disabled:grad.has_content}" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">
            <!--<i class="far fa-lock icon" :class="{'d-none':grad.unlock}"></i>-->
            پایه {{grad.title}}
        </router-link>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
import axios from 'axios'
export default {
    //<button @click="onLogout" class="logout">Logout</button>
    //<p v-if="FullName">Your email address: {{ FullName }}</p>
    components: {
        Header
    },
    data() {
        return {
            grads: []
        }
    },
    computed: {
        //FullName() {
        //    return !this.$store.getters.user ? false : this.$store.getters.user.FullName
        //},
        //auth() {
        //    return this.$store.getters.isAuthenticated
        //}
    },
    methods: {
        //onLogout() {
        //    this.$store.dispatch('logout')
        //},
        getgrads() {
            const path = '/courses';
            axios.get(path)
                .then((res) => {
                    this.grads = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.$store.dispatch('fetchUser');
        this.getgrads();
    },
}
</script>

<style>
.btn-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    padding: 15px;
    margin-top: 30%;
    background-color: #f8f9fa99;
    border-radius: 4px;
}

.btn-box a {
    width: 45%;
    margin: 20px 0 0;
    padding: 8px;
}
</style>
