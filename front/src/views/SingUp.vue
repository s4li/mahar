<template>
<div class="outter">
    <div class="inner">
        <form @submit="onSubmit">
            <CInput lable="نام کاربری" @inputdata="SingupForm.FullName=$event"></CInput>
            <CInput lable="کلمه عبور" @inputdata="SingupForm.Mobile=$event" type="password"></CInput>
            <CInput lable="شماره موبایل" @inputdata="SingupForm.Password=$event" type="number"></CInput>
            <div class="btn-box">
                <button class="btn" type="submit">ثبت نام</button>
            </div>
        </form>
    </div>
</div>
</template>

<script>
import CustomInput from '../components/CustomInput';
export default {
    data() {
        return {
            SingupForm: {
                FullName: '',
                Mobile: '',
                Password: ''
            }
        }
    },
    components: {
        CInput: CustomInput,
    },
    methods: {
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                FullName: this.SingupForm.FullName,
                Mobile: this.SingupForm.Mobile,
                Password: this.SingupForm.Password,
            };
            this.$store.dispatch('signup', payload)
            this.initForm();
        },
        initForm() {
            this.SingupForm.FullName = '';
            this.SingupForm.Mobile = '';
            this.SingupForm.Password = '';
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