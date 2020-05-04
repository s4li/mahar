<template>
<div>
    <Header title="پایه مورد نظر خود را انتخاب کنید"></Header>
    <transition name="fadeIn" appear>
        <div class="parent">
            <div class="btn-box" v-if="show">
                <router-link class="btn btn-warning" :class="{disabled:!grad.has_content}" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">
                    <i class="far fa-lock icon" :class="{'d-none':grad.has_content}"></i>
                    پایه {{grad.title}}
                </router-link>
                <button @click="onLogout" class="btn btn-outline-danger mx-auto mt-3 d-block w-25 btn-sm shadow">خروج</button>
            </div>
        </div>
    </transition>
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
            show: true,
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
                    console.log(res)
                    //res.status: 200
                    //res.statusText: "OK"

                })
                .catch((error) => {
                    console.log(error);
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
    background-color: #ffffffcc;
    border-radius: 4px;
    box-shadow: 0 3px 10px #cccccc;
}

.btn-box a {
    width: 45%;
    margin: 10px 0 10px;
    padding: 8px;
}

.btn-warning {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.btn-warning:focus,
.btn-warning.focus {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    box-shadow: none;
}
</style>
