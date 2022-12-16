import csv

import scrapy

import datetime
import json
import re

import scrapy
from scrapy import Request
from scrapy.utils.response import open_in_browser


class ClassadriversSpider(scrapy.Spider):
    name = 'classadrivers'
    zyte_key = ''  # Todo : YOUR API KEY FROM ZYTE
    custom_settings = {
        'FEED_URI': 'Drivers.csv',
        'FEED_FORMAT': 'csv',
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_APIKEY': zyte_key,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
        },
    }

    headers = {
        'authority': 'employer.classadrivers.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'cache-control': 'no-cache',
        'cookie': '_RCRTX03=d631851a741811edaf1d973dcbcf4ef2eea1b0696fd54b7e8c5335c98ef239ed; _RCRTX03-samesite=d631851a741811edaf1d973dcbcf4ef2eea1b0696fd54b7e8c5335c98ef239ed; PHPSESSID=9b48ea40295bb8d35f488d6b2ed136b2; BIGipServerclassadrivers_POOL=!3yXhIOe0reOVOK/JRH0vqDRENlAHRr4TQwOohKuT32cuiAf6RQBA0foJmO2kWjDn7es4Mwzj4GlMAFk=; _hjSessionUser_81383=eyJpZCI6IjYzOGFiOTc1LWU3YmUtNTEyMi1hM2UzLWZhNGRmMWU0OWFjNCIsImNyZWF0ZWQiOjE2NzAxODg1NTM2ODgsImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2022-12-05T15:37:27.811Z; eupubconsent-v2=CPjg4BgPjg4BgAcABBENCtCsAP_AAH_AACiQJLNf_X__b2_r-_5_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M7vF36tq4KuR4ku3LBIUdlHOHcTUmw6okVryPsbk2cr7NKJ7PEmnMbOydYGH9_n1_z-ZKY7___f_7z_v-v________7-3f3__5___-__e_V__9zfn9_____9vP___9v-_9__________3_7997_HBJUAkw1biALsyxwZtowigRAjCsJDqBQAUUAwtEBhA6uCnZXAT6wgQAIBQBOBECHAFGDAIAABIAkIiAkCPBAIACIBAACABUIhAAxsAgsALAwCAAUA0LFGKAIQJCDIgIilMCAqRIKCeyoQSg_0NMIQ6ywAoNH_FQgI1kDFYEQkLByHBEgJeLJA8xRvkAIwQoBRKhWohPQAiQAEBoRQACA0IA.f_gAD_gAAAAA; usprivacy=1YNY; OneTrustWPCCPAGoogleOptOut=false; _gid=GA1.2.835327237.1670254648; optimizelyEndUserId=oeu1670254648907r0.4427814677138897; _hjIncludedInSessionSample=1; _hjSession_81383=eyJpZCI6IjYwZjgxMzY2LWE2MjItNDEzMy1hNWQzLWExZmFmYWQ3OGQwMSIsImNyZWF0ZWQiOjE2NzAyNTg2Mjk2MzAsImluU2FtcGxlIjp0cnVlfQ==; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; _ga_0V9QZJ6837=GS1.1.1670258628.3.1.1670263352.0.0.0; _ga=GA1.2.1297979426.1670188552; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Dec+05+2022+19%3A02%3A34+GMT%2B0100+(Central+European+Standard+Time)&version=6.39.0&isIABGlobal=false&hosts=&consentId=9a3faccd-ae2e-426c-ad3c-cab1f0f1b12a&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1%2CSTACK42%3A1&genVendors=V4%3A1%2CV5%3A1%2C&AwaitingReconsent=false&geolocation=SE%3BM',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Crawlera-Cookies': 'disable',
        'X-Crawlera-Profile': 'pass'
    }

    def start_requests(self):
        olds = [row['Url'] for row in csv.DictReader(open('Drivers.csv'))]

        for row in csv.DictReader(open('data_urls.csv')):
            if row['Url'] not in olds:
                yield Request(url=row['Url'],
                              headers=self.headers)

    def parse(self, response, **kwargs):
        name = response.css('.contentSection strong:nth-child(1)::text').get('')
        phone = response.css('.contentSection strong:nth-child(2)::text').get('')
        email = response.css('[name="inputEmailTo"]::attr(value)').get('')
        age = response.xpath('//*[contains(text(),"Age:")]/ancestor::p//text()').getall()
        licence_type = response.xpath('//*[contains(text(),"License Type")]/following::dd[1]//text()').get()
        addr = response.xpath(
            '//*[contains(text(),"Willing to work from:")]/ancestor::p[1]/following::ul[1]//text()').getall()
        routes = response.xpath('//*[contains(text(),"Route types")]/following::p[1]//text()').get()
        yield {
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Age': ' '.join(''.join(age).split()).replace('Age: ', ''),
            'License Type': licence_type,
            'Address': ' '.join(''.join(addr).split()),
            'Routes': routes,
            'Url': response.url
        }
