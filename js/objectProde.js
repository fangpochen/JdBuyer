delete __dirname
delete __filename
const CryptoJS = require("crypto-js");

function watch(obj, name) {
    return new Proxy(obj, {
        get: function(target, property, receiver) {
            try {
                if (typeof target[property] === 'function') {
                    console.log("对象 =>" + name + ",读取属性:" + property + "(), 值为:" + target[property] + ", 类型:" + typeof target[property])
                    return target[property].apply(target, arguments)
                } else {
                    console.log("对象 =>" + name + ",读取属性:" + property + ", 值为:" + target[property] + ", 类型:" + typeof target[property])
                }
            } catch (e) {
                console.log("对象 =>" + name + ",读取属性:" + property + ", 值为:undefined" + ", 类型:undefined")
            }
            return target[property]
        },
        set: function(target, property, newValue, receiver) {
            try {
                if (typeof target[property] === 'function') {
                    console.log("对象 =>" + name + ",设置属性:" + property + "(), 值为:" + newValue + ", 类型:" + typeof target[property])
                } else {
                    console.log("对象 =>" + name + ",设置属性:" + property + ", 值为:" + newValue + ", 类型:" + typeof newValue)
                }
            } catch (e) {}
            return Reflect.set(target, property, newValue, receiver)
        }
    })
}
//基础bom代理
window = watch(globalThis, "window")

function Window() {}

function Document() {}

function Element() {}

function HTMLElement() {}

function HTMLDocument() {}

function Node() {}

function HTMLScriptElement() {
    this.tagName = "SCRIPT"
    this.parentNode = {
        removeChild: function(args) {
            console.log("对象 => " + "document.createElement.parentNode, 方法 => removeChild:", args)
        }
    }
}

function HTMLCanvasElement() {
    this.tagName = "CANVAS"
    this.width = 300
    this.height = 150
    this.getContext = function(type) {
        console.log("canvas.getContext:", type)
        return {
            fillRect: function() {},
            clearRect: function() {},
            getImageData: function() { return { data: new Uint8ClampedArray(4) } },
            putImageData: function() {},
            createImageData: function() { return { data: new Uint8ClampedArray(4) } },
            setTransform: function() {},
            drawImage: function() {},
            save: function() {},
            restore: function() {},
            beginPath: function() {},
            moveTo: function() {},
            lineTo: function() {},
            closePath: function() {},
            stroke: function() {},
            fill: function() {}
        }
    }
    this.toDataURL = function() { return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==" }
}

function HTMLDivElement() {
    this.tagName = "DIV"
    this.innerHTML = ""
    this.textContent = ""
}

function HTMLInputElement() {
    this.tagName = "INPUT"
    this.value = ""
    this.type = "text"
}

// 设置原型链
Node.prototype = {}
Element.prototype = Object.create(Node.prototype)
HTMLElement.prototype = Object.create(Element.prototype)
HTMLDocument.prototype = Object.create(Document.prototype)

// 基础方法
Element.prototype.scrollIntoViewIfNeeded = function() {}

// 使用Object.defineProperty定义Document原型方法
Object.defineProperty(Document.prototype, 'createElement', {
    configurable: true,
    enumerable: true,
    writable: true,
    value: function createElement(tagName) {
        console.log("对象 => document, 方法 => createElement创建元素:", tagName)
        if (tagName === 'script') {
            let scr = watch(new HTMLScriptElement(), 'script')
            return scr
        }
        if (tagName === 'canvas') {
            let cvs = watch(new HTMLCanvasElement(), 'canvas')
            return cvs
        }
        if (tagName === 'div') {
            let div = watch(new HTMLDivElement(), 'div')
            return div
        }
        if (tagName === 'input') {
            let inp = watch(new HTMLInputElement(), 'input')
            return inp
        }

        // 默认返回通用HTMLElement
        let element = new HTMLElement()
        element.tagName = tagName.toUpperCase()
        element.parentNode = null
        element.children = []
        element.style = {}
        element.addEventListener = function() {}
        element.removeEventListener = function() {}
        element.setAttribute = function() {}
        element.getAttribute = function() { return null }
        element.appendChild = function(child) {
            child.parentNode = this
            this.children.push(child)
        }
        element.removeChild = function(child) {
            child.parentNode = null
            let index = this.children.indexOf(child)
            if (index > -1) this.children.splice(index, 1)
        }

        return watch(element, tagName)
    }
})

Object.defineProperty(Document.prototype, 'querySelector', {
    configurable: true,
    enumerable: true,
    writable: true,
    value: function querySelector(selector) {
        console.log("对象 => document, 方法 => querySelector查询:", selector)
        return null
    }
})

Object.defineProperty(Document.prototype, 'createEvent', {
    configurable: true,
    enumerable: true,
    writable: true,
    value: function createEvent(type) {
        console.log("对象 => document, 方法 => createEvent创建事件:", type)
        return {}
    }
})

Document.prototype.all = {}
Document.prototype.documentElement = new HTMLElement()
Document.prototype.head = new HTMLElement()
Document.prototype.body = new HTMLElement()
Document.prototype.cookie = ""
Document.prototype.referrer = ""

// 创建浏览器环境对象
function Navigator() {
    this.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    this.platform = "Win32"
    this.appName = "Netscape"
    this.appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

function Location() {
    this.href = "https://search.jd.com/"
    this.hostname = "search.jd.com"
    this.host = "search.jd.com"
    this.origin = "https://search.jd.com"
    this.protocol = "https:"
    this.pathname = "/"
    this.port = ""
    this.search = ""
    this.hash = ""
}

function Screen() {
    this.width = 1920
    this.height = 1080
    this.availWidth = 1920
    this.availHeight = 1040
}

function LocalStorage() {
    this.getItem = function() { return null }
    this.setItem = function() {}
    this.removeItem = function() {}
}

function XMLHttpRequest() {
    this.open = function() {}
    this.send = function() {}
    this.setRequestHeader = function() {}
}

Window.prototype.navigator = watch(new Navigator(), "navigator")
Window.prototype.location = watch(new Location(), "location")
Window.prototype.screen = watch(new Screen(), "screen")
Window.prototype.localStorage = watch(new LocalStorage(), "localStorage")
Window.prototype.XMLHttpRequest = XMLHttpRequest
Window.prototype.outerWidth = 1920
Window.prototype.outerHeight = 1080
Window.prototype.devicePixelRatio = 1
Window.prototype.crypto = { getRandomValues: function() {} }

Window.prototype.document = watch(new Document(), "document")
Object.setPrototypeOf(window, Window.prototype)

// 全局暴露
global.Element = Element
global.HTMLElement = HTMLElement
global.Node = Node
global.XMLHttpRequest = XMLHttpRequest



require("./code1.js")

h = {
    "area": "16",
    "enc": "utf-8",
    "keyword": "电脑整机",
    "adType": 7,
    "page": "2",
    "ad_ids": "292:5",
    "xtest": "new_search"
}
g = {
    "appid": "search-pc-java",
    "functionId": "pc_search_adv_Search",
    "client": "pc",
    "clientVersion": "1.0.0",
    "t": (new Date).getTime()
}
g.body = CryptoJS.SHA256(JSON.stringify(h)).toString()

window.PSign = new ParamsSign({
    appId: "f06cc",
    debug: false,
    preRequest: false,
    onSign: function(data) {
        if (data && data.code && data.code != 200) { console.log(JSON.stringify(data)) }
    },
    onRequestTokenRemotely: function(data) {
        if (data && data.code && data.code != 0) { console.log(JSON.stringify(data)) }
    },
    onRequestToken: function(data) {
        if (data && data.code && data.code != 0) { console.log(JSON.stringify(data)) }
    }
});

h5stParames = window.PSign._$sdnmd(g)
console.log(h5stParames)