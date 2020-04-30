<template>
<div class="position-relative">
    <transition name="slideout" type="animation" appear>
        <div class="back first" v-if="show">
            <h3>الغیم</h3>
            <button class="btn play" @click.prevent="playSound('https://s3-us-west-2.amazonaws.com/s.cdpn.io/28963/rain.mp3')"><i class="fas fa-volume"></i></button>
            <button class="btn btn-warning" @click.prevent="show=false">معنیش چیه؟</button>
        </div>
    </transition>
    <transition name="slidein" type="animation">
        <div class="back seconde" v-if="!show">
            <h3>ابر</h3>
            <div>
                <button class="btn true"><i class="far fa-check"></i>درسته</button>
                <button class="btn false"><i class="far fa-times"></i>غلطه</button>
            </div>
        </div>
    </transition>
</div>
</template>

<script>
//import axios from 'axios'
export default {
    data() {
        return {
            Courses: [],
            CoursesType: this.$route.params.Type,
            show: true
        }
    },
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
    background: #f8f9fa;
}

.play i {
    vertical-align: middle;
    font-size: 18px;
}

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

.slidein-enter {
    opacity: 0;
}

.slidein-enter-active {
    animation: slide-in 1s ease-in forwards;
    transition: opacity 1s;
}

.slidein-leave {}

.slidein-leave-active {
    animation: slide-out 1s ease-in forwards;
    transition: opacity 1s;

}

.slideout-enter {
    opacity: 0;
}

.slideout-enter-active {
    animation: slide-in 1.5s ease-in forwards;
    transition: opacity 1.5s;
}

.slideout-leave {}

.slideout-leave-active {
    animation: slide-out 1.5s ease-in forwards;
    transition: opacity 1s;

}

@keyframes slide-in {
    from {
        transform: translateY(100px);
    }

    to {
        transform: translateY(0);
    }
}

@keyframes slide-out {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(-100px);
    }
}
</style>
