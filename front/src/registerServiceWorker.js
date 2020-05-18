/* eslint-disable no-console */

import { register } from 'register-service-worker'

if (process.env.NODE_ENV === 'production') {
  register(`${process.env.BASE_URL}service-worker.js?v2`, {
    registrationOptions: { scope: '/' },
    ready (registration) {
      console.log(
        'App is being served from cache by a service worker.',registration
      )
    },
    registered (registration) {
      console.log('Service worker has been registered.',registration)
    },
    cached (registration) {
      console.log('Content has been cached for offline use.',registration)
    },
    updatefound (registration) {
      console.log('New content is downloading.',registration)
    },
    updated (registration) {
      console.log('New content is available; Refresh...',registration)
      let worker = registration.waiting
      worker.postMessage({action: 'skipWaiting'})
      setTimeout(() => {
        window.location.reload(true)
      }, 1000)
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
}