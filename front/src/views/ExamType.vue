<template>
<div>
    <Header title="تمایل به انجام چه کاری دارید ؟ "></Header>

    <router-link class="back-btn" :to="'/Lessons/' + gradId "><i class='fas fa-arrow-left'></i></router-link>

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
                <h1 class="d-block h5">تمایل به انجام چه کاری دارید ؟ </h1>
                <div class="btn-box">
                    <router-link class="btn box btn-top" v-if="!previousStatus" :to="'/Courses/check_new_question/'+ lessonId + '/' + gradId">تمرین جدید</router-link>
                    <router-link class="btn box btn-top" v-if="previousStatus" :to="'/Courses/review_previous_questions/'+ lessonId + '/' + gradId">ادامه تمرین قبلی</router-link>
                    <router-link class="btn box btn-bottom" :class="{disabled:!wrongStatus}" :to="'/Courses/check_wrong_questions/'+ lessonId + '/' + gradId">مرور تمرین های گذشته</router-link>
                </div>
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
            lessonId: this.$route.params.lessonId,
            gradId: this.$route.params.gradId,
            userid: this.$store.state.userId,
            newStatus: false,
            previousStatus: false,
            wrongStatus: false,
            toggleShow: true,
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
        getStatus() {
            const url = this.$route.path
            this.$store.dispatch('saveurl', url);
            axios.get('/get-status-question-user', {
                    params: {
                        user_id: this.userid,
                        lesson_id: this.lessonId
                    }
                })
                .then((res) => {
                    if (res.data.check_new_question == 'True') {
                        this.newStatus = true
                    }
                    if (res.data.review_previous_questions == 'True') {
                        this.previousStatus = true
                    }
                    if (res.data.check_wrong_questions == 'True') {
                        this.wrongStatus = true
                    }
                    this.toggleShow = false
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    created() {
        this.getStatus();
        setTimeout(() => {
            this.toggleCondition()
        }, 5000)
    },
}
</script>

<style scoped>
.btn-box {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

.btn-box button,
.btn-box a {
    margin: 15px 0;
    padding: 8px;
    width: 80%;
    text-align: center;
    border-radius: 4px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

a.btn.disabled,
fieldset:disabled a.btn {
    pointer-events: none;
}

.btn-top {
    background-color: #ffd83b;
    border-color: #ffd83b;
    color: #212529;
}

.btn-middle {
    background-color: #ece6c9;
    border-color: #ece6c9;
    color: #212529;
}

.btn-bottom {
    background-color: #b1953f;
    border-color: #b1953f;
    color: #f1f1f1;
}
</style>
