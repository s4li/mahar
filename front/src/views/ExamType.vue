<template>
<div>
    <Header title="نوع پرسش خود را انتخاب کنید"></Header>
    <div class="btn-box">
        <b-button>پرسش جدید</b-button>
        <b-button>ادامه پرسش قبلی</b-button>
        <b-button>مرور غلط های این بخش</b-button>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
    components: {
        Header
    },
    data() {
        return {}
    },
    computed: {},
    methods: {},
    created() {
        this.$store.dispatch('fetchUser')
    },
}
</script>

<style scoped>
.btn-box {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    margin-top: 30%;
    background-color: #f8f9fa99;
    border-radius: 4px;
}

.btn-box button {
    margin: 10px 0 10px;
    padding: 8px;
    width: 80%;
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
}
</style>
