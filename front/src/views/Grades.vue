<template>
<div>
    <Header title="پایه مورد نظر خود را انتخاب کنید"></Header>
    <b-alert class="shakeError text-center mt-2" variant="success" :show="5">خوش آمدید</b-alert>
    <div class="btn-box">
        <router-link class="btn btn-warning" :class="{disabled:!grad.has_content}" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">
            <i class="far fa-lock icon" :class="{'d-none':grad.has_content}"></i>
            پایه {{grad.title}}
        </router-link>
        <button @click="onLogout" class="btn btn-outline-danger mx-auto mt-5 d-block w-25 btn-sm">خروج</button>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
import axios from 'axios'
export default {
    components: {
        Header
    },
    data() {
        return {
            grads: [],
        }
    },
    computed: {},
    methods: {
        onLogout() {
            this.$store.dispatch('logout')
        },
        getgrads() {
            const url = this.$route.path
            this.$store.commit('StoreCurrentUrl', url);
            axios.get('/courses')
                .then((res) => {
                    this.grads = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.getgrads();
    },
}
</script>

<style scoped>
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

.btn-warning {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
}

.btn-warning:focus,
.btn-warning.focus {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    box-shadow: none;
}
</style>
