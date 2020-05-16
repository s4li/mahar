<template>
<div>
    <Header title="ورود"></Header>
    <transition name="shakeTop">
        <div class="shakeTop alert alert-danger alert-dismissible" v-if="this.$store.state.showAlert" role="alert">
            {{this.$store.state.alerttext}}
            <button type="button" class="close" @click.prevent="close()" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    </transition>
    <transition name="fadeIn" appear>
        <div class="container p-0" v-if="show">
            <div class="row no-gutters">
                <div class="col-12 col-lg-8 mx-lg-auto">
                    <div class="inner">
                        <h1 class="lgTitle">ورود</h1>
                        <form @submit="onSubmit">
                            <div class="limiter">
                                <div class="container-login100">
                                    <div class="wrap-login100">
                                        <div class="login100-form validate-form">
                                            <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.LoginForm.Mobile.$error}">
                                                <input type="number" @blur="$v.LoginForm.Mobile.$touch()" :class="{'has-val':checkingMobile}" class="input100" v-model="LoginForm.Mobile" v-on:keyup="checkingValMobile">
                                                <span class="focus-input100" data-placeholder="شماره موبایل"></span>
                                            </div>
                                            <small class="form-text text-muted">هر شماره موبایل ۱۱ کاراکتر می باشد.</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="limiter">
                                <div class="container-login100">
                                    <div class="wrap-login100">
                                        <div class="login100-form validate-form">
                                            <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.LoginForm.Password.$error}">
                                                <input type="password" @blur="$v.LoginForm.Password.$touch()" :class="{'has-val':checkingPass}" class="input100" v-model="LoginForm.Password" v-on:keyup="checkingValPass">
                                                <span class="focus-input100" data-placeholder="کلمه عبور"></span>
                                            </div>
                                            <small class="form-text text-muted">تعداد کاراکتر های کلمه عبور ۵ تا یا بیشتر باشد.</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button class="btn enterBtn w-25 shadow" :disabled="$v.$invalid" id="loginbtn" type="submit">ورود</button>
                            <div class="btn-boxl">
                                <router-link to="/Singup" id="singupbtn" class="btn btn-sm shadow">ثبت نام</router-link>
                                <router-link to="/Recovery" class="btn btn-sm btn-outline-primary shadow">بازیابی رمز عبور</router-link>
                                <router-link to="/Guids" class="btn btn-sm btn-outline-secondary shadow">راهنمای استفاده</router-link>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
import {
    required,
    minLength,
    maxLength
} from 'vuelidate/lib/validators'
export default {
    data() {
        return {
            LoginForm: {
                Mobile: '',
                Password: ''
            },
            checkingPass: false,
            checkingMobile: false,
            show: true
        }
    },
    components: {
        Header
    },
    methods: {
        close() {
            this.$store.state.showAlert = false
        },
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                Mobile: this.LoginForm.Mobile,
                Password: this.LoginForm.Password,
            };
            if (payload.Mobile && payload.Password != '') {
                this.$store.dispatch('login', {
                    Mobile: payload.Mobile,
                    Password: payload.Password
                })
            }
        },
        checkingValPass() {
            if (this.LoginForm.Password != '') {
                this.checkingPass = true
            } else {
                this.checkingPass = false
            }
        },
        checkingValMobile() {
            if (this.LoginForm.Mobile != '') {
                this.checkingMobile = true
            } else {
                this.checkingMobile = false
            }
        },
        initForm() {
            this.LoginForm.Mobile = '';
            this.LoginForm.Password = '';
            this.checkingPass = false
            this.checkingMobile = false
        },
    },
    validations: {
        LoginForm: {
            Mobile: {
                required,
                minlin: minLength(11),
                maxLength: maxLength(11)
            },
            Password: {
                required,
                minlin: minLength(5)
            },
        },
    },
    created() {
        this.$store.state.showAlert = false
    },
}
</script>

<style lang="css" scoped>
.lgTitle {
    display: block;
    font-size: 18px;
    text-align: center;
    padding: 20px;
    font-weight: 600;
    margin: 0;
}

.enterBtn {
    margin: 10px auto;
    min-width: 110px;
    display: block;
    padding: 4px;
}

#loginbtn {
    background-color: #fbb901;
}

#singupbtn {
    border: 1px solid #fbb901;
    background: #faf9f6;
}

.inner {
    background-color: #ffffffcc;
    border-radius: 4px;
    margin-top: 10%;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.233);
}

.btn-boxl {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: wrap;
    padding: 15px;
}

.btn-boxl button,
.btn-boxl a {
    min-width: 110px;
    margin-bottom: 15px;
}
@media (max-width: 991.8px) {
    .lgTitle {
        display: none;
    }
    .inner{
        margin-top: 25%;
    }
}
</style>
