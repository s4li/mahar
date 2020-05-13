<template>
<div>
    <Header title="ثبت نام"></Header>
    <div class="outter">
        <router-link class="back-btn" to="/login"><i class='fas fa-arrow-left'></i></router-link>
        <transition name="shakeTop">
            <div class="shakeTop alert alert-danger alert-dismissible" v-if="this.$store.state.showAlert" role="alert">
                {{this.$store.state.alerttext}}
                <button type="button" class="close" @click.prevent="close()" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </transition>

        <transition name="fadeIn" appear>
            <div class="container" v-if="show">
                <div class="row">
                    <div class="col-12 col-lg-8 mx-lg-auto">
                        <div class="inner">
                            <h1 class="lgTitle">ورود</h1>
                            <form @submit="onSubmit">
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.SingupForm.FullName.$error}">
                                                    <input type="text" @blur="$v.SingupForm.FullName.$touch()" :class="{'has-val':checkingName}" class="input100" v-model="SingupForm.FullName" v-on:keyup="checkingValName">
                                                    <span class="focus-input100" data-placeholder="نام کاربری"></span>
                                                </div>
                                                <small class="form-text text-muted">تعداد کاراکترها نمی تواند کمتر از ۵ کاراکتر باشد</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.SingupForm.Password.$error}">
                                                    <input type="password" @blur="$v.SingupForm.Password.$touch()" :class="{'has-val':checkingPass}" class="input100" v-model="SingupForm.Password" v-on:keyup="checkingValPass">
                                                    <span class="focus-input100" data-placeholder="کلمه عبور"></span>
                                                </div>
                                                <small class="form-text text-muted">تعداد کاراکترها نمی تواند کمتر از ۵ کاراکتر باشد</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.SingupForm.Mobile.$error}">
                                                    <input type="number" @blur="$v.SingupForm.Mobile.$touch()" :class="{'has-val':checkingMobile}" class="input100" v-model="SingupForm.Mobile" v-on:keyup="checkingValMobile">
                                                    <span class="focus-input100" data-placeholder="شماره موبایل"></span>
                                                </div>
                                                <small class="form-text text-muted">هر شماره موبایل ۱۱ کاراکتر می باشد</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="btn-box1">
                                    <button class="btn shadow" :disabled="$v.$invalid" type="submit">ثبت نام</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
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
            SingupForm: {
                FullName: '',
                Mobile: '',
                Password: ''
            },
            checkingName: false,
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
                FullName: this.SingupForm.FullName,
                Mobile: this.SingupForm.Mobile,
                Password: this.SingupForm.Password,
            };
            if (payload.Mobile && payload.Password && payload.FullName != '') {
                this.$store.dispatch('signup', {
                    Mobile: payload.Mobile,
                    Password: payload.Password,
                    FullName: payload.FullName
                })
            }
        },
        initForm() {
            this.SingupForm.FullName = '';
            this.SingupForm.Mobile = '';
            this.SingupForm.Password = '';
            this.checkingName = false
            this.checkingPass = false
            this.checkingMobile = false
        },
        checkingValName() {
            if (this.SingupForm.FullName != '') {
                this.checkingName = true
            } else {
                this.checkingName = false
            }
        },
        checkingValPass() {
            if (this.SingupForm.Password != '') {
                this.checkingPass = true
            } else {
                this.checkingPass = false
            }
        },
        checkingValMobile() {
            if (this.SingupForm.Mobile != '') {
                this.checkingMobile = true
            } else {
                this.checkingMobile = false
            }
        }
    },
    validations: {
        SingupForm: {
            Mobile: {
                required,
                minlin: minLength(11),
                maxLength: maxLength(11)
            },
            Password: {
                required,
                minlin: minLength(5)
            },
            FullName: {
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

@media (max-width: 991.8px) {
    .lgTitle {
        display: none;
    }
}

.outter {
    padding: 15px;
}

.inner {
    background-color: #ffffffcc;
    border-radius: 4px;
    margin-top: 20%;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.233);
}

.btn-box1 {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    flex-wrap: wrap;
    padding: 15px;
}

.btn-box1 button,
.btn-box1 a {
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
