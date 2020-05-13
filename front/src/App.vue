<template>
<div id="app">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <Navbar></Navbar>
                <router-view />
                <div class="installbanner" v-if="showaddBanner">
                    <button class="btn btn-link btn-lg mx-3" @click="closeBanner()">&times;</button>
                    <p> برنامه مهار در دسترس است </p>
                    <button class="btn btn-primary mr-2 btn-sm" @click.prevent="open()">کلیک کنید</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Navbar from '@/components/Navbar'
export default {
    components: {
        Navbar
    },
    data() {
        return {
            showaddBanner: false,
            data: ''
        }
    },
    methods: {
        closeBanner() {
            this.showaddBanner = false
        },
        open() {
            this.data.prompt();
            this.showaddBanner = false
            this.data.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('User accepted the A2HS prompt');
                } else {
                    console.log('User dismissed the A2HS prompt');
                }
                this.data = null;
            });
        }
    },
    created() {
        this.$store.dispatch('tryAutoLogin')
        this.showaddBanner = false
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.data = e
            this.showaddBanner = true
        });
    },
}
</script>

<style>
@import './assets/style/fontawesome.min.css';
@import './assets/style/global.css';

.installbanner {
    background-color: #ffffffcc;
    padding: 10px;
    position: absolute;
    top: 0;
    left: 0px;
    right: 0;
    width: 100%;
}

.installbanner p {
    display: inline-block;
    margin: 0;
}

.installbanner span {
    color: black;
}

.installbanner :hover {
    text-decoration: none;
}

@media (min-width: 992px) {
    .installbanner {
        text-align: center;
    }
}
</style>
