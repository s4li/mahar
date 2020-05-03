<template>
<div class="hereparent">
    <router-link class="back-btn" :to="'/ExamType/' + lessonId + '/' + gradId"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="slideInUp" appear mode="out-in">
        <div class="back" v-if="show" key="first">
            <h3>{{Courses.question}}</h3>
            <button class="btn play" @click.prevent="playSound()"><i class="fas fa-volume"></i></button>
            <button class="btn btn-warning" @click.prevent="show = false">معنیش چیه؟</button>
        </div>
        <div class="back" v-if="!show" key="seconde">
            <h3>{{answer}}</h3>
            <div>
                <button @click.prevent="SendAnswer(0)" class="btn true"><i class="far fa-check"></i>درسته</button>
                <button @click.prevent="SendAnswer(1)" class="btn false"><i class="far fa-times"></i>غلطه</button>
            </div>
        </div>
    </transition>
    <b-modal v-model="ModalShow" class="text-center" content-class="shadow" hide-footer hide-header centered title="">
        <h4 class="my-4 text-center">شما به پایان این دوره از کلمات رسیدید</h4>
        <button class="btn btn-primary d-block m-auto w-25" @click.prevent="redirect()">بستن</button>
    </b-modal>
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
            CoursesType: this.$route.params.type,
            lessonId: this.$route.params.lessonId,
            gradId: this.$route.params.gradId,
            answer: '',
            userid: this.$store.state.userId,
            path: '',
            ModalShow: false,
            questionType: 0
        }
    },
    methods: {
        getCourses(URL) {
            this.path = URL
            axios.get(URL, {
                    params: {
                        user_id: this.userid,
                        lesson_id: this.lessonId,
                        index: this.index,
                    }
                })
                .then((res) => {
                    this.Courses = res.data;
                    this.index = res.data.next_index
                    this.answer = res.data.answer
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        SendAnswer(num) {
            axios.post('/set-user-answer', {
                    user_id: this.userid,
                    lesson_id: this.lessonId,
                    ans_no: num,
                    question_type: this.questionType
                })
                .then((res) => {
                    console.log(res)
                    if (res.data.has_next_question == 'True') {
                        this.initForm();
                        this.getCourses(this.path)
                        this.show = true
                    } else {
                        this.ModalShow = true
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        redirect() {
            this.initForm();
            this.show = true
            this.$router.push('/ExamType/' + this.lessonId + '/' + this.gradId);
        },
        playSound() {
            var audio = new Audio(require(`../assets/${this.Courses.voice}`));
            audio.play();
        },
        initForm() {
            this.Courses = [];
            this.answer = '';
        },
    },
    created() {
        if (this.CoursesType == 'check_new_question') {
            this.questionType = 1
            this.getCourses('/new-questions');
        } else if (this.CoursesType == 'review_previous_questions') {
            this.questionType = 2
            this.getCourses('/get-previous-questions');
        } else {
            this.questionType = 3
            this.getCourses('/get-wrong-questions');
        }
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
    -webkit-animation-duration: 0.75s;
    animation-duration: 0.75s;
    -webkit-backface-visibility: visible !important;
    backface-visibility: visible !important;
    -webkit-animation-name: flipOutY;
    animation-name: flipOutY;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
}

@-webkit-keyframes flipOutY {
    from {
        -webkit-transform: perspective(400px);
        transform: perspective(400px);
    }

    30% {
        -webkit-transform: perspective(400px) rotate3d(0, 1, 0, -15deg);
        transform: perspective(400px) rotate3d(0, 1, 0, -15deg);
        opacity: 1;
    }

    to {
        -webkit-transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
        transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
        opacity: 0;
    }
}

@keyframes flipOutY {
    from {
        -webkit-transform: perspective(400px);
        transform: perspective(400px);
    }

    30% {
        -webkit-transform: perspective(400px) rotate3d(0, 1, 0, -15deg);
        transform: perspective(400px) rotate3d(0, 1, 0, -15deg);
        opacity: 1;
    }

    to {
        -webkit-transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
        transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
        opacity: 0;
    }
}

.flipOutY {
    -webkit-animation-duration: 0.75s;
    animation-duration: 0.75s;
    -webkit-backface-visibility: visible !important;
    backface-visibility: visible !important;
    -webkit-animation-name: flipOutY;
    animation-name: flipOutY;
}
</style>
