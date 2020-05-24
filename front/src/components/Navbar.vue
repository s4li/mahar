<template>
<nav class="navbar navbar-expand-lg navbar-light">
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <router-link class="nav-link" to="/">خانه</router-link>
            </li>
            <li class="nav-item" v-if="!auth">
                <router-link class="nav-link" to="/login">ورود</router-link>
            </li>
            <li class="nav-item" v-if="!auth">
                <router-link class="nav-link" to="/Singup">ثبت نام</router-link>
            </li>
            <li class="nav-item">
                <router-link class="nav-link" to="/Guids">راهنما</router-link>
            </li>
            <li class="nav-item">
                <router-link v-if="this.$store.state.InstallAppStatus" class="nav-link" to="/InstallApp"><b-badge variant="danger">!</b-badge> آموزش نصب اپلیکیشن </router-link>
            </li>
            <li v-if="auth" class="nav-item">
                <button @click="show=true" class="btn btn-link nav-link">خروج</button>
            </li>
        </ul>
    </div>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <nav class="navbar navbar-light">
        <router-link class="navbar-brand" to="/">
            <span>مهار</span>
            <img src="../assets/image/logos/144.png" width="30" height="30" class="d-inline-block align-top" alt="" loading="lazy">
        </router-link>
    </nav>
    <b-modal v-model="show" id="modal-center" content-class="shadow" hide-footer centered header-bg-variant="danger" headerTextVariant="light">
        <template v-slot:modal-header="{ close }">
            <h5 class="w-100 m-0 text-center">آیا مطمئن هستید؟</h5>
            <b-button class="d-none" size="sm" variant="light" @click="close()"><i style="vertical-align: sub;" class="far fa-times"></i></b-button>
        </template>
        <div class="text-center p-4">
            <button @click="onLogout" class="btn btn-primary w-25 m-3">بله</button>
            <button @click="show=false" class="btn btn-warning w-25 m-3 shadow">خیر</button>
        </div>
    </b-modal>
</nav>
</template>

<script>
export default {
    methods: {
        onLogout() {
            this.$store.dispatch('logout')
            this.show=false
        },
    },
    computed: {
        auth() {
            return this.$store.getters.isAuthenticated
        },

    },
    data() {
        return {
            show: false,
        }
    }
}
</script>

<style>
.navbar {
    margin: 0 -15px;
    padding: 0.4rem 2.5rem;
    background-color: #eeeeee;
}

.navbar-brand span {
    vertical-align: bottom;
    padding: 0 5px;
}

.navbar-nav .nav-item .router-link-exact-active {
    color: rgba(0, 0, 0, 0.9) !important;
}

@media (max-width: 991.99px) {
    .navbar {
        display: none;
    }
}
</style>
