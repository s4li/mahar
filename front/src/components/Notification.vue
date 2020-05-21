<template>
<div>
    <div class="tooltip b-tooltip bs-tooltip-top bs-tooltip-top-docs" role="tooltip">
        <div class="arrow"></div>
        <div class="tooltip-inner">آموزش نصب اپلیکیشن</div>
    </div>
    <div class="bell-icon" tabindex="0">
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="50px" height="30px" viewBox="0 0 50 30" enable-background="new 0 0 50 30" xml:space="preserve">
            <g class="bell-icon__group">
                <path class="bell-icon__ball" id="ball" fill-rule="evenodd" stroke-width="1.5" clip-rule="evenodd" fill="none" stroke="#currentColor" stroke-miterlimit="10" d="M28.7,25 c0,1.9-1.7,3.5-3.7,3.5s-3.7-1.6-3.7-3.5s1.7-3.5,3.7-3.5S28.7,23,28.7,25z" />
                <path class="bell-icon__shell" id="shell" fill-rule="evenodd" clip-rule="evenodd" fill="#FFFFFF" stroke="#currentColor" stroke-width="2" stroke-miterlimit="10" d="M35.9,21.8c-1.2-0.7-4.1-3-3.4-8.7c0.1-1,0.1-2.1,0-3.1h0c-0.3-4.1-3.9-7.2-8.1-6.9c-3.7,0.3-6.6,3.2-6.9,6.9h0 c-0.1,1-0.1,2.1,0,3.1c0.6,5.7-2.2,8-3.4,8.7c-0.4,0.2-0.6,0.6-0.6,1v1.8c0,0.2,0.2,0.4,0.4,0.4h22.2c0.2,0,0.4-0.2,0.4-0.4v-1.8 C36.5,22.4,36.3,22,35.9,21.8L35.9,21.8z" />
            </g>
        </svg>
        <div class="notification-amount" v-if="this.$store.state.InstallAppFlag">
            <span>!</span>
        </div>
    </div>
</div>
</template>

<script>
export default {

}
</script>

<style>
.bd-example-tooltip-static .tooltip {
    position: relative;
    display: inline-block;
    margin: 10px 20px;
    opacity: 1;
}

.bs-tooltip-auto[x-placement^=top],
.bs-tooltip-top {
    padding: .4rem 0;
}

.tooltip {
    position: absolute;
    z-index: 1070;
    margin: 0;
    width: 80px;
    left: -5px;
    top: -50px;
    display: block;
    opacity: .9;
    outline: 0;
    animation-name: bounce;
    animation-delay: 1000ms;
}

.bs-tooltip-auto[x-placement^=top] .arrow,
.bs-tooltip-top .arrow {
    bottom: 0;
}

.tooltip .arrow {
    position: absolute;
    display: block;
    width: .8rem;
    height: .4rem;
}

.tooltip-inner {
    max-width: 200px;
    padding: 5px;
    color: #fff;
    text-align: center;
    background-color: #000;
    border-radius: .25rem;
}

.tooltip.b-tooltip .arrow {
    margin: 0 .25rem;
}

.bs-tooltip-auto[x-placement^=top] .arrow,
.bs-tooltip-top .arrow {
    bottom: 0;
}

.tooltip .arrow {
    position: absolute;
    display: block;
    width: .8rem;
    height: .4rem;
    left: 30px;
}

.tooltip .arrow:before {
    position: absolute;
    content: "";
    border-color: transparent;
    border-style: solid;
}

.bs-tooltip-auto[x-placement^=top] .arrow:before,
.bs-tooltip-top .arrow:before {
    top: 0;
    border-width: .4rem .4rem 0;
    border-top-color: #000;
}

.bell-icon {
    position: relative;
    width: 70px;
    height: 70px;
    background: rgb(247, 247, 247);
    border-radius: 50%;
    display: flex;
    box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.233);
    outline: none;
}

.bell-icon svg {
    margin: auto;
    position: relative;
    right: 2%;
    width: 90%;
    height: 90%;
    stroke: rgba(0, 0, 0, 0.75);
}

.bell-icon .bell-icon__group {
    transform-origin: 50% 2px;
    transform: rotate(-8deg);
    animation-fill-mode: both;
    animation-iteration-count: 1;
    animation-timing-function: ease-in-out;
    animation-delay: 1000ms;
}

.bell-icon .bell-icon__ball {
    transform-origin: 50% 2px;
    transform: translateX(-6.5%);
    animation-fill-mode: both;
    animation-iteration-count: 1;
    animation-timing-function: ease-in-out;
    animation-delay: 1000ms;
}

.bell-icon .bell-icon__group {
    animation: animateGroup 2.3s;
}

.bell-icon .bell-icon__ball {
    animation: animateBall 2.3s;
}

.bell-icon .notification-amount {
    opacity: 1;
    visibility: visible;
}

.bell-icon .notification-amount::before {
    animation-name: bounce;
    animation-delay: 1000ms;
}

.notification-amount {
    opacity: 0;
    visibility: hidden;
    position: absolute;
    top: 20%;
    right: 24%;
    width: 20px;
    height: 20px;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.notification-amount span {
    position: relative;
}

.notification-amount::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: #f72918;
    border-radius: 50%;
    z-index: 0;
    transform: scale(0);
    animation-duration: 800ms;
    animation-fill-mode: both;
}

@keyframes animateGroup {

    0%,
    100% {
        transform: rotate(-8deg);
    }

    17.542% {
        transform: rotate(0deg);
    }

    35.084% {
        transform: rotate(-20deg);
    }

    48.2405% {
        transform: rotate(20deg);
    }

    57.0115% {
        transform: rotate(-20deg);
    }

    64.9054% {
        transform: rotate(8deg);
    }

    74.5535% {
        transform: rotate(-15deg);
    }

    78.939% {
        transform: rotate(-7deg);
    }
}

@keyframes animateBall {

    0%,
    100% {
        transform: translateX(-6.5%);
    }

    17.542% {
        transform: translateX(0%);
    }

    21.9275% {
        transform: translateX(-1%);
    }

    35.084% {
        transform: translateX(11%);
    }

    48.2405% {
        transform: translateX(-11%);
    }

    52.626% {
        transform: translateX(0%);
    }

    59.6428% {
        transform: translateX(10%);
    }

    68.4138% {
        transform: translateX(-11%);
    }

    78.939% {
        transform: translateX(11%);
    }

    85.9558% {
        transform: translateX(-11%);
    }
}

@keyframes bounce {
    0% {
        transform: scale(0);
    }

    14% {
        transform: scale(1.15);
    }

    28% {
        transform: scale(1);
    }

    42% {
        transform: scale(1.15);
    }

    70% {
        transform: scale(1);
    }

    100% {
        transform: scale(1);
    }
}
</style>
