#-*- coding=utf8 -*-
import re,json,csv,asyncio
from datetime import datetime



headers = ['datetime','部门','拦截','sql注入','信息泄露','代码注入','代码执行','文件包含','xss注入','目录穿越']

async def run(strings,department):
	sqli = 0
	info_disclose = 0
	codeinject = 0
	code_exec = 0
	fileinlcusion = 0
	xss = 0
	directory_traversal = 0
	# attack_dic = {0:'sql注入',14:'信息泄露',8:'代码注入',7:'代码执行',11:'文件包含'}
	print(type(strings))
	print(str(strings))
	top5 = re.search(r'(?<=\\"attack_type\\":).*?(?=, \\"country\\")',strings)
	deny = re.search(r'(?<=\\"deny\\":).*?(?=, \\"attack\\")',strings)
	if top5 and deny:
		try:
			result = top5.group()
			for item in eval(result):
				attack_type = item[0]
				if attack_type == 0:
					sqli = item[1]
				elif attack_type == 14:
					info_disclose = item[1]
				elif attack_type == 8:
					codeinject = item[1]
				elif attack_type == 7:
					code_exec = item[1]
				elif attack_type == 11:
					fileinlcusion = item[1]
				elif attack_type == 1:
					xss = item[1]
				elif attack_type == 20:
					directory_traversal = item[1]
			rows = [
			[datetime.now(),department,deny.group(),sqli,info_disclose,codeinject,code_exec,fileinlcusion,xss,directory_traversal]
			]
			with open('test.csv','a',encoding='utf-8-sig')as f:
				f_csv = csv.writer(f)
			
				f_csv.writerows(rows)
		except Exception as e:
			raise e
	else:
		print('oh,no')

if __name__ == "__main__":
	strings = '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{"code":200,"data":"{\"err\": null, \"data\": {\"attack_type\": [[0, 13993767], [14, 7602207], [11, 5103023], [20, 2839696], [1, 1417032]], \"country\": [], \"host\": [[\"http://fgw.ningbo.gov.cn\", 2269397], [\"http://kjt.zj.gov.cn\", 979684], [\"http://www.sx.gov.cn\", 879621], [\"http://mpa.zj.gov.cn\", 748481], [\"http://court.sxyc.gov.cn\", 576513]], \"province\": [[\"\\u5e7f\\u897f\", 329], [\"\\u8d35\\u5dde\", 57], [\"\\u897f\\u85cf\", 1], [\"\\u9999\\u6e2f\", 518], [\"\\u7518\\u8083\", 8], [\"\\u6e56\\u5357\", 2815869], [\"\\u6c5f\\u897f\", 1381], [\"\\u6cb3\\u5317\", 279119], [\"\\u53f0\\u6e7e\", 8693], [\"\\u9ed1\\u9f99\\u6c5f\", 219], [\"\\u9752\\u6d77\", 1], [\"\\u5e7f\\u4e1c\", 14459607], [\"\\u6e56\\u5317\", 1636], [\"\\u4e91\\u5357\", 1735], [\"\\u5b81\\u590f\", 3], [\"\\u91cd\\u5e86\", 16], [\"\\u5c71\\u897f\", 6], [\"\\u4e0a\\u6d77\", 26323], [\"\\u6cb3\\u5357\", 4535], [\"\\u5c71\\u4e1c\", 2597], [\"\\u8fbd\\u5b81\", 100], [\"\\u5929\\u6d25\", 145], [\"\\u5b89\\u5fbd\", 263], [\"\\u798f\\u5efa\", 563], [\"\\u6d77\\u5357\", 927], [\"\\u5185\\u8499\\u53e4\", 49668], [\"\\u5317\\u4eac\", 5307], [\"\\u56db\\u5ddd\", 2927], [\"\\u9655\\u897f\", 6], [\"\\u6d59\\u6c5f\", 14407609], [\"\\u6c5f\\u82cf\", 665724]], \"request_number\": [], \"src_ip\": [], \"total\": {\"request\": 504025456, \"deny\": 24373860, \"attack\": 0}}, \"msg\": null}","requestId":"1f4a6b2f-6221-4742-8be0-54d1d0264c08","message":"success"}</pre></body></html>'
	strings = str(strings)
	asyncio.get_event_loop().run_until_complete(run(strings))