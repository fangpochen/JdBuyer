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

function HTMLScriptElement() {
    this.tagName = "SCRIPT"
    this.parentNode = {
        removeChild: function(args) {
            console.log("对象 => document.createElement.parentNode, 方法 => removeChild, 移除元素: ", args)
        }
    }
}

Object.defineProperty(Document.prototype, 'createElement', {
    configurable: true,
    enumerable: true,
    writable: true,
    value: function createElement(tagName) {
        console.log("对象 => document, 方法 => createElement, 创建元素: ", tagName)
        if (tagName === "script") {
            scr = watch(new HTMLScriptElement(), "script")
            return scr
        }
    }
})

Window.prototype.document = watch(new Document(), "document")
Object.setPrototypeOf(window, Window.prototype)

function Elements() {
    this.prototype = function() {
        return scrollIntoViewIfNeeded
    }
}

Element = watch(new Elements(), "Element")


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
console.log('h5stParames:', h5stParames)