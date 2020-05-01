<template>
<div class="hereparent">
    <transition name="slideInUp" appear mode="out-in">
        <div class="back" v-if="show" key="first">
            <h3>{{Courses.question}}</h3>
            <button class="btn play" @click.prevent="playSound()"><i class="fas fa-volume"></i></button>
            <button class="btn btn-warning" @click.prevent="getanswerdata()">معنیش چیه؟</button>
        </div>
        <div class="back" v-if="!show" key="seconde">
            <h3>{{answer.answer}}</h3>
            <div>
                <button @click.prevent="SendAnswer(1)" class="btn true"><i class="far fa-check"></i>درسته</button>
                <button @click.prevent="SendAnswer(0)" class="btn false"><i class="far fa-times"></i>غلطه</button>
            </div>
        </div>
    </transition>
</div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            show: true,
            index: -1,
            Courses: [],
            CoursesType: this.$route.params.Type,
            lessonId: this.$route.params.lessonId,
            gradId: this.$route.params.gradId,
            answer: '',
            questionId: '',
            userid: this.$store.state.userId,
        }
    },
    methods: {
        getCourses() {
            axios.get('/new-questions', {
                    params: {
                        index: this.index,
                        lesson_id: this.lessonId
                    }
                })
                .then((res) => {
                    this.Courses = res.data;
                    this.index = res.data.next_index
                    this.questionId = res.data.question_id
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        getanswerdata() {
            axios.get('/get-answer', {
                    params: {
                        question_id: this.questionId
                    }
                })
                .then((res) => {
                    this.show = false
                    this.answer = res.data
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        SendAnswer(num) {
            axios.post('/set-user-answer', {
                    params: {
                        user_id: this.userid,
                        question_id: this.questionId,
                        lesson_id: this.lessonId,
                        ans_no: num,
                    }
                })
                .then(() => {
                    this.initForm();
                    this.getCourses()
                    this.show = true
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        playSound() {
            var audio = new Audio(require(`../assets/${this.Courses.voice}`));
            audio.play();
        },
        initForm() {
            this.Courses = [];
            this.answer = '';
            this.questionId = '';
        },
    },
    created() {
        this.getCourses();
    },
}
</script>

<style lang="css">
.hereparent {
    position: relative;
    height: 100vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.back {
    padding: 15px;
    background-color: #f8f9facc;
    border-radius: 4px;
    text-align: center;
    width: 70%;
}

.play {
    display: block;
    margin: 15px auto;
    padding: 8px 12px;
    border: 1px solid #909090;
    background: #f8f9fa;
}

.play i {
    vertical-align: middle;
    font-size: 18px;
}

.true {
    padding: 5px 15px;
    background-color: #28a745;
    margin: 10px 10px 0;
    color: #ffffff;
}

.true i,
.false i {
    width: 15px;
    text-align: right;
    vertical-align: middle;
}

.false {
    padding: 5px 15px;
    background-color: #dc3545;
    margin: 10px 10px 0;
    color: #ffffff;
}

.slideInUp-enter-active {
    -webkit-animation-name: slideInUp;
    animation-name: slideInUp;
    -webkit-animation-duration: 1s;
    animation-duration: 1s;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
}

@-webkit-keyframes slideInUp {
    from {
        -webkit-transform: translate3d(0, 100%, 0);
        transform: translate3d(0, 100%, 0);
        visibility: visible;
    }

    to {
        -webkit-transform: translate3d(0, 0, 0);
        transform: translate3d(0, 0, 0);
    }
}

@keyframes slideInUp {
    from {
        -webkit-transform: translate3d(0, 100%, 0);
        transform: translate3d(0, 100%, 0);
        visibility: visible;
    }

    to {
        -webkit-transform: translate3d(0, 0, 0);
        transform: translate3d(0, 0, 0);
    }
}
</style>
