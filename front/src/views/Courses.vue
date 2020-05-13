<template>
<div class="hereparent">
    <div class="coursesheader">
        <h1>{{lessonTitle}}</h1>
    </div>
    <router-link class="back-btn" :to="'/ExamType/' + lessonId + '/' + gradId"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" mode="out-in">
        <div class="spinnerbackground" v-if="toggleShow" key="first">
                <b-spinner type="grow" variant="warning" label="Text Centered"></b-spinner>
                <div v-if="toolboxcondition" class="exitBtnaAnimate">
                    <h6 class="my-2">لطفا کمی صبر کنید</h6>
                    <button @click="onLogout" class="btn btn-danger mx-auto mt-3 shadow">خروج</button>
                </div>
            </div>
        <div class="flip-card" v-if="!toggleShow" key="seconde">
            <div class="flip-card-inner" :class="{isFlipped:flip}">
                <div class="flip-card-front back">
                    <h3 class="mb-2">{{Courses.question}}</h3>
                    <button class="btn play" @click.prevent="playSound()"><i class="fas fa-volume"></i></button>
                    <button class="btn btn-warning" @click.prevent="flip = true">معنیش چیه؟</button>
                </div>
                <div class="flip-card-back back">
                    <h3 class="h4">{{answer}}</h3>
                    <div>
                        <button @click.prevent="SendAnswer(0)" class="btn shadow true"><i class="far fa-check"></i>درسته</button>
                        <button @click.prevent="SendAnswer(1)" class="btn shadow false"><i class="far fa-times"></i>غلطه</button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
    <b-modal v-model="ModalShow" class="text-center" content-class="shadow" hide-footer centered header-bg-variant="warning" headerTextVariant="dark">
        <template v-slot:modal-header="{ close }">
            <h5 class="w-100 m-0 text-center">شما به پایان این دوره از کلمات رسیدید</h5>
            <b-button class="d-none" size="sm" variant="light" @click="close()"><i style="vertical-align: sub;" class="far fa-times"></i></b-button>
        </template>
        <h4 class="my-4 text-center"> تعداد جواب های صحیح : {{trueAnswer | faNum}}</h4>
        <h4 class="my-4 text-center">تعداد جواب های غلط : {{wrongAnswer | faNum}}</h4>
        <div class="d-flex justify-content-center">
            <router-link class="btn btn-primary m-2" :to="'/Lessons/' + gradId">درس ها</router-link>
            <button class="btn btn-secondary m-2" @click.prevent="redirect()">آزمون ها</button>
        </div>
    </b-modal>
</div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            index: -1,
            Courses: [],
            CoursesType: this.$route.params.type,
            lessonId: this.$route.params.lessonId,
            gradId: this.$route.params.gradId,
            answer: '',
            userid: this.$store.state.userId,
            path: '',
            ModalShow: false,
            questionType: 0,
            flip: false,
            questionId: '',
            wrongAnswer: '',
            trueAnswer: '',
            toggleShow: true,
            lessonTitle: '',
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
                    this.index = res.data.next_index;
                    this.answer = res.data.answer;
                    this.questionId = res.data.question_id;
                    this.toggleShow = false
                    this.lessonTitle = res.data.lesson_title;
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
                    question_type: this.questionType,
                    question_id: this.questionId,
                })
                .then((res) => {
                    if (res.data.has_next_new_question == 'True') {
                        this.initForm();
                        this.getCourses(this.path)
                        this.Preview()
                    } else {
                        this.ModalShow = true
                        this.wrongAnswer = res.data.wrong_answer_no
                        this.trueAnswer = res.data.true_answer_no
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        Preview(){
            this.toggleShow = true
            this.flip = false
            this.toolboxcondition= false
            setTimeout(() => {
            this.toggleCondition()
        }, 5000)
        },
        redirect() {
            this.initForm();
            this.flip = true
            this.$router.push('/ExamType/' + this.lessonId + '/' + this.gradId);
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
        setTimeout(() => {
            this.toggleCondition()
        }, 5000)
    },
}
</script>

<style lang="css">
.coursesheader {
    text-align: center;
    padding: 20px;
    background: #ffba23;
    /* fallback for old browsers */
    background: -webkit-linear-gradient(to right, #FFD200, #ffba23);
    /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to right, #FFD200, #ffba23);
    /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    color: #f8f9fa;
    margin: 0 -15px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}
.spinnerbackground{
    background: #ffffff8f;
    padding: 15px;
    border-radius: 4px;
    text-align: center;
}
.coursesheader h1 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    padding-top: 5px;
}

.hereparent {
    position: relative;
    height: calc(100vh - 161.13px);
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.back {
    padding: 15px;
    background-color: #fdfdfd;
    border-radius: 10px;
    text-align: center;
}

.play {
    display: block;
    margin: 10px auto;
    padding: 8px 12px;
    border: none;
    border-radius: 4px;
    background: linear-gradient(145deg, #ffffff, #e6e6e6);
    box-shadow: 4px 4px 8px #b3b3b3,
        -4px -4px 8px #ffffff;
}

.play:focus {
    box-shadow: 4px 4px 8px #b3b3b3,
        -4px -4px 8px #ffffff !important;
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
/************************************** */
.flip-card {
    background-color: transparent;
    width: 300px;
    height: 150px;
    perspective: 1000px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.isFlipped {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
}

.flip-card-front {
    background-color: #fdfdfd;
}

.flip-card-back {
    background-color: #fdfdfd;
    transform: rotateY(180deg);
}

.flip-card-back h3 {
    min-height: 60px;
    padding-top: 10px;
}
</style>
