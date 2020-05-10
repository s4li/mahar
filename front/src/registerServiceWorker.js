if (process.env.NODE_ENV === 'production') {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register(`${process.env.BASE_URL}service-worker.js?v2`, {
            scope: '/'
        }).then(function(registration) {
            console.log(registration);
        }, function(err) {
            console.log(err);
        });
    }
}