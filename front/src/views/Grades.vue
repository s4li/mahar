<template>
<div>
    <Header title="پایه مورد نظر خود را انتخاب کنید"></Header>
    <div class="parent">
        <transition name="fadeIn" mode="out-in">
            <div class="text-center bg-light p-4 rounded" v-if="toggleShow" key="first">
                <b-spinner type="grow" variant="warning" label="Text Centered"></b-spinner>
                <div v-if="toolboxcondition" class="exitBtnaAnimate">
                    <h6 class="my-2">لطفا کمی صبر کنید</h6>
                    <button @click="onLogout" class="btn btn-danger mx-auto mt-3 shadow">خروج</button>
                </div>
            </div>
            <div class="btn-box" v-if="!toggleShow" key="seconde">
                <router-link class="btn btn-warning" :class="{disabled:!grad.has_content}" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">
                    <i class="far fa-lock icon" :class="{'d-none':grad.has_content}"></i>
                    پایه {{grad.title}}
                </router-link>
                <button @click="onLogout" class="btn btn-outline-danger mx-auto mt-3 d-block w-25 btn-sm shadow">خروج</button>
            </div>
        </transition>
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
            toggleShow: true,
            toolboxcondition: false
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
                    this.toggleShow = false
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        toggleCondition() {
            this.toolboxcondition = true
        }
    },
    created() {
        this.getgrads();
        setTimeout(() => {
            this.toggleCondition()
        }, 5000)
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
