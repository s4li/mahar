<template>
<div>
    <Header title="بازیابی رمز عبور"></Header>
    <router-link class="back-btn" to="/login"><i class='fas fa-arrow-left'></i></router-link>
    <div class="outter">

        <transition name="shakeTop">
            <div class="shakeTop alert alert-danger alert-dismissible" v-if="this.$store.state.showAlert" role="alert">
                {{this.$store.state.alerttext}}
                <button type="button" class="close" @click.prevent="close()" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </transition>
        <transition name="shakeTop">
            <div class="shakeTop alert alert-success alert-dismissible" v-if="showsuccessAlert" role="alert">
                {{showsuccessAlertText}}
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
                            <h1 class="lgTitle">بازیابی رمز عبور</h1>
                            <form @submit="SubmitMobile">
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.mobileNumber.$error}">
                                                    <input type="number" @blur="$v.mobileNumber.$touch()" :class="{'has-val':checkingMobile}" class="input100" v-model="mobileNumber" v-on:keyup="checkingValMobile">
                                                    <span class="focus-input100" data-placeholder="شماره موبایل"></span>
                                                </div>
                                                <small class="form-text text-muted">هر شماره موبایل ۱۱ کاراکتر می باشد</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button class="btn box enterBtn w-25 shadow" :disabled="$v.mobileNumber.$invalid" id="loginbtn" type="submit">ورود</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container p-0" v-if="!show">
                <div class="row no-gutters">
                    <div class="col-12 col-lg-8 mx-lg-auto">
                        <div class="inner">
                            <h1 class="lgTitle">ورود</h1>
                            <form @submit="Submitdata">
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2">
                                                    <input type="number" :class="{'has-val':checkingconfirmCode}" class="input100" v-model="confirmCode" v-on:keyup="checkingValCode">
                                                    <span class="focus-input100" data-placeholder="کد تایید"></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="limiter">
                                    <div class="container-login100">
                                        <div class="wrap-login100">
                                            <div class="login100-form validate-form">
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.password.$error}">
                                                    <input type="password" @blur="$v.password.$touch()" :class="{'has-val':checkingPassword}" class="input100" v-model="password" v-on:keyup="checkingValPass">
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
                                                <div class="wrap-input100 validate-input my-2" data-validate="فیلد به درستی پر نشده است" :class="{'alert-validate':$v.repeatPassword.$error}">
                                                    <input type="password" @blur="$v.repeatPassword.$touch()" :class="{'has-val':checkingrepeatPassword}" class="input100" v-model="repeatPassword" v-on:keyup="checkingValrepeatPass">
                                                    <span class="focus-input100" data-placeholder="کلمه عبور"></span>
                                                </div>
                                                <small class="form-text text-muted">تعداد کاراکترها نمی تواند کمتر از ۵ کاراکتر باشد</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button class="btn box enterBtn w-25 shadow" :disabled="$v.$invalid" id="loginbtn" type="submit">ورود</button>
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
import axios from 'axios'
import {
    required,
    minLength,
    maxLength
} from 'vuelidate/lib/validators'
export default {
    data() {
        return {
            mobileNumber: '',
            password: '',
            repeatPassword: '',
            confirmCode: '',
            checkingMobile: false,
            checkingPassword: false,
            checkingrepeatPassword: false,
            checkingconfirmCode: false,
            show: true,
            showsuccessAlert: false,
            showsuccessAlertText: '',
        }
    },
    components: {
        Header
    },
    methods: {
        close() {
            this.$store.state.showAlert = false
        },
        SubmitMobile(evt) {
            evt.preventDefault();
            axios.get('/confirm-mobile', {
                    params: {
                        mobile: this.mobileNumber,
                    }
                })
                .then(() => {
                    this.show = false
                })
                .catch((error) => {
                    if (error.response.status == 401) {
                        this.$store.state.alerttext = error.response.data.result
                        this.$store.state.showAlert = true
                    } else {
                        this.$store.state.alerttext = 'خطای غیرمنتظره'
                        this.$store.state.showAlert = true
                    }
                });
        },
        Submitdata(evt) {
            evt.preventDefault();
            axios.post('/reset-password', {
                    mobile: this.mobileNumber,
                    password: this.password,
                    re_password: this.repeatPassword,
                    confirm_code: this.confirmCode,
                })
                .then((res) => {
                    if (res.status == 200) {
                        this.showsuccessAlertText = res.data.result
                        this.showsuccessAlert = true
                    }
                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 2000)
                })
                .catch((error) => {
                    if (error.response.status == 401) {
                        this.$store.state.alerttext = error.response.data.result
                        this.$store.state.showAlert = true
                    } else {
                        this.$store.state.alerttext = 'خطای غیرمنتظره'
                        this.$store.state.showAlert = true
                    }
                });
        },
        checkingValMobile() {
            if (this.mobileNumber != '') {
                this.checkingMobile = true
            } else {
                this.checkingMobile = false
            }
        },
        checkingValCode() {
            if (this.confirmCode != '') {
                this.checkingconfirmCode = true
            } else {
                this.checkingconfirmCode = false
            }
        },
        checkingValPass() {
            if (this.password != '') {
                this.checkingPassword = true
            } else {
                this.checkingPassword = false
            }
        },
        checkingValrepeatPass() {
            if (this.repeatPassword != '') {
                this.checkingrepeatPassword = true
            } else {
                this.checkingrepeatPassword = false
            }
        },
        initForm() {
            this.mobileNumber = '';
            this.checkingMobile = false
            this.confirmCode = '';
            this.checkingconfirmCode = false
            this.password = '';
            this.checkingPassword = false
            this.repeatPassword = '';
            this.checkingrepeatPassword = false
        },
    },
    validations: {
        mobileNumber: {
            required,
            minlin: minLength(11),
            maxLength: maxLength(11)
        },
        password: {
            required,
            minlin: minLength(5)
        },
        repeatPassword: {
            required,
            minlin: minLength(5)
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

.enterBtn {
    margin: 30px auto;
    min-width: 150px;
    display: block;
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
    padding: 15px;
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
    min-width: 100px;
    margin-bottom: 15px;
}
</style>
