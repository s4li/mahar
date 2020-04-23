<template>
<div>
    <form @submit="onSubmit">
        <CInput lable="نام کاربری" @inputdata="SingupForm.Username=$event"></CInput>
        <CInput lable="کلمه عبور" @inputdata="SingupForm.Mobile=$event"></CInput>
        <CInput lable="شماره موبایل" @inputdata="SingupForm.Password=$event" type="number"></CInput>
        <button type="submit">ثبت نام</button>
    </form>
</div>
</template>

<style lang="css">

</style>

<script>
import CustomInput from '../components/CustomInput';
import axios from 'axios';
export default {
    data() {
        return {
            SingupForm: {
                Username: '',
                Mobile: '',
                Password: ''
            },
            usercheck:false,
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
                        this.$router.push('/Grades');
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
                Username: this.SingupForm.Username,
                Mobile: this.SingupForm.Mobile,
                Password: this.SingupForm.Password,
            };
            this.Login(payload);
            this.initForm();
        },
        initForm() {
            this.SingupForm.Username = '';
            this.SingupForm.Mobile = '';
            this.SingupForm.Password = '';
        },
    },
}
</script>
