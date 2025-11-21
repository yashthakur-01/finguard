const originalError = console.error;
console.error = (...args) => {
    if (/ResizeObserver loop/.test(args[0])) {
        return;
    }
    originalError.call(console, ...args);
};

window.addEventListener('error', (e) => {
    const msg = e.message || (e.error && e.error.message) || (typeof e === 'string' ? e : '');
    if (msg && /ResizeObserver loop/.test(msg)) {
        e.stopImmediatePropagation();
        e.preventDefault();
    }
});

window.addEventListener('unhandledrejection', (e) => {
    const msg = e.reason?.message || (typeof e.reason === 'string' ? e.reason : '');
    if (msg && /ResizeObserver loop/.test(msg)) {
        e.stopImmediatePropagation();
        e.preventDefault();
    }
});
