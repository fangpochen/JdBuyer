delete __dirname
delete __filenames

window = global
Window = function(){}
window.__proto__ = Window.prototype


HTMLAllCollection=function() {}
window.HTMLAllCollection = HTMLAllCollection;

window.Element=function(){}



location = {
    "ancestorOrigins": {},
    "href": "https://item.jd.com/100012253044.html",
    "origin": "https://item.jd.com",
    "protocol": "https:",
    "host": "item.jd.com",
    "hostname": "item.jd.com",
    "port": "",
    "pathname": "/100012253044.html",
    "search": "",
    "hash": ""
}


document={
    querySelector:function(ele){
        console.log('document querySelector:::',ele)
    },
    createElement:function(ele){
        console.log('document createElement:::',ele)
        if (ele == 'script'){
            return {}
        }
        if (ele == 'canvas'){
            return {}
        }
    },
    getElementById:function(ele){
        console.log('document getElementById:::',ele)
    },
    createEvent:function(ele){
        console.log('document createEvent:::',ele)
    },
    cookie: '',
    head: {childElementCount:42},
    body: {childElementCount:25},
    all: {},
    documentElement: {
        getAttribute:function(){}
    },
    getElementsByTagName:function(ele){
        console.log('document getElementsByTagName:::',ele)
        if (ele == 'head'){
            return []
        }
    }

}
document.all.__proto__ = HTMLAllCollection.prototype



navigator = {
    appName: "Netscape",
    appVersion: '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    platform: "Win32",
    product: "Gecko",
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
    language: "zh-CN",
    languages: [
        "zh-CN",
        "en",
        "en-GB",
        "en-US"
    ],
    plugins: {
        length:5
    },
    webdriver: false,
    hardwareConcurrency: 8,
}




localStorage = {}
localStorage.getItem = function (ele){
    console.log("[native code] localStorage getItem:::",ele)
    return this[ele]
};

xuxulog=console.log
console.log=function(){}