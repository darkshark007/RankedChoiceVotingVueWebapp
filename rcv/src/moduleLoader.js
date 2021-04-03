// Single-File-Component Loader
//   https://github.com/FranckFreiburger/vue3-sfc-loader

const { loadModule, vueVersion } = window['vue2-sfc-loader'];
// const { defineAsyncComponent } = window['Vue'];
const options = {
    moduleCache: {
        vue: Vue,
        myData: {
            vueVersion,
        }
    },
    getFile: async (url) => {
        return fetch(url).then(res => res.text());
    },
    addStyle(textContent) {
        const style = Object.assign(document.createElement('style'), { textContent });
        const ref = document.head.getElementsByTagName('style')[0] || null;
        document.head.insertBefore(style, ref);
    },
}

export default function loadComponent(path) {
    return () => loadModule(path, options); // Vue2-SFC-Loader
    // return defineAsyncComponent(() => loadModule(path, options)); // Vue3-SFC-Loader
}