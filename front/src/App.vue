<template>
<div id="app">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <Navbar></Navbar>
                <router-view />
                <router-link v-if="this.$store.state.InstallAppStatus" v-show="InstallAppBtnMobile" class="InstallAppBtnMobile" to="/InstallApp">
                    <Notification></Notification>
                </router-link>
            </div>
        </div>
    </div>
    <!---<div class="installbanner" v-if="showaddBanner">
        <button class="btn btn-link btn-lg mx-3" @click="closeBanner()">&times;</button>
        <p> برنامه مهار در دسترس است </p>
        <button class="btn btn-primary mr-2 btn-sm" @click.prevent="open()">کلیک کنید</button>
    </div>-->
</div>
</template>

<script>
import Notification from '@/components/Notification'
import Navbar from '@/components/Navbar'
export default {
    data() {
        return {
            InstallAppBtnMobile: true,
        }
    },
    components: {
        Navbar,
        Notification
    },
    updated() {
        if (this.$route.path == '/InstallApp' || this.$route.path == '/') {
            this.InstallAppBtnMobile = false
        } else {
            this.InstallAppBtnMobile = true
        }
    },
    created() {
        this.$store.dispatch('tryAutoLogin')
        this.$store.state.InstallAppStatus = false
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            if (this.$store.state.InstallAppFlag) {
                this.$store.state.InstallAppData = e
                this.$store.state.InstallAppStatus = true
            } else {
                this.$store.state.InstallAppData = null
                this.$store.state.InstallAppStatus = false
            }
        });
        window.addEventListener('appinstalled', () => {
            console.log('a2hs installed');
        });
        window.addEventListener('load', () => {
            if (navigator.standalone) {
                console.log('Launched: Installed (iOS)');
            } else if (matchMedia('(display-mode: standalone)').matches) {
                console.log('Launched: Installed');
            } else {
                console.log('Launched: Browser Tab');
            }
        });
    },
}
</script>

<style>
@import './assets/style/fontawesome.min.css';
@import './assets/style/global.css';

.InstallAppBtnMobile {
    position: fixed;
    bottom: 5px;
    left: 10px;
}

.InstallAppBtnMobile img {
    width: 60px;
    height: auto;
    border-radius: 50%;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.233);
}

@media (min-width: 992px) {
    .installbanner {
        text-align: center;
    }

    .InstallAppBtnMobile {
        display: none;
    }
}
</style>
