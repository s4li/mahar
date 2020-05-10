module.exports = {
  pwa: {
    workboxPluginMode:'InjectManifest',
    workboxOptions: {swSrc: "public/service-worker.js"},
    name: 'مرکز هوشمندسازی آموزش های رسانه ای',
    themeColor: '#ffc107',
    msTileColor: '#FFFFFF',
    appleMobileWebAppCapable:'no',
    manifestPath:'manifest.json',
    manifestOptions:{
      name: 'مرکز هوشمندسازی آموزش های رسانه ای',
      short_name: 'مهار',
      start_url: '/',
      background_color: '#fff',
      description: 'مرکز هوشمندسازی آموزش های رسانه ای',
      categories: ['education'],
      display: 'fullscreen',
      dir: 'rtl',
      lang: 'fa-ir',
    },
    iconPaths:{
      favicon32: 'img/icons/favicon-32x32.png',
      favicon16: 'img/icons/favicon-16x16.png',
      appleTouchIcon: 'img/icons/apple-touch-icon-152x152.png',
      maskIcon: 'img/icons/safari-pinned-tab.svg',
      msTileImage: 'img/icons/msapplication-icon-144x144.png'
    }
  }
}