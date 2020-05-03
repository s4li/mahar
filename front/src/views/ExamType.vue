<template>
<div>
    <Header title="نوع آزمون خود را انتخاب کنید"></Header>
    <router-link class="back-btn" :to="'/ExamType/' + lessonId "><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" appear>
        <div class="parent">
            <div class="btn-box">
                <router-link class="btn" :class="{disabled:!newStatus}" :to="'/Courses/check_new_question/'+ lessonId + '/' + gradId">پرسش جدید</router-link>
                <router-link class="btn" :class="{disabled:!previousStatus}" :to="'/Courses/review_previous_questions/'+ lessonId + '/' + gradId">ادامه پرسش قبلی</router-link>
                <router-link class="btn" :class="{disabled:!wrongStatus}" :to="'/Courses/check_wrong_questions/'+ lessonId + '/' + gradId">مرور غلط های این بخش</router-link>
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
            lessonId: this.$route.params.lessonId,
            gradId: this.$route.params.gradId,
            userid: this.$store.state.userId,
            newStatus:false,
            previousStatus:false,
            wrongStatus:false,
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
                    console.log(res)
                    console.log(res.data.check_new_question)
                    console.log(res.data.review_previous_questions)
                    console.log(res.data.check_wrong_questions)
                    if(res.data.check_new_question == 'True'){
                        this.newStatus=true
                    }
                    if(res.data.review_previous_questions == 'True'){
                        this.previousStatus=true
                    }
                    if(res.data.check_wrong_questions == 'True'){
                        this.wrongStatus=true
                    }
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
    background-color: #f8f9fa99;
    border-radius: 4px;
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
