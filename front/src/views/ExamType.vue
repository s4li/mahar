<template>
<div>
    <Header title="نوع آزمون خود را انتخاب کنید"></Header>

    <router-link class="back-btn" :to="'/Lessons/' + gradId "><i class='fas fa-arrow-left'></i></router-link>

    <div class="parent">
        <transition name="fadeIn" mode="out-in">
            <div class="text-center" v-if="toggleShow" key="first">
                <b-spinner class="ml-2" type="grow" variant="warning" label="Text Centered"></b-spinner>
            </div>
            <div class="btn-box" v-if="!toggleShow" key="seconde">
                <router-link class="btn" :class="{disabled:!newStatus}" :to="'/Courses/check_new_question/'+ lessonId + '/' + gradId">پرسش جدید</router-link>
                <router-link class="btn" :class="{disabled:!previousStatus}" :to="'/Courses/review_previous_questions/'+ lessonId + '/' + gradId">ادامه پرسش قبلی</router-link>
                <router-link class="btn" :class="{disabled:!wrongStatus}" :to="'/Courses/check_wrong_questions/'+ lessonId + '/' + gradId">مرور غلط های این بخش</router-link>
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
        }
    },
    methods: {
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
    },
}
</script>

<style scoped>
.btn-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    background-color: #ffffffcc;
    border-radius: 4px;
    box-shadow: 0 3px 10px #cccccc;
}

.btn-box button,
.btn-box a {
    margin: 15px 0;
    padding: 8px;
    width: 80%;
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    text-align: center;
    border-radius: 4px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

a.btn.disabled,
fieldset:disabled a.btn {
    pointer-events: none;
}
</style>
