<template>
<div>
    <Header title="ورود"></Header>
    <div class="outter">
        <div class="inner">
            <form @submit="onSubmit">
                <CInput lable="شماره موبایل" @inputdata="LoginForm.Mobile=$event" type="number"></CInput>
                <CInput lable="کلمه عبور" type="password" @inputdata="LoginForm.Password=$event"></CInput>
                <div class="btn-box">
                    <button class="btn" type="submit">ورود</button>
                    <router-link to="/Singup" class="btn">ثبت نام</router-link>
                    <router-link to="/Guids" class="btn">راهنمای استفاده</router-link>
                </div>
            </form>
        </div>
    </div>
</div>
</template>

<script>
import CustomInput from '../components/CustomInput'
import Header from '@/components/Header.vue'
export default {
    data() {
        return {
            LoginForm: {
                Mobile: '',
                Password: ''
            },
        }
    },
    components: {
        CInput: CustomInput,
        Header
    },
    methods: {
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                Mobile: this.LoginForm.Mobile,
                Password: this.LoginForm.Password,
            };
            this.$store.dispatch('login', {
                Mobile: payload.Mobile,
                Password: payload.Password
            })
            this.initForm();
        },
        initForm() {
            this.LoginForm.Mobile = '';
            this.LoginForm.Password = '';
        },
    },
}
</script>

<style lang="css" scoped>
.outter {
    padding: 15px;
}

.inner {
    background-color: #f1d6ab66;
    border-radius: 4px;
    margin-top: 30%;
}

.btn-box {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: wrap;
    padding: 15px;
}

.btn-box button,
.btn-box a {
    background-color: #f0a500;
    min-width: 120px;
    margin-bottom: 15px;
}
</style>
