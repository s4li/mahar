<template>
<div class="position-relative">
    <div class="back first show-box">
        <h3>الغیم</h3>
        <button class="btn play" @click.prevent="playSound('http://soundbible.com/mp3/Elevator Ding-SoundBible.com-685385892.mp3')"><i class="fas fa-volume"></i></button>
        <button class="btn btn-warning">معنیش چیه؟</button>
    </div>
    <div class="back seconde ">
        <h3>ابر</h3>
        <div>
            <button class="btn true"><i class="far fa-check"></i>درسته</button>
            <button class="btn false"><i class="far fa-times"></i>غلطه</button>
        </div>
    </div>
</div>
</template>

<script>
//import axios from 'axios'
export default {
    //data() {
    //    return {
    //        Courses: [],
    //        CoursesType: this.$route.params.Type,
    //
    //    }
    //},
    methods: {
        //    getCourses() {
        //        axios.get('/courses')
        //            .then((res) => {
        //                this.Courses = res.data;
        //            })
        //            .catch((error) => {
        //                console.error(error);
        //            });
        //    },
        playSound(sound) {
            if (sound) {
                var audio = new Audio(sound);
                audio.play();
            }
        }
    },
    //created() {
    //    this.getCourses();
    //},
}
</script>

<style lang="css">
.back {
    padding: 15px;
    margin-top: 30%;
    background-color: #f8f9facc;
    border-radius: 4px;
    text-align: center;
}

.play {
    display: block;
    margin: 15px auto;
    padding: 8px 12px;
    border: 1px solid #909090;
    background: #fff;
}

.play i {
    vertical-align: middle;
    font-size: 18px;
}

.first {}

.seconde {}

.true {
    padding: 5px 15px;
    background-color: #28a745;
    margin: 10px 10px 0;
    color: #ffffff;
}

.true i,
.false i {
    width: 15px;
    text-align: right;
    vertical-align: middle;
}

.false {
    padding: 5px 15px;
    background-color: #dc3545;
    margin: 10px 10px 0;
    color: #ffffff;
}

.show-box {
    display: block;
}

.hidden-box {
    display: none;
}
</style>
