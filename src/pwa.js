// This file was stolen from https://github.com/mdn/dom-examples/tree/main/service-worker/simple-service-worker
// and is licensed under the Creative Commons Zero v1.0 Universal.

// More information under https://www.jhanley.com/blog/pyscript-creating-installable-offline-applications/

const registerServiceWorker = async () => {
    if ('serviceWorker' in navigator) {
        try {
            const registration = await navigator.serviceWorker.register(
                'sw.js',
                {
                    scope: '/',
                }
            );
            if (registration.installing) {
                console.log('Service worker installing');
            } else if (registration.waiting) {
                console.log('Service worker installed');
            } else if (registration.active) {
                console.log('Service worker active');
            }
        } catch (error) {
            console.error(`Registration failed with ${error}`);
        }
    }
};

registerServiceWorker();
