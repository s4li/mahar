<template>
<div>
    <Header title="درس مورد نظر خود را انتخاب کنید"></Header>
    <router-link class="back-btn" to="/Grades"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" appear>
        <div class="parent">
            <div class="btn-box">
                <b-button @click="unlockCheck(lesson.id)" variant="warning" v-for="(lesson, index) in lessons" :key="index">
                    <i class="far fa-lock icon" :class="{'d-none':lesson.show_lesson}"></i>{{lesson.title}}</b-button>
            </div>
        </div>
    </transition>
    <b-modal v-model="show" id="modal-center" content-class="shadow" hide-footer centered header-bg-variant="warning" headerTextVariant="dark">
        <template v-slot:modal-header="{ close }">
            <h5 class="w-100 m-0 text-center">توجه!</h5>
            <b-button class="d-none" size="sm" variant="light" @click="close()"><i style="vertical-align: sub;" class="far fa-times"></i></b-button>
        </template>
        <h4 class="text-center h6">شما پایه <span style="font-weight:bold">{{gardnum | translate}}</span> را انتخاب کرده اید محتویات این پایه در صورت خریداری شدن فعال خواهد شد</h4>
        <div class="buy-box">
            <div class="buy-box-child" style="border-left: 1px solid #d8d8d8;">
                <h5>فعالسازی این پایه</h5>
                <button class="btn btn-primary" @click.prevent="buyPlan(gardnum,2)">۲۰۰۰ تومان</button>
            </div>
            <div class="buy-box-child">
                <h5>فعالسازی کل برنامه</h5>
                <button class="btn btn-success" @click.prevent="buyPlan(0,1)">۵۰۰۰ تومان</button>
            </div>
        </div>
        <div class="text-center" v-if="spinnerShow">
            <b-spinner type="grow" variant="warning" label="Text Centered"></b-spinner>
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
            spinnerShow:false,
        }
    },
    methods: {
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
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        buyPlan(grad, plan) {
            this.spinnerShow = true
            axios.get('/zarinpall', {
                    params: {
                        user_id: this.userid,
                        course_id: grad,
                        sale_plan_id: plan,
                    }
                })
                .then((res) => {
                    this.lessons = res.data;
                    const URL = res.data.zarinpal_url
                    window.location = URL
                })
                .catch((error) => {
                    console.error(error);
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
    background-color: #f8f9fa99;
    border-radius: 4px;
}

.btn-box button {
    width: 45%;
    margin: 20px 0 0;
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
