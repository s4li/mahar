<template>
<router-link to="/login">
    <div class="home">
        <div class="container h-100">
            <div class="row h-100">
                <div class="col-12 h-100">
                    <div class="welcome">
                        <div>
                            <div id="logo">
                                <img src="../assets/image/flip-pen.png" alt="">
                                <img src="../assets/image/amar.png" alt="">
                                <img src="../assets/image/pen.png" alt="">
                            </div>
                            <h1>دنیا کوچیکه زود میرسه</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</router-link>
</template>

<style>
.home {
    height: 100%;
    width: 100%;
}

.welcome {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

#logo {
    padding: 90px 20px;
    background: #fff;
    border-radius: 50%;
}

#logo img {
    max-width: 190px;
    background: #fff;
    height: auto;
    display: block;
    margin: auto;
}

.welcome h1 {
    color: #fff;
    font-size: 22px;
    text-align: center;
    margin: 20px;
    font-weight: 600;
}

#app {
    height: 100%;
}
</style>
