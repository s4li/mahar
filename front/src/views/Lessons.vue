<template>
<div>
    <Header title="درس مورد نظر خود را انتخاب کنید"></Header>
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
            <div class="text-center" v-if="toggleShow" key="first">
                <b-spinner class="ml-2" type="grow" variant="warning" label="Text Centered"></b-spinner>
            </div>
            <div class="btn-box" v-if="!toggleShow" key="seconde">
                <b-button @click="unlockCheck(lesson.id)" variant="warning" v-for="(lesson, index) in lessons" :key="index">
                    <i class="far fa-lock icon" :class="{'d-none':lesson.show_lesson}"></i>{{lesson.title}}</b-button>
            </div>
        </transition>
    </div>

    <b-modal v-model="show" id="modal-center" content-class="shadow" hide-footer centered header-bg-variant="warning" headerTextVariant="dark">
        <template v-slot:modal-header="{ close }">
            <h5 class="w-100 m-0 text-center">توجه!</h5>
            <b-button class="d-none" size="sm" variant="light" @click="close()"><i style="vertical-align: sub;" class="far fa-times"></i></b-button>
        </template>
        <h4 class="text-center h6">شما پایه <span style="font-weight:bold">{{gardnum | translate}}</span> را انتخاب کرده اید محتویات این پایه در صورت خریداری شدن فعال خواهد شد</h4>
        <div class="buy-box">
            <div class="buy-box-child" style="border-left: 1px solid #d8d8d8;">
                <h5>فعالسازی این پایه</h5>
                <button class="btn shadow btn-primary" @click.prevent="buyPlan(gardnum,2)">۲۰۰۰ تومان</button>
            </div>
            <div class="buy-box-child">
                <h5>فعالسازی کل برنامه</h5>
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
        }
    },
    methods: {
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
                    window.location = URL
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
    background-color: #ffffffcc;
    border-radius: 4px;
    box-shadow: 0 3px 10px #cccccc;
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
</style>
