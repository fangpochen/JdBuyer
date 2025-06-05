# -*- coding:utf-8 -*-
import json
import os
import sys
import pickle
import random
import time
import requests

from lxml import etree

DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

if getattr(sys, 'frozen', False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))


class Session(object):
    """
    京东买手
    """

    # 初始化
    def __init__(self):
        self.userAgent = DEFAULT_USER_AGENT
        self.headers = {'User-Agent': self.userAgent}
        self.timeout = DEFAULT_TIMEOUT
        self.itemDetails = dict()  # 商品信息：分类id、商家id
        self.username = 'jd'
        self.isLogin = False
        self.password = None
        self.sess = requests.session()
        try:
            self.loadCookies()
        except Exception:
            pass

    ############## 登录相关 #############
    # 保存 cookie
    def saveCookies(self):
        cookiesFile = os.path.join(
            absPath, './cookies/{0}.cookies'.format(self.username))
        directory = os.path.dirname(cookiesFile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(cookiesFile, 'wb') as f:
            pickle.dump(self.sess.cookies, f)

    # 加载 cookie
    def loadCookies(self):
        cookiesFile = os.path.join(
            absPath, './cookies/{0}.cookies'.format(self.username))
        with open(cookiesFile, 'rb') as f:
            local_cookies = pickle.load(f)
        self.sess.cookies.update(local_cookies)
        self.isLogin = self._validateCookies()

    # 验证 cookie
    def _validateCookies(self):
        """
        通过访问用户订单列表页进行判断：若未登录，将会重定向到登陆页面。
        :return: cookies是否有效 True/False
        """
        url = 'https://order.jd.com/center/list.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }
        try:
            resp = self.sess.get(url=url, params=payload,
                                 allow_redirects=False)
            if self.respStatus(resp):
                return True
        except Exception as e:
            return False

        self.sess = requests.session()
        return False

    # 获取登录页
    def getLoginPage(self):
        url = "https://passport.jd.com/new/login.aspx"
        page = self.sess.get(url, headers=self.headers)
        return page

    # 获取登录二维码
    def getQRcode(self):
        url = 'https://qr.m.jd.com/show'
        payload = {
            'appid': 133,
            'size': 147,
            't': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.sess.get(url=url, headers=headers, params=payload)

        if not self.respStatus(resp):
            return None

        return resp.content

    # 获取Ticket
    def getQRcodeTicket(self):
        url = 'https://qr.m.jd.com/check'
        payload = {
            'appid': '133',
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            'token': self.sess.cookies.get('wlfstk_smdl'),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://passport.jd.com/new/login.aspx',
        }
        resp = self.sess.get(url=url, headers=headers, params=payload)

        if not self.respStatus(resp):
            return False

        respJson = self.parseJson(resp.text)
        if respJson['code'] != 200:
            return None
        else:
            return respJson['ticket']

    # 验证Ticket
    def validateQRcodeTicket(self, ticket):
        url = 'https://passport.jd.com/uc/qrCodeTicketValidation'
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
        }
        resp = self.sess.get(url=url, headers=headers, params={'t': ticket})

        if not self.respStatus(resp):
            return False

        respJson = json.loads(resp.text)
        if respJson['returnCode'] == 0:
            return True
        else:
            return False

    ############## 商品方法 #############
    # 获取商品详情信息
    def getItemDetail(self, skuId, skuNum=1, areaId=1):
        """ 查询商品详情 - 新版接口
        :param skuId
        :return 商品信息（下单模式、库存）
        """
        # 新版接口URL
        url = 'https://api.m.jd.com/'
        
        # 构建body参数（JSON字符串）
        body_data = {
            "skuId": str(skuId),
            "cat": "",  # 分类信息，可以为空
            "area": str(areaId) if isinstance(areaId, int) else str(areaId),  # 地区ID
            "shopId": "",  # 店铺ID，可以为空
            "venderId": "",  # 商家ID，可以为空
            "paramJson": json.dumps({"platform2": "1", "colType": 100}),
            "num": skuNum,
            "bbTraffic": "",
            "canvasType": 1,
            "giftServiceIsSelected": "",
            "customInfoId": "0"
        }
        
        payload = {
            'appid': 'pc-item-soa',
            'functionId': 'pc_detailpage_wareBusiness',
            'client': 'pc',
            'clientVersion': '1.0.0',
            't': str(int(time.time() * 1000)),
            'body': json.dumps(body_data, separators=(',', ':')),  # 压缩JSON
            'loginType': '3',
            'scval': str(skuId),  # 商品ID作为scval参数
        }
        
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://item.jd.com/{}.html'.format(skuId),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://item.jd.com',
        }
        
        # 先尝试简化版本，如果403则说明需要h5st签名
        try:
            # 使用POST方法发送请求
            resp = self.sess.post(url=url, data=payload, headers=headers)
            if resp.status_code == 403:
                print("⚠️ 新接口需要h5st签名参数，当前无法绕过")
                print("💡 建议: 使用浏览器F12获取完整请求参数，或寻找其他接口")
                
                # 尝试备用方案：回退到简化的GET请求
                print("🔄 尝试备用方案...")
                fallback_url = 'https://item-soa.jd.com/getWareBusiness'
                fallback_payload = {
                    'skuId': skuId,
                    'area': areaId,
                    'num': skuNum
                }
                fallback_headers = {
                    'User-Agent': self.userAgent,
                    'Referer': 'https://item.jd.com/{}.html'.format(skuId),
                }
                resp = self.sess.get(url=fallback_url, params=fallback_payload, headers=fallback_headers)
                print(f"备用接口状态码: {resp.status_code}")
            
            return resp
            
        except Exception as e:
            print(f"接口请求异常: {str(e)}")
            return None

    def fetchItemDetail(self, skuId):
        """ 解析商品信息
        :param skuId
        """
        resp = self.getItemDetail(skuId)
        print(f"商品详情接口状态码: {resp.status_code}")
        print(f"商品详情接口URL: {resp.url}")
        print(f"响应头Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
        
        if not self.respStatus(resp):
            raise Exception('获取商品详情失败，状态码：{}'.format(resp.status_code))
        
        print("响应内容前1000字符：", resp.text[:1000])  # 增加调试输出
        
        try:
            respJson = resp.json()
        except Exception as e:
            print("完整响应内容：", resp.text)  # 打印完整响应用于分析
            raise Exception('商品详情响应不是有效JSON格式：{}'.format(str(e)))
        
        if 'shopInfo' not in respJson or 'shop' not in respJson['shopInfo']:
            raise Exception('商品详情响应格式异常，缺少shopInfo信息')
            
        shopId = respJson['shopInfo']['shop']['shopId']
        detail = dict(venderId=shopId)
        if 'YuShouInfo' in respJson:
            detail['yushouUrl'] = respJson['YuShouInfo']['url']
        if 'miaoshaInfo' in respJson:
            detail['startTime'] = respJson['miaoshaInfo']['startTime']
            detail['endTime'] = respJson['miaoshaInfo']['endTime']
        self.itemDetails[skuId] = detail

    ############## 库存方法 #############
    def getItemStock(self, skuId, skuNum, areaId):
        """获取单个商品库存状态
        :param skuId: 商品id
        :param num: 商品数量
        :param areadId: 地区id
        :return: 商品是否有货 True/False
        """
        resp = self.getItemDetail(skuId, skuNum, areaId)
        if not self.respStatus(resp):
            return False
        try:
            respJson = resp.json()
            # 新接口返回结构：stockInfo.isStock
            return 'stockInfo' in respJson and respJson['stockInfo'].get('isStock', False)
        except Exception as e:
            print("库存查询响应异常：", resp.text[:200])
            return False

    ############## 购物车相关 #############

    def uncheckCartAll(self):
        """ 取消所有选中商品
        return 购物车信息
        """
        url = 'https://api.m.jd.com/api'

        headers = {
            'User-Agent': self.userAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://cart.jd.com',
            'referer': 'https://cart.jd.com'
        }

        data = {
            'functionId': 'pcCart_jc_cartUnCheckAll',
            'appid': 'JDC_mall_cart',
            'body': '{"serInfo":{"area":"","user-key":""}}',
            'loginType': 3
        }

        resp = self.sess.post(url=url, headers=headers, data=data)

        # return self.respStatus(resp) and resp.json()['success']
        return resp

    def addCartSku(self, skuId, skuNum):
        """ 加入购入车
        skuId 商品sku
        skuNum 购买数量
        retrun 是否成功
        """
        url = 'https://api.m.jd.com/api'

        headers = {
            'User-Agent': self.userAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://cart.jd.com',
            'referer': 'https://cart.jd.com'
        }

        data = {
            'functionId': 'pcCart_jc_cartAdd',
            'appid': 'JDC_mall_cart',
            'body': '{\"operations\":[{\"carttype\":1,\"TheSkus\":[{\"Id\":\"' + skuId + '\",\"num\":' + str(skuNum) + '}]}]}',
            'loginType': 3
        }

        resp = self.sess.post(url=url, headers=headers, data=data)

        return self.respStatus(resp) and resp.json()['success']

    def changeCartSkuCount(self, skuId, skuUid, skuNum, areaId):
        """ 修改购物车商品数量
        skuId 商品sku
        skuUid 商品用户关系
        skuNum 购买数量
        retrun 是否成功
        """
        url = 'https://api.m.jd.com/api'

        headers = {
            'User-Agent': self.userAgent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://cart.jd.com',
            'referer': 'https://cart.jd.com'
        }

        body = '{\"operations\":[{\"TheSkus\":[{\"Id\":\"'+skuId+'\",\"num\":'+str(
            skuNum)+',\"skuUuid\":\"'+skuUid+'\",\"useUuid\":false}]}],\"serInfo\":{\"area\":\"'+areaId+'\"}}'
        data = {
            'functionId': 'pcCart_jc_changeSkuNum',
            'appid': 'JDC_mall_cart',
            'body': body,
            'loginType': 3
        }

        resp = self.sess.post(url=url, headers=headers, data=data)

        return self.respStatus(resp) and resp.json()['success']

    def prepareCart(self, skuId, skuNum, areaId):
        """ 下单前准备购物车
        1 取消全部勾选（返回购物车信息）
        2 已在购物车则修改商品数量
        3 不在购物车则加入购物车
        skuId 商品sku
        skuNum 商品数量
        return True/False
        """
        resp = self.uncheckCartAll()
        respObj = resp.json()
        if not self.respStatus(resp) or not respObj['success']:
            raise Exception('购物车取消勾选失败')

        # 检查商品是否已在购物车
        cartInfo = respObj['resultData']['cartInfo']
        if not cartInfo:
            # 购物车为空 直接加入
            return self.addCartSku(skuId, skuNum)

        venders = cartInfo['vendors']

        for vender in venders:
            # if str(vender['vendorId']) != self.itemDetails[skuId]['vender_id']:
            #     continue
            items = vender['sorted']
            for item in items:
                if str(item['item']['Id']) == skuId:
                    # 在购物车中 修改数量
                    return self.changeCartSkuCount(skuId, item['item']['skuUuid'], skuNum, areaId)
        # 不在购物车中
        return self.addCartSku(skuId, skuNum)

    ############## 订单相关 #############

    def trySubmitOrder(self, skuId, skuNum, areaId, retry=3, interval=5):
        """提交订单
        :return: 订单提交结果 True/False
        """
        itemDetail = self.itemDetails[skuId]
        isYushou = False
        if 'yushouUrl' in itemDetail:
            self.getPreSallCheckoutPage(skuId, skuNum)
            isYushou = True
        else:
            self.prepareCart(skuId, skuNum, areaId)
            self.getCheckoutPage()

        for i in range(1, retry + 1):
            ret, msg = self.submitOrder(isYushou)
            if ret:
                return True
            else:
                time.sleep(interval)
        return False

    def submitOrderWitchTry(self, retry=3, interval=4):
        """提交订单，并且带有重试功能
        :param retry: 重试次数
        :param interval: 重试间隔
        :return: 订单提交结果 True/False
        """
        for i in range(1, retry + 1):
            self.getCheckoutPage()
            sumbmitSuccess, msg = self.submitOrder()
            if sumbmitSuccess:
                return True
            else:
                if i < retry:
                    time.sleep(interval)
        return False

    def getCheckoutPage(self):
        """获取订单结算页面信息
        :return: 结算信息 dict
        """
        url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
        # url = 'https://cart.jd.com/gotoOrder.action'
        payload = {
            'rid': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://cart.jd.com/cart',
        }
        try:
            resp = self.sess.get(url=url, params=payload, headers=headers)
            if not self.respStatus(resp):
                return

            html = etree.HTML(resp.text)
            self.eid = html.xpath("//input[@id='eid']/@value")
            self.fp = html.xpath("//input[@id='fp']/@value")
            self.risk_control = html.xpath("//input[@id='riskControl']/@value")
            self.track_id = html.xpath("//input[@id='TrackID']/@value")

            order_detail = {
                # remove '寄送至： ' from the begin
                'address': html.xpath("//span[@id='sendAddr']")[0].text[5:],
                # remove '收件人:' from the begin
                'receiver':  html.xpath("//span[@id='sendMobile']")[0].text[4:],
                # remove '￥' from the begin
                'total_price':  html.xpath("//span[@id='sumPayPriceId']")[0].text[1:],
                'items': []
            }
            return order_detail
        except Exception as e:
            return

    def getPreSallCheckoutPage(self, skuId, skuNum=1):
        """获取预售商品结算页面信息
        :return: 结算信息 dict
        """
        url = 'https://cart.jd.com/cart/dynamic/gateForSubFlow.action'
        # url = 'https://cart.jd.com/gotoOrder.action'
        payload = {
            'wids': skuId,
            'nums': skuNum,
            'subType': 32
        }
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://cart.jd.com/cart',
        }
        try:
            resp = self.sess.get(url=url, params=payload, headers=headers)
            if not self.respStatus(resp):
                return

            html = etree.HTML(resp.text)
            self.eid = html.xpath("//input[@id='eid']/@value")
            self.fp = html.xpath("//input[@id='fp']/@value")
            self.risk_control = html.xpath("//input[@id='riskControl']/@value")
            self.track_id = html.xpath("//input[@id='TrackID']/@value")
            order_detail = {
                # remove '寄送至： ' from the begin
                'address': html.xpath("//span[@class='addr-info']")[0].text,
                # remove '收件人:' from the begin
                'receiver':  html.xpath("//span[@class='addr-name']")[0].text,
            }
            return order_detail
        except Exception as e:
            return

    def submitOrder(self, isYushou=False):
        """提交订单
        :return: True/False 订单提交结果
        """
        url = 'https://trade.jd.com/shopping/order/submitOrder.action'
        # js function of submit order is included in https://trade.jd.com/shopping/misc/js/order.js?r=2018070403091

        data = {
            'overseaPurchaseCookies': '',
            'vendorRemarks': '[]',
            'submitOrderParam.sopNotPutInvoice': 'false',
            'submitOrderParam.trackID': 'TestTrackId',
            'submitOrderParam.ignorePriceChange': '0',
            'submitOrderParam.btSupport': '0',
            'riskControl': self.risk_control,
            'submitOrderParam.isBestCoupon': 1,
            'submitOrderParam.jxj': 1,
            'submitOrderParam.trackId': self.track_id,
            'submitOrderParam.eid': self.eid,
            'submitOrderParam.fp': self.fp,
            'submitOrderParam.needCheck': 1,
        }

        if isYushou:
            data['submitOrderParam.needCheck'] = 1
            data['preSalePaymentTypeInOptional'] = 2
            data['submitOrderParam.payType4YuShou'] = 2

        # add payment password when necessary
        paymentPwd = self.password
        if paymentPwd:
            data['submitOrderParam.payPassword'] = ''.join(
                ['u3' + x for x in paymentPwd])

        headers = {
            'User-Agent': self.userAgent,
            'Host': 'trade.jd.com',
            'Referer': 'http://trade.jd.com/shopping/order/getOrderInfo.action',
        }

        try:
            resp = self.sess.post(url=url, data=data, headers=headers)
            respJson = json.loads(resp.text)

            if respJson.get('success'):
                orderId = respJson.get('orderId')
                return True, orderId
            else:
                message, result_code = respJson.get(
                    'message'), respJson.get('resultCode')
                if result_code == 0:
                    self._saveInvoice()
                    message = message + '(下单商品可能为第三方商品，将切换为普通发票进行尝试)'
                elif result_code == 60077:
                    message = message + '(可能是购物车为空 或 未勾选购物车中商品)'
                elif result_code == 60123:
                    message = message + '(需要在config.ini文件中配置支付密码)'
                return False, message
        except Exception as e:
            return False, e

    def _saveInvoice(self):
        """下单第三方商品时如果未设置发票，将从电子发票切换为普通发票
        http://jos.jd.com/api/complexTemplate.htm?webPamer=invoice&groupName=%E5%BC%80%E6%99%AE%E5%8B%92%E5%85%A5%E9%A9%BB%E6%A8%A1%E5%BC%8FAPI&id=566&restName=jd.kepler.trade.submit&isMulti=true
        :return:
        """
        url = 'https://trade.jd.com/shopping/dynamic/invoice/saveInvoice.action'
        data = {
            "invoiceParam.selectedInvoiceType": 1,
            "invoiceParam.companyName": "个人",
            "invoiceParam.invoicePutType": 0,
            "invoiceParam.selectInvoiceTitle": 4,
            "invoiceParam.selectBookInvoiceContent": "",
            "invoiceParam.selectNormalInvoiceContent": 1,
            "invoiceParam.vatCompanyName": "",
            "invoiceParam.code": "",
            "invoiceParam.regAddr": "",
            "invoiceParam.regPhone": "",
            "invoiceParam.regBank": "",
            "invoiceParam.regBankAccount": "",
            "invoiceParam.hasCommon": "true",
            "invoiceParam.hasBook": "false",
            "invoiceParam.consigneeName": "",
            "invoiceParam.consigneePhone": "",
            "invoiceParam.consigneeAddress": "",
            "invoiceParam.consigneeProvince": "请选择：",
            "invoiceParam.consigneeProvinceId": "NaN",
            "invoiceParam.consigneeCity": "请选择",
            "invoiceParam.consigneeCityId": "NaN",
            "invoiceParam.consigneeCounty": "请选择",
            "invoiceParam.consigneeCountyId": "NaN",
            "invoiceParam.consigneeTown": "请选择",
            "invoiceParam.consigneeTownId": 0,
            "invoiceParam.sendSeparate": "false",
            "invoiceParam.usualInvoiceId": "",
            "invoiceParam.selectElectroTitle": 4,
            "invoiceParam.electroCompanyName": "undefined",
            "invoiceParam.electroInvoiceEmail": "",
            "invoiceParam.electroInvoicePhone": "",
            "invokeInvoiceBasicService": "true",
            "invoice_ceshi1": "",
            "invoiceParam.showInvoiceSeparate": "false",
            "invoiceParam.invoiceSeparateSwitch": 1,
            "invoiceParam.invoiceCode": "",
            "invoiceParam.saveInvoiceFlag": 1
        }
        headers = {
            'User-Agent': self.userAgent,
            'Referer': 'https://trade.jd.com/shopping/dynamic/invoice/saveInvoice.action',
        }
        self.sess.post(url=url, data=data, headers=headers)

    def parseJson(self, s):
        begin = s.find('{')
        end = s.rfind('}') + 1
        return json.loads(s[begin:end])

    def respStatus(self, resp):
        if resp.status_code != requests.codes.OK:
            return False
        return True


if __name__ == '__main__':

    skuId = '100015253059'
    areaId = '1_2901_55554_0'
    skuNum = 1

    session = Session()
    print(session.getItemDetail(skuId, skuNum, areaId).text)
