<template>
<div>
    <Header title="درس مورد نظر خود را انتخاب نمایید."></Header>
    <router-link class="back-btn" to="/Grades"><i class='fas fa-arrow-left'></i></router-link>

    <transition name="shakeTop">
        <div class="shakeTop alert alert-danger mt-2 alert-dismissible" v-if="this.$store.state.showAlert" role="alert">
            {{this.$store.state.alerttext}}
            <button type="button" class="close" @click.prevent="close()" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    </transition>

    <div class="parent">
        <transition name="fadeIn" mode="out-in">
            <div class="text-center bg-light p-4 rounded" v-if="toggleShow" key="first">
                <b-spinner type="grow" variant="warning" label="Text Centered"></b-spinner>
                <div v-if="toolboxcondition" class="exitBtnaAnimate">
                    <h6 class="my-2">لطفا کمی صبر کنید</h6>
                    <button @click="onLogout" class="btn btn-danger mx-auto mt-3 shadow">خروج</button>
                </div>
            </div>
            <div class="btnBoxParrent" v-if="!toggleShow" key="seconde">
                <h1 class="d-block h5">درس مورد نظر خود را انتخاب نمایید.</h1>
                <div class="btn-box">
                    <b-button @click="unlockCheck(lesson.id)" class="box" variant="warning" v-for="(lesson, index) in lessons" :key="index">
                        <i class="far fa-lock icon" :class="{'d-none':lesson.show_lesson}"></i>{{lesson.title}}</b-button>
                </div>
            </div>
        </transition>
    </div>

    <b-modal v-model="show" id="modal-center" content-class="shadow" hide-footer centered header-bg-variant="warning" headerTextVariant="dark">
        <template v-slot:modal-header="{ close }">
            <h5 class="w-100 m-0 text-center">توجه!</h5>
            <b-button class="d-none" size="sm" variant="light" @click="close()"><i style="vertical-align: sub;" class="far fa-times"></i></b-button>
        </template>
        <h4 class="text-center h6">کاربر عزیز شما پایه<span style="font-weight:bold"> {{gardnum | translate}} </span>  را انتخاب کرده اید پس از خرید آن دسترسی به دروس باز می شود. </h4>
        <div class="buy-box">
            <div class="buy-box-child" style="border-left: 1px solid #d8d8d8;">
                <h5>فعالسازی این پایه</h5>
                <button class="btn shadow btn-primary" @click.prevent="buyPlan(gardnum,2)">۲۰۰۰ تومان</button>
            </div>
            <div class="buy-box-child">
                <h5>فعالسازی {{gradname}}</h5>
                <button class="btn shadow btn-success" @click.prevent="buyPlan(0,1)">۵۰۰۰ تومان</button>
            </div>
        </div>
        <div class="text-center" v-if="spinnerShow">
            <b-spinner class="ml-2" type="grow" variant="warning" label="Text Centered"></b-spinner>
            <h4>لطفا کمی صبر کنید ...</h4>
        </div>
    </b-modal>
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
            gardnum: this.$route.params.id,
            userid: this.$store.state.userId,
            show: false,
            lessonsData: [],
            lessons: [],
            courseId: 0,
            spinnerShow: false,
            toggleShow: true,
            gradname: '',
            toolboxcondition: false
        }
    },
    methods: {
        onLogout() {
            this.$store.dispatch('logout')
        },
        toggleCondition() {
            this.toolboxcondition = true
        },
        close() {
            this.$store.state.showAlert = false
        },
        unlockCheck(checkid) {
            this.courseId = checkid
            const grads = this.lessons
            for (let key in grads) {
                const grad = grads[key]
                if (grad.id == checkid) {
                    this.lessonsData = grad
                }
            }
            if (this.lessonsData.show_lesson) {
                this.$router.push('/ExamType/' + checkid + '/' + this.gardnum);
            } else {
                this.show = true
            }
        },
        getlessons() {
            const url = this.$route.path
            this.$store.dispatch('saveurl', url);
            axios.get('/lessons', {
                    params: {
                        user_id: this.userid,
                        course_id: this.gardnum
                    }
                })
                .then((res) => {
                    this.lessons = res.data;
                    this.toggleShow = false
                })
                .catch((error) => {
                    console.error(error);
                });
            const gradId = this.gardnum
            if (gradId == 1 || gradId == 2 || gradId == 3) {
                this.gradname = 'متوسطه اول'
            } else {
                this.gradname = 'متوسطه دوم'
            }
        },
        buyPlan(grad, plan) {
            this.spinnerShow = true
            const gradId = this.gardnum
            let planId
            if (plan == 2) {
                planId = 2
            } else {
                if (gradId == 1 || gradId == 2 || gradId == 3) {
                    planId = 3
                } else {
                    planId = 1
                }
            }
            const path = '/zarinpal/site/' + this.userid + '/' + planId + '/' + grad
            axios.get(path)
                .then((res) => {
                    this.lessons = res.data;
                    const URL = res.data.zarinpal_url
                    window.open(URL, '_blank');
                })
                .catch((error) => {
                    if (error.response.status == 401) {
                        this.state.alerttext = error.response.data.result
                    } else {
                        this.state.alerttext = 'خطای غیرمنتظره'
                    }
                    this.state.showAlert = true
                });
        }
    },
    created() {
        this.getlessons();
        setTimeout(() => {
            this.toggleCondition()
        }, 5000)
    },
}
</script>

<style>

.btn-box {
    display: block;
}

.btn-box button {
    width: 45%;
    margin: 10px 0 10px;
    padding: 8px;
}

.icon {
    width: 20px;
    text-align: center;
}

.modal-backdrop {
    background-color: #0006 !important;
}

.modal-content {
    border: none;
    border-radius: 4px;
}

.modal-body h4 {
    font-size: 14px;
    line-height: 1.5;
}

.buy-box {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.buy-box-child {
    padding: 10px 20px;
    margin: 15px 0;
}

.buy-box-child h5 {
    font-size: 14px;
}

@media (max-width: 991.8px) {
    .btn-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
}

@media (min-width: 992px) {
    .btn-box button {
        margin: 10px;
    }
}
</style>
