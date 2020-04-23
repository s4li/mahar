<template>
<div>
    <form @submit="onSubmit">
        <CInput lable="نام کاربری" @inputdata="LoginForm.Username=$event"></CInput>
        <CInput lable="کلمه عبور" @inputdata="LoginForm.Password=$event"></CInput>
        <button>ورود</button>
    </form>
    <router-link to="/Singup">ثبت نام</router-link>
</div>
</template>

<style lang="css">

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
