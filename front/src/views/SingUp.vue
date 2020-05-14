<template>
<div>
    <Header title="ثبت نام"></Header>
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

.inner {
    background-color: #ffffffcc;
    border-radius: 4px;
    margin-top: 10%;
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
@media (max-width: 991.8px) {
    .lgTitle {
        display: none;
    }
    .inner {
    margin-top: 20%;
}
}
</style>
