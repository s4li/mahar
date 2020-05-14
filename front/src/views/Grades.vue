<template>
<div>
    <Header :title="title"></Header>
    <div class="parent">
        <transition name="fadeIn" mode="out-in">
            <div class="text-center bg-light p-4 rounded" v-if="toggleShow" key="first">
                <b-spinner type="grow" variant="warning" label="Text Centered"></b-spinner>
                <div v-if="toolboxcondition" class="exitBtnaAnimate">
                    <h6 class="my-2">لطفا کمی صبر کنید</h6>
                    <button @click="onLogout" class="btn btn-danger mx-auto mt-3 shadow">خروج</button>
                </div>
            </div>
            <div v-if="!toggleShow" key="seconde">
                <div class="btnBoxParrent p-4" id="width" v-if="extraData">
                    <h1 class="d-block h6 p-3 my-2" id="extratitle">لطفا پایه و شهر خود را مشخص کنید</h1>
                    <form @submit="getExtraUserData">
                        <b-row class="mb-2 mb-lg-5">
                            <b-col cols="2"><p class="titleextradata">شهر</p></b-col>
                            <b-col>
                                <b-form-select required class="my-2" v-model="city" :options="provinces"></b-form-select>
                            </b-col>
                        </b-row>
                        <b-row class="mb-2 mb-lg-4">
                            <b-col cols="2"><p class="titleextradata">پایه</p></b-col>
                            <b-col>
                                <b-form-select required class="my-2" v-model="degree" :options="degrees"></b-form-select>
                            </b-col>
                        </b-row>
                        <button class="btn btn-primary" type="submit">ذخیره اطلاعات</button>
                    </form>
                </div>
                <div class="btnBoxParrent" v-if="!extraData">
                    <h1 class="d-block h5">پایه مورد نظر خود را انتخاب کنید</h1>
                    <div class="btn-box">
                        <router-link class="btn btn-warning" :class="{disabled:!grad.has_content}" :to="'/Lessons/'+ grad.id" v-for="(grad, index) in grads" :key="index">
                            <i class="far fa-lock icon" :class="{'d-none':grad.has_content}"></i>
                            پایه {{grad.title}}
                        </router-link>
                    </div>
                    <button @click="onLogout" class="btn btn-outline-danger mx-auto mt-3 d-block w-25 btn-sm shadow">خروج</button>
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

    methods: {
        onLogout() {
            this.$store.dispatch('logout')
        },
        getgrads() {
            const url = this.$route.path
            this.$store.commit('StoreCurrentUrl', url);
            axios.get('/courses', {
                    params: {
                        user_id: this.userId
                    }
                })
                .then((res) => {
                    this.grads = res.data.all_courses;
                    this.extraData = res.data.complete_information
                    if (this.extraData) {
                        this.title = 'لطفا پایه و شهر خود را مشخص کنید'
                    } else {
                        this.title = 'پایه مورد نظر خود را انتخاب کنید'
                    }
                    this.toggleShow = false
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        getExtraUserData(evt) {
            evt.preventDefault();
            axios.post('/information-completion-status', {
                    user_id: this.userId,
                    grade: this.degree,
                    city: this.city,
                })
                .then((res) => {
                    console.log(res)
                    this.extraData = false
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        toggleCondition() {
            this.toolboxcondition = true
        }
    },
    created() {
        this.getgrads();
        setTimeout(() => {
            this.toggleCondition()
        }, 5000)
    },
    data() {
        return {
            title:'',
            grads: [],
            toggleShow: true,
            toolboxcondition: false,
            userId: this.$store.state.userId,
            degree: null,
            city: null,
            extraData: false,
            provinces: [
                { value: null, text: 'شهر خود را انتخاب نمایید' },
                {"value": "آذربایجان شرقی", "text": "آذربایجان شرقی"},
                {"value": "آذربایجان غربی", "text": "آذربایجان غربی"},
                {"value": "اردبیل", "text": "اردبیل"},
                {"value": "اصفهان", "text": "اصفهان"},
                {"value": "البرز", "text": "البرز"},
                {"value": "ایلام", "text": "ایلام"},
                {"value": "بوشهر", "text": "بوشهر"},
                {"value": "تهران", "text": "تهران"},
                {"value": "چهارمحال و بختیاری", "text": "چهارمحال و بختیاری"},
                {"value": "خراسان جنوبی", "text": "خراسان جنوبی"},
                {"value": "خراسان رضوی", "text": "خراسان رضوی"},
                {"value": "خراسان شمالی", "text": "خراسان شمالی"},
                {"value": "خوزستان", "text": "خوزستان"},
                {"value": "زنجان", "text": "زنجان"},
                {"value": "سمنان", "text": "سمنان"},
                {"value": "سیستان و بلوچستان", "text": "سیستان و بلوچستان"},
                {"value": "فارس", "text": "فارس"},
                {"value": "قزوین", "text": "قزوین"},
                {"value": "قم", "text": "قم"},
                {"value": "کردستان", "text": "کردستان"},
                {"value": "کرمان", "text": "کرمان"},
                {"value": "کرمانشاه", "text": "کرمانشاه"},
                {"value": "کهگیلویه و بویراحمد", "text": "کهگیلویه و بویراحمد"},
                {"value": "گلستان", "text": "گلستان"},
                {"value": "گیلان", "text": "گیلان"},
                {"value": "لرستان", "text": "لرستان"},
                {"value": "مازندران", "text": "مازندران"},
                {"value": "مرکزی", "text": "مرکزی"},
                {"value": "هرمزگان", "text": "هرمزگان"},
                {"value": "همدان", "text": "همدان"},
                {"value": "یزد", "text": "یزد"}
            ],
            degrees: [
                { value: null, text: 'پایه خود را انتخاب نمایید' },
                {"value": "هفتم", "text": "هفتم"},
                {"value": "هشتم", "text": "هشتم"},
                {"value": "نهم", "text": "نهم"},
                {"value": "دهم", "text": "دهم"},
                {"value": "یازدهم", "text": "یازدهم"},
                {"value": "دوازدهم", "text": "دوازدهم"},
            ],
        }
    },
}
</script>

<style scoped>
#width{
    min-width: 500px;
}
.titleextradata{
    margin: 15px 0 0 0;
}
.btn-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.btn-box a {
    width: 45%;
    margin: 10px 0 10px;
    padding: 8px;
}

.btn-warning {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.btn-warning:focus,
.btn-warning.focus {
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
    box-shadow: none;
}
@media (max-width: 991.8px) {
    #width{
        min-width: 300px;
    }
    #extratitle{
        display: none!important;
    }
}
</style>
