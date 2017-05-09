# -*- coding: utf-8 -*-
import random, base64


class ProxyMiddleware(object):
    #代理IP列表
    proxyList = [ \
	'116.211.143.11:80',
	'180.76.154.5:8888',
	'112.243.114.130:9999',
	'119.176.224.167:8118'
        ]

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        print "USE PROXY -> " + pro_adr
        request.meta['proxy'] = "http://" + pro_adr
