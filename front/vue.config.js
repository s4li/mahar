module.exports = {
  pwa: {
    //workboxPluginMode: 'InjectManifest',
    workboxPluginMode: 'GenerateSW',
    workboxOptions: {
        //swSrc: 'public/service-worker.js',
        navigateFallback: 'index.html',
        exclude: /\.mp3$/,
    },
    name: 'مرکز هوشمندسازی آموزش های رسانه ای',
    themeColor: '#FFFFFF',
    msTileColor: '#FFFFFF',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'white',
    manifestPath:'manifest.json',
    manifestOptions:{
      name: 'مرکز هوشمندسازی آموزش های رسانه ای',
      short_name: 'مهار عربی',
      start_url: '/',
      background_color: '#fff',
      description: 'مرکز هوشمندسازی آموزش های رسانه ای',
      categories: ['education'],
      display: 'standalone',
      dir: 'rtl',
      lang: 'fa-ir',
      scope: ['/','/Guids','/login','/Singup','/InstallApp','/Grades','/Recovery','/Lessons/','/ExamType/','/Courses/']
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