<template>
  <div id="app">
    <div class="container">
      <div class="row">
        <div class="col-12 col-md-12 m-md-auto">
          <router-view/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    created() {
      this.$store.dispatch('tryAutoLogin')
    },
  }
</script>

<style>
  @import './assets/style/fontawesome.min.css';
  @import './assets/style/global.css';
</style>
