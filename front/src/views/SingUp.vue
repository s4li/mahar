<template>
<div>
    <Header title="ثبت نام"></Header>
    <div class="outter">
        <div class="inner">
            <form @submit="onSubmit">
                <CInput lable="نام کاربری" @inputdata="SingupForm.FullName=$event"></CInput>
                <CInput lable="کلمه عبور" @inputdata="SingupForm.Password=$event" type="password"></CInput>
                <CInput lable="شماره موبایل" @inputdata="SingupForm.Mobile=$event" type="number"></CInput>
                <div class="btn-box">
                    <button class="btn" :disabled="$v.$invalid" type="submit">ثبت نام</button>
                </div>
            </form>
        </div>
    </div>
</div>
</template>

<script>
import CustomInput from '../components/CustomInput';
import Header from '@/components/Header.vue'
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
        Header
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
    background-color: #f8f9fa99;
    border-radius: 4px;
    margin-top: 20%;
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
