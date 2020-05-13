<template>
<div>
    <Header title="راهنمای برنامه"></Header>
    <router-link class="back-btn" to="/login"><i class='fas fa-arrow-left'></i></router-link>
    <transition name="fadeIn" appear>
        <div class="guidParent" v-if="show">
            <div class="container">
                <div class="row">
                    <div class="col-lg-4 col-md-6 col-12 wrraper" v-for="(item, index) in content" :key="index">
                        <img :src="item.imgPath" alt="">
                        <p>{{index+1 | faNum}} - {{ item.text }}</p>
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
            content: [{
                    imgPath: require('@/assets/image/guidImage/1.png'),
                    text: 'وقتی وارد برنامه می شوید با صفحه ثبت نام و ورود روبرو می شوید که در صورت ثبت نام، روی ورود کلیک کرده و اطلاعات خودتان را وارد کنید و اگر ثبت نام نکرده اید باید روی ثبت نام کلیک کرده و اطلاعاتتان را وارد کنید.'
                },
                {
                    imgPath: require('@/assets/image/guidImage/2.jpg'),
                    text: 'پس از انتخاب پایه، درس های مربوطه برای شما باز می شود که می توانید روی یکی از درس ها کلیک کرده و سپس از کلمات آن درس استفاده کنید.'
                },
                {
                    imgPath: require('@/assets/image/guidImage/3.jpg'),
                    text: 'پس از وارد شدن به هر پایه، کلمات یک درس به صورت رایگان بوده و باقی دروس را با پرداخت هزینه می توانید استفاده کنید.'
                },
                {
                    imgPath: require('@/assets/image/guidImage/4.jpg'),
                    text: "پس از کلیک روی هر درس وارد این صفحه خواهید شد، که می توانید با زدن روی 'معنیش چیه؟' معنی کلمه رو ببینید و برای خودتان مشخص کنید آیا معنی رو درست جواب دادید یا خیر.و با زدن روی علامت بلندگو میتوانید کلمه را با تلفظ عربی گوش کنید"
                },
                {
                    imgPath: require('@/assets/image/guidImage/5.jpg'),
                    text: 'با کلیک روی پرسش جدید می توانید از اول در پرسش جدید شرکت کنید و کل کلمات یک درس را از خودتان آزمون بگیرید. شما خودتان می توانید صحیح یا غلط بودن پاسختان را مشخص کنید. با کلیک روی ادامه ی پرسش قبلی می توانید به پرسشی که از قبل شروع کرده بودید ادامه دهید.'
                },
                {
                    imgPath: require('@/assets/image/guidImage/6.jpg'),
                    text: "و با زدن روی 'مرور غلط های این بخش' می توانید نتیجه پرسش خودتان رو در این صفحه ببینید که مشخص شده شما چند کلمه رو به درستی و چند کلمه رو غلط جواب دادید و از این صفحه هم می توانید با زدن روی 'آزمون ها'، مجدد غلط های خودتان را مرور کنید و حتی اگر غلطی نداشتید روی 'پایه ها' کلیک کنید و وارد صفحه پایه ها شوید و دیگر پایه ها و دوری را انتخاب کنید."
                },
                {
                    imgPath: require('@/assets/image/guidImage/7.jpg'),
                    text: 'در انتها خرید یک پایه یا کل پایه ها را داریم که شما در این صفحه با انتخاب گزینه مورد نظر به صفحه پرداخت منتقل میشوید و می توانید خرید خودتان را انجام دهید.'
                },
            ],
            show: true
        }
    },
}
</script>

<style>
.guidParent {
    margin: 15px 0;
    text-align: center;
}

.wrraper {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #ffffffcc;
    border-radius: 4px;
    box-shadow: 0 3px 10px #cccccc;
}

.wrraper img {
    width: 100%;
    height: auto;
    border-radius: 4px;
    max-width: 400px;
}

.wrraper p {
    margin: 10px 0;
    font-size: 13px;
    line-height: 20px;
}
</style>
