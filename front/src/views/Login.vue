<template>
<div>
    <Header title="ورود"></Header>
    <div class="outter">

        <transition name="shakeTop">
            <div class="shakeTop alert alert-danger alert-dismissible" v-if="this.$store.state.showAlert" role="alert">
                {{this.$store.state.alerttext}}
                <button type="button" class="close" @click.prevent="close()" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </transition>

        <transition name="fadeIn" appear>
        <div class="inner" v-if="show">
            <form @submit="onSubmit">
                <div class="limiter">
                    <div class="container-login100">
                        <div class="wrap-login100">
                            <div class="login100-form validate-form">
                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.LoginForm.Mobile.$error}">
                                    <input type="number" @blur="$v.LoginForm.Mobile.$touch()" :class="{'has-val':checkingMobile}" class="input100" v-model="LoginForm.Mobile" v-on:keyup="checkingValMobile">
                                    <span class="focus-input100" data-placeholder="شماره موبایل"></span>
                                </div>
                                <small class="form-text text-muted">هر شماره موبایل ۱۱ کاراکتر می باشد</small>
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
                                <small class="form-text text-muted">تعداد کاراکترها نمی تواند کمتر از ۵ کاراکتر باشد</small>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="btn-boxl">
                    <router-link to="/Singup" id="singupbtn" class="btn shadow">ثبت نام</router-link>
                    <button class="btn shadow" :disabled="$v.$invalid" id="loginbtn" type="submit">ورود</button>
                    <router-link to="/Guids" id="infobtn" class="btn">راهنمای استفاده</router-link>
                </div>
            </form>
        </div>
        </transition>
    </div>
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
            show : true
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
#infobtn {
    border-radius: 4px;
    background: linear-gradient(145deg, #cbc9c1, #f2efe5);
    box-shadow: 5px 5px 15px #c5c2ba, -5px -5px 15px #fffcf2;
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
    background-color: #ffffffcc;
    border-radius: 4px;
    margin-top: 30%;
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
    background-color: #fbb901;
    min-width: 120px;
    margin-bottom: 15px;
}

/*//////////////////////////////////////////////////////////////////
[ login ]*/

.limiter {
    width: 100%;
    margin: 0 auto;
}

.container-login100 {
    display: -webkit-box;
    display: -webkit-flex;
    display: -moz-box;
    display: -ms-flexbox;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    padding: 15px;
}

.wrap-login100 {
    width: 390px;
}

/*------------------------------------------------------------------
[ Form ]*/

input {
    outline: none;
    border: none;
}

.login100-form {
    width: 100%;
}

/*------------------------------------------------------------------
  [ Input ]*/

.wrap-input100 {
    width: 100%;
    position: relative;
    border-bottom: 2px solid #ffd76a;
}

.input100 {
    font-size: 14px;
    color: #2b2b28;
    line-height: 1.2;
    display: block;
    width: 100%;
    height: 40px;
    background: transparent;
    padding: 0 5px;
}

/*---------------------------------------------*/

.focus-input100 {
    position: absolute;
    display: block;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
}

.focus-input100::before {
    content: "";
    display: block;
    position: absolute;
    bottom: -2px;
    right: 0;
    width: 0;
    height: 2px;
    -webkit-transition: all 0.4s;
    -o-transition: all 0.4s;
    -moz-transition: all 0.4s;
    transition: all 0.4s;
    background: #fbb901;
}

.focus-input100::after {
    font-size: 14px;
    color: #2b2b28;
    line-height: 1.2;
    content: attr(data-placeholder);
    display: block;
    width: 100%;
    position: absolute;
    top: 10px;
    left: 0px;
    padding-left: 5px;
    -webkit-transition: all 0.4s;
    -o-transition: all 0.4s;
    -moz-transition: all 0.4s;
    transition: all 0.4s;
}

.input100:focus+.focus-input100::after {
    top: -18px;
    font-size: 14px;
}

.input100:focus+.focus-input100::before {
    width: 100%;
}

.has-val.input100+.focus-input100::after {
    top: -18px;
    font-size: 14px;
}

.has-val.input100+.focus-input100::before {
    width: 100%;
}

/*------------------------------------------------------------------
[ Alert validate ]*/

.validate-input {
    position: relative;
}

.alert-validate::before {
    content: attr(data-validate);
    position: absolute;
    max-width: 70%;
    background-color: #fff;
    border: 1px solid #dc3545;
    border-radius: 2px;
    padding: 4px 10px 4px 25px;
    top: 50%;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
    left: 0px;
    pointer-events: none;
    color: #dc3545;
    font-size: 13px;
    line-height: 1.4;
    text-align: left;
    visibility: hidden;
    opacity: 0;
    -webkit-transition: opacity 0.4s;
    -o-transition: opacity 0.4s;
    -moz-transition: opacity 0.4s;
    transition: opacity 0.4s;
}

.alert-validate::after {
    content: "\f06a";
    font-family: "Font Awesome 5 Pro";
    font-size: 14px;
    color: #dc3545;
    display: block;
    position: absolute;
    background-color: #fff;
    top: 50%;
    -webkit-transform: translateY(-50%);
    -moz-transform: translateY(-50%);
    -ms-transform: translateY(-50%);
    -o-transform: translateY(-50%);
    transform: translateY(-50%);
    left: 5px;
}

.alert-validate:hover:before {
    visibility: visible;
    opacity: 1;
}

@media (max-width: 992px) {
    .alert-validate::before {
        visibility: visible;
        opacity: 1;
    }
}
</style>
