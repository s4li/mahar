<template>
<div>
    <Header title="نوع آزمون خود را انتخاب کنید"></Header>
    <div class="btn-box">
        <router-link to="/Courses/check_new_question">پرسش جدید</router-link>
        <router-link to="/Courses/review_previous_questions">ادامه پرسش قبلی</router-link>
        <router-link to="/Courses/check_wrong_questions">مرور غلط های این بخش</router-link>
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'
export default {
    components: {
        Header
    }
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

.btn-box button,
.btn-box a {
    margin: 10px 0 10px;
    padding: 8px;
    width: 80%;
    color: #212529;
    background-color: #ffc107;
    border-color: #ffc107;
}
</style>
