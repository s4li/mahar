<template>
<div>
    <div class="limiter">
        <div class="container-login100">
            <div class="wrap-login100">
                <div class="login100-form validate-form">
                    <div class="wrap-input100 validate-input my-2" data-validate="این فیلد را پر کنید" :class="{'alert-validate':$v.data.$error}">
                        <input :type="type" @blur="$v.data.$touch()" :class="{'has-val':checking}" class="input100" v-model="data" v-on:keyup="emitToParent">
                        <span class="focus-input100" :data-placeholder="lable"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {required} from 'vuelidate/lib/validators'
export default {
    props: {
        lable: {
            type: String
        },
        type: {
            default: 'text'
        }
    },
    data() {
        return {
            data: '',
            checking:false
        }
    },
    methods: {
        emitToParent() {
            this.$emit('inputdata', this.data);
            if( this.data != '' ){
                this.checking = true
            }else{
                this.checking = false
            }
        }
    },
    validations: {
        data: {
            required,
        }
    }
}
</script>

<style lang="css" scoped>
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
