<template>
<div class="outter">
    <div class="inner">
        <form @submit="onSubmit">
            <CInput lable="نام کاربری" @inputdata="SingupForm.Username=$event"></CInput>
            <CInput lable="کلمه عبور" @inputdata="SingupForm.Mobile=$event"></CInput>
            <CInput lable="شماره موبایل" @inputdata="SingupForm.Password=$event" type="number"></CInput>
            <div class="btn-box">
                <button class="btn" type="submit">ثبت نام</button>
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
            usercheck: false,
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
