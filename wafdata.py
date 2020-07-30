from pyppeteer import launch
import asyncio,json,re,requests,time
from config import conf 
from putinfile import run




async def save_cookie(cookie):
	with open("cookie.json", 'w+', encoding="utf-8") as file:
		json.dump(cookie, file, ensure_ascii=False)

async def load_cookie():
	with open("cookie.json", 'r', encoding="utf-8") as file:
		cookie = json.load(file)
	return cookie


async def getcookie(page,username,password,loginurl):
	print(loginurl)
	await page.goto(loginurl,{'timeout': 12000})
	await asyncio.sleep(1.2)
	await page.type('#username',username)
	await page.type('#password',password)
	await page.waitFor(1000)
	await page.click('#kc-login')
	# await page.waitForSelector('.logged', {'timeout': 30000})
	await page.waitFor(10000)
	cookies = await page.cookies()
	await save_cookie(cookies)

# def waf(wafurl,cookies):
# 	for cookie in cookies:
# 		res = requests.get(url=wafurl,cookies=cookie,timeout=10,verify=False)
# 		content = res.content
# 	print(content)


async def waf(page,wafurl,cookies,department):
	print(wafurl)
	await page.goto(wafurl,{'timeout': 12000})
	for cookie in cookies:
		print(cookie)
		await page.setCookie(cookie)
	await page.goto(wafurl)
	strings = await page.content()
	strings = str(strings)
	await run(strings,department)


async def main():
	for c in conf:
		browser = await launch(headless=True,args=['--disable-xss-auditor','--no-sandbox'],ignoreHTTPSErrors=True,dumpio=True)
		loginurl = c['loginurl']
		wafurl = c['wafurl']
		username = c['username']
		password = c['password']
		department = c['department']
		page = await browser.newPage()
		await getcookie(page,username,password,loginurl)
		cookies = await load_cookie()
		await waf(page,wafurl,cookies,department)
		await page.close()
		await browser.close()
		time.sleep(2.2)



if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())