<template>
<div>
    <header class="header">
        <h1>{{title}}</h1>
    </header>
</div>
</template>

<script>
export default {
    props: ['title']
}
</script>

<style>

.header {
    text-align: center;
    padding: 20px;
    background: #ffba23;  /* fallback for old browsers */
    background: -webkit-linear-gradient(to right, #FFD200, #ffba23);  /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to right, #FFD200, #ffba23); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    color: #f8f9fa;
    margin: 0 -15px;
    position: relative;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.header h1 {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
    padding-top: 5px;
}
</style>
