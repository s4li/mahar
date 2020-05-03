<template>
<div class="hereparent">
    <router-link class="back-btn" :to="'/ExamType/' + lessonId + '/' + gradId"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" appear>
        <div class="flip-card">
            <div class="flip-card-inner" :class="{isFlipped:flip}">
                <div class="flip-card-front back">
                    <h3>{{Courses.question}}</h3>
                    <button class="btn play" @click.prevent="playSound()"><i class="fas fa-volume"></i></button>
                    <button class="btn btn-warning" @click.prevent="flip = true">معنیش چیه؟</button>
                </div>
                <div class="flip-card-back back">
                    <h3 class="mb-4">{{answer}}</h3>
                    <div>
                        <button @click.prevent="SendAnswer(0)" class="btn shadow true"><i class="far fa-check"></i>درسته</button>
                        <button @click.prevent="SendAnswer(1)" class="btn shadow false"><i class="far fa-times"></i>غلطه</button>
                    </div>
                </div>
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
                    this.index = res.data.next_index;
                    this.answer = res.data.answer;
                    this.questionId = res.data.question_id;
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
                    console.log(res)
                    if (res.data.has_next_new_question == 'True') {
                        this.initForm();
                        this.getCourses(this.path)
                        this.flip = false
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
    background-color: #fdfdfd;
    border-radius: 10px;
    text-align: center;
}

.play {
    display: block;
    margin: 15px auto;
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
    width: 250px;
    height: 170px;
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
    padding-top: 35px;
}
</style>
