<template>
<div>
    <Header title="ورود"></Header>
    <div class="outter">
        <b-alert class="shakeError" variant="danger" dismissible fade :show="this.$store.state.showAlert">لطفا فرم را به درستی پر کنید.</b-alert>
        <div class="inner">
            <form @submit="onSubmit">
                <CInput lable="شماره موبایل" @inputdata="LoginForm.Mobile=$event" type="number"></CInput>
                <CInput lable="کلمه عبور" type="password" @inputdata="LoginForm.Password=$event"></CInput>
                <div class="btn-box">
                    <router-link to="/Singup" id="singupbtn" class="btn">ثبت نام</router-link>
                    <button class="btn" id="loginbtn" type="submit">ورود</button>
                    <router-link to="/Guids" id="infobtn" class="btn">راهنمای استفاده</router-link>
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
            if (payload.Mobile && payload.Password != '') {
                console.log('ok')
                this.$store.dispatch('login', {
                    Mobile: payload.Mobile,
                    Password: payload.Password
                })
            } else {
                this.$store.state.showAlert = true
                console.log('nok')
            }
        },
    },
}
</script>

<style lang="css" scoped>
#infobtn {
    border: 1px solid #e0e0d8;
    background: #e2dfd6;
}

#loginbtn {
    background-color: #fbb901;
}

#singupbtn {
    border: 1px solid #fbb901;
    background: #faf9f6;
}

.outter {
    padding: 15px;
}

.inner {
    background-color: #f8f9fa99;
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
    background-color: #fbb901;
    min-width: 120px;
    margin-bottom: 15px;
}
</style>
