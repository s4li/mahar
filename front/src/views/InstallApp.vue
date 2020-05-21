<template>
<div>
    <Header title="آموزش نصب اپلیکیشن"></Header>
    <router-link class="back-btn" to="/login"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" appear>
        <div class="container" v-if="show">
            <div class="row">
                <div class="col-12 p-0">
                    <div class="appInstallPar">
                        <div class="appInstallTitle">
                            <img class="installmodallogo" src="@/assets/image/logos/96.png" alt="لوگو مهار">
                            <h5 class="installmodal"> راهنمای نصب وب اپلیکیشن <span> عربی مهار </span> برای دستگاه های مختلف در مرورگر کروم</h5>
                        </div>
                        <div class="appInstallContent">
                            <div>
                                <a class="btn btn-link m-2" href="#IOS">IOS</a>
                                <a class="btn btn-link m-2" href="#Android">Android</a>
                                <a class="btn btn-link m-2" href="#Windows">Windows</a>
                                <a class="btn btn-link m-2" href="#Mac">Mac</a>
                            </div>
                            <div class="pb-3 pb-md-0 mb-1">
                                <div class="row">
                                    <div id="IOS" class="col-12 col-lg-6">
                                        <div class="appInstallContex">
                                            <div><img src="@/assets/image/ios.png" alt="ios logo"></div>
                                            <div class="installtext">
                                                <h4>راهنمای نصب برای IOS</h4>
                                                <p>۱ - در نوار پایین دکمه <img class="appInstallIOSImg" src="@/assets/image/share.png" alt="IOS Action (Share) icon"> <span>" Share "</span> را انتخاب کنید.</p>
                                                <p>۲ - سپس منو باز شده را به چپ بکشید و گزینه <img class="appInstallIOSImg" src="@/assets/image/Add.png" alt="IOS Add icon"> <span>" Add to home screen "</span> را انتخاب کنید.</p>
                                                <p>۳ - در مرحله بعد در قسمت بالا روی <span>" Add "</span>  کلیک کنید.</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div id="Android" class="col-12 col-lg-6">
                                        <div class="appInstallContex">
                                            <div><img src="@/assets/image/Android.png" alt="Android logo"></div>
                                            <div class="installtext">
                                                <h4>راهنمای نصب برای Android</h4>
                                                <p>۱ - برای نصب برنامه روی دکمه <i class='far fa-ellipsis-v' style='font-size:18px;vertical-align: middle;'></i> در قسمت بالا سمت راست مرورگر کلیک کنید.</p>
                                                <p>۲ - از درون پنجره باز شده بر روی دکمه <span>" Add To Home Screen "</span>  کلیک کنید.</p>
                                                <p>۳ - از درون پنجره باز شده بر روی دکمه <span>" Add "</span>  کلیک کنید.</p>
                                                <p>۴ - برنامه به صورت خودکار به صفحه اصلی موبایل شما اضافه می شود.</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div id="Windows" class="col-12 col-lg-6">
                                        <div class="appInstallContex">
                                            <div><img src="@/assets/image/Windows.png" alt="Windows logo"></div>
                                            <div class="installtext">
                                                <h4>راهنمای نصب برای Windows</h4>
                                                <p>۱ - برای نصب برنامه روی دکمه <i class='far fa-ellipsis-v' style='font-size:18px;vertical-align: middle;'></i> در قسمت بالا سمت راست مرورگر کلیک کنید.</p>
                                                <p>۲ - از درون پنجره باز شده بر روی دکمه <span>" Install مرکز هوشمند سازی آموزش های دیجیتال "</span>  کلیک کنید.</p>
                                                <p>همچنین می توانید با زدن دکمه <i class='fal fa-plus-circle' style='font-size:18px;vertical-align: middle;'></i> در قسمت ادرس سایت این کار را انجام دهید.</p>
                                                <p>۳ - از درون پنجره باز شده بر روی دکمه <span>" Install "</span> کلیک کنید.</p>
                                                <p>۴ - برنامه به صورت خودکار به دسکتاپ شما اضافه می شود.</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div id="Mac" class="col-12 col-lg-6">
                                        <div class="appInstallContex">
                                            <div><img src="@/assets/image/apple.png" alt="Mac logo"></div>
                                            <div class="installtext">
                                                <h4>راهنمای نصب برای MAC</h4>
                                                <p>۱ - برای نصب برنامه روی دکمه <i class='far fa-ellipsis-v' style='font-size:18px;vertical-align: middle;'></i> در قسمت بالا سمت راست مرورگر کلیک کنید.</p>
                                                <p>۲ - از درون پنجره باز شده بر روی دکمه <span>" Install مرکز هوشمند سازی آموزش های دیجیتال "</span>  کلیک کنید.</p>
                                                <p>همچنین می توانید با زدن دکمه <i class='fal fa-plus-circle' style='font-size:18px;vertical-align: middle;'></i> در قسمت ادرس سایت این کار را انجام دهید.</p>
                                                <p>۳ - از درون پنجره باز شده بر روی دکمه <span>" Install "</span> کلیک کنید.</p>
                                                <p>۴ - برنامه به صورت خودکار به دسکتاپ شما اضافه می شود.</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <router-link to="/login" class="btn btn-warning my-3 w-50 mx-auto">متوجه شدم</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
    components: {
        Header
    },
    data() {
        return {
            data: this.$store.state.InstallAppData,
            show: true
        }
    },
    methods: {
        open() {
            this.data.prompt();
            this.$store.state.InstallAppStatus = false
            this.data.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2HS prompt');
                } else {
                    console.log('User dismissed the A2HS prompt');
                    this.$store.state.InstallAppFlag = false
                }
                this.$store.state.InstallAppData = null
            });
        },
    },
}
</script>

<style>
html {
    scroll-behavior: smooth;
}
.btn-link:hover,.btn-link:active {
    color: #0056b3;
    text-decoration: none;
}
.appInstallContex {
    display: flex;
    justify-content: right;
    text-align: right;
    padding: 15px;
    margin: 15px 0;
    border-radius: 4px;
}

.appInstallContex img {
    width: 60px;
    height: auto;
    background: #fff;
    margin-left: 5px;
}

.appInstallIOSImg {
    width: 15px !important;
    height: auto!important;
    background: #f5f5f5!important;
    margin: 0 5px!important;
}

.appInstallContex span {
    font-weight: 600;
}

.appInstallPar {
    border: 1px solid #f8f8f8;
    border-radius: 4px;
    margin-top: 10%;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.233);
    text-align: center;
}

.appInstallTitle {
    display: flex;
    justify-content: right;
    align-items: center;
    padding: 15px;
    background: #f8f9fa;
    border-bottom: 1px solid #e4e4e4;
}

.appInstallContent {
    padding: 15px;
    background: #ffffff;
}

.installmodal {
    width: 100%;
    padding: 10px;
    font-weight: 600;
    font-size: 16px;
    margin: 0;
    line-height: 30px;
}

.installmodal span {
    color: #dea701;
}

.installtext {
    padding: 0 10px;
}

.installtext h4 {
    font-size: 15px;
    font-weight: 600;
}

.installtext p {
    font-size: 13px;
    margin-bottom: 10px;
    line-height: normal;
}

.installmodallogo {
    width: 40px;
    border-radius: 10px;
}

@media (max-width: 992px) {
    .installmodal {
        padding: 0;
        line-height: 32px;
        font-size: 15px;
        padding-right: 5px;
    }

    .appInstallContent {
        padding: 0;
    }

    .appInstallContex {
        padding-left: 0;
        margin: 0;
        border-bottom: 1px solid #e2e2e2;
    }
}
</style>
