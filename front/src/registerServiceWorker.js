  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js?v2', {
        scope: '.'
    }).then(function(registration) {
        console.log(registration);
    }, function(err) {
        console.log(err);
    });
}