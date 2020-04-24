<template>
<div class="outter">
    <div class="inner">
        <form @submit="onSubmit">
            <CInput lable="نام کاربری" @inputdata="LoginForm.Username=$event"></CInput>
            <CInput lable="کلمه عبور" type="password" @inputdata="LoginForm.Password=$event"></CInput>
            <div class="btn-box">
                <button class="btn" type="submit">ورود</button>
                <router-link to="/Singup" class="btn">ثبت نام</router-link>
                <router-link to="/Guids" class="btn">راهنمای استفاده</router-link>
            </div>
        </form>
    </div>
</div>
</template>

<style lang="css" scoped>
.outter {
    padding: 15px;
}

.inner {
    background-color: #f1d6ab66;
    border-radius: 4px;
    margin-top: 40%;
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

<script>
import CustomInput from '../components/CustomInput'
import axios from 'axios';
export default {
    data() {
        return {
            LoginForm: {
                Username: '',
                Password: ''
            },
        }
    },
    components: {
        CInput: CustomInput,
    },
    methods: {
        Login(payload) {
            //const path = 'http://localhost:5000/api/login';
            const path = '/api/login';
            axios.post(path, payload)
                .then((res) => {
                    if (res.data.user) {
                        this.$router.push('/AllOrder');
                    } else {
                        console.log('error1')
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                Username: this.LoginForm.Username,
                Password: this.LoginForm.Password,
            };
            this.Login(payload);
            this.initForm();
        },
        initForm() {
            this.LoginForm.Username = '';
            this.LoginForm.Password = '';
        },
    },
}
</script>
