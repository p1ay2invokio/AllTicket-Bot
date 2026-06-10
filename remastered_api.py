import requests
import urllib3
from curl_cffi import requests

# ปิดแจ้งเตือน InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getShowTime(perform_id):
    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        'G_ENABLED_IDPS': 'google',
        'cookieconsent_status': 'allow',
        'cookies-strictly': 'true',
        'cookies-performance': 'false',
        '_gid': 'GA1.2.455267189.1781077393',
        'G_AUTHUSER_H': '0',
        'aws-waf-token': '007be20d-3076-4d21-bb5d-51466c3b7f11:NQoAiSE16uoGAAAA:v40CCquR8LVE4v0PuBYGk50edtbLaPGdVq/0CNDmcMKfl6S0Amzdl26fZO7eTvGzA6twTSdTnEHPVKV268KapMM9HbbP2QIB6EMLvrR9kOGHVqF3MNQyMwRuKZMlEj7V70oN/Rbi0XvDp/nv94zhw64BGEH6EfexP1U8J6/rcerEqLa67B7jS8QtCwxwYj6H6yAzM7nJk27kMIFvHpnKn3LIHIt1AFMMJHUUOS89yDgxX1L2b5Ih1Ysh',
        '_gat': '1',
        '_ga_ERZFFGWN5D': 'GS2.2.s1781077405$o4$g1$t1781077526$j21$l0$h2120421124',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsYXkyMTk0N0BnbWFpbC5jb20iLCJ1cmxiYWNrIjoid3d3LmFsbHRpY2tldC5jb20iLCJwYXltZW50Q2hhbm5lbCI6IkMwNyIsInRpY2tldFR5cGUiOiIwMSIsImxhbmciOiJFIiwiZGF0YSI6ImM0YTgyZTMyOTY5YmUxYzU3OWFjZDFmNTI4ZWUxODA5YzYzYWM4OTBhMGFlN2VjOGFmZDAyYmQ3OTJjNjFlYjg4YWYxOGRjYTI0NDdhOTEwMWZjZDYxZjJmZjQzZDJmOGQ0M2VkODI5NThmMDg0NWFiNmI2OGZjYTE0NWFkOWQyMzM4Y2YyMmJjZmUyYjJkYTM2N2U3ODAxMDEzZWFiM2NiYzYyYTE1MzE5MTFjYzYyOTAzZmY4YWMxYTM5ZTljNGM5Y2UxNzJhYjNiNDQ1MjY0NjEzZmRkOTg4ZTljZGJlN2Y0Yjk2ZjNjMTAxNGFjYWYxMDA5ZDQ0ZWIyYWIyMjBiYzU4OTVjYWY1OWQ2ZDY1OTBkNjU0YjExZTkxYTMwNTNhMjcxZjMyMjM4ODJiNmJkYTRmZjI2NWZkNzY1ZTViOTY3MDhmYTY3ZWI4NzVmOWM2YTJlM2UxZjc1YTU3ZjVlNDNjNWY4YjJkMTU1NDJmMmQ3Zjg3MWMyMTkyMjk1YzZhMTJkZjhjNjJmZTJiYTBkZjMyZDkxNDgxYzJjZjM4NDNmODQxMTg2YmM5ZTk5Yzk4YWQxN2NmNzM1MjUwNmIzMjEzZTM0ZGI3NTJhYWQ4OTdmMDhiNjMwMzM0NDlmNzRiNmJjZjI4YjhjOTJlYTA0OGY0MzM4NTZhOTVmY2ZmYWQ5NGY2MmQzNjI1NDQ2NzMxYWRiMmUyYjE2MTU0Y2M5YjY4MGM1YzU5MWZhZDg4MzlkYzFmOTNjNDM4NDUxZGExNGVjNzNiNzQyNzBmYjU2Y2Q2MDA5NjRlN2Y3NzU0MDY3YTRiMDE5OWUxMzIxNTRmMWNiYjdhMDQ3MjIxYTg3NmYzMDYwZDAzOTUyNTcwM2Q2ZThlNjg5YjExMzdjNGFiZmY0MmI0Nzc0ODdiOTRlODk3MGI1YjZmNjA5YjU5MzUzODc5NzcyOTllOGRjNzQxYjE3YjI2YTQzZjRlMTYzODU3MjM1ZmQzNTJmZDE1ZmY3ZjFkNTNiMDFiNmRiNSIsInRpbWVTdGFtcCI6MC4zMDg2NzEwNzEwMjUwNzIyLCJzaW5nQWRkcmVzcyI6IjIyMy4yMDQuODcuNTYiLCJ0eXBlIjoiR09PR0xFIiwiaWF0IjoxNzgxMDc3NDAzLCJleHAiOjE3ODEwODgyMDMsImlzcyI6ImNzYXRrMTgifQ.4FFHP5lPlR7iaByR5fW9g0zAGwc2p--7H-VMR1_ywkc',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.allticket.com',
        'referer': 'https://www.allticket.com/event/2026&TEAMCONCERTTOURINBANGKOK',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    }

    json_data = {'performId': perform_id}

    try:
        response = requests.post('https://www.allticket.com/api-booking/get-round', cookies=cookies, headers=headers, json=json_data, verify=False, impersonate="chrome")
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}

def getShowZoneAvailable(performId, roundId):
    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        'G_ENABLED_IDPS': 'google',
        '_ga_ERZFFGWN5D': 'GS2.2.s1781079920$o5$g1$t1781081499$j11$l0$h978463243',
        'aws-waf-token': '007be20d-3076-4d21-bb5d-51466c3b7f11:NQoApAs/E+UAAAAA:sGtxEuu9Ym5dSDb8q9/zZuPRRMGJf5iU+V0OP7JBXXSL4KlWjVV9CaRJhpWpWqc9rIgngAP2CFXrh501L0/Or5e0L9Qd7h0XFtugi1S+v2DKxHQTVsv0v90b1sGS8THRJwO5Pp1A+vQSAq9vakevQANPixtIMyr0CUpX9HitEdh5xWvmw8Z2VbQErAVO9JjuXSp3gkvGG69Yez1lZWt4IamNPbfvBCn9IrGDd/tWevRz6r8sX+lUhLWR',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsYXkyMTk0N0BnbWFpbC5jb20iLCJ1cmxiYWNrIjoid3d3LmFsbHRpY2tldC5jb20iLCJwYXltZW50Q2hhbm5lbCI6IkMwNyIsInRpY2tldFR5cGUiOiIwMSIsImxhbmciOiJFIiwiZGF0YSI6ImM0YTgyZTMyOTY5YmUxYzU3OWFjZDFmNTI4ZWUxODA5YzYzYWM4OTBhMGFlN2VjOGFmZDAyYmQ3OTJjNjFlYjg4YWYxOGRjYTI0NDdhOTEwMWZjZDYxZjJmZjQzZDJmOGQ0M2VkODI5NThmMDg0NWFiNmI2OGZjYTE0NWFkOWQyMzM4Y2YyMmJjZmUyYjJkYTM2N2U3ODAxMDEzZWFiM2NiYzYyYTE1MzE5MTFjYzYyOTAzZmY4YWMxYTM5ZTljNGM5Y2UxNzJhYjNiNDQ1MjY0NjEzZmRkOTg4ZTljZGJlN2Y0Yjk2ZjNjMTAxNGFjYWYxMDA5ZDQ0ZWIyYWIyMjBiYzU4OTVjYWY1OWQ2ZDY1OTBkNjU0YjExZTkxYTMwNTNhMjcxZjMyMjM4ODJiNmJkYTRmZjI2NWZkNzY1ZTViOTY3MDhmYTY3ZWI4NzVmOWM2YTJlM2UxZjc1YTU3ZjVlNDNjNWY4YjJkMTU1NDJmMmQ3Zjg3MWMyMTkyMjk1YzZhMTJkZjhjNjJmZTJiYTBkZjMyZDkxNDgxYzJjZjM4NDNmODQxMTg2YmM5ZTk5Yzk4YWQxN2NmNzM1MjUwNmIzMjEzZTM0ZGI3NTJhYWQ4OTdmMDhiNjMwMzM0NDlmNzRiNmJjZjI4YjhjOTJlYTA0OGY0MzM4NTZhOTVmY2ZmYWQ5NGY2MmQzNjI1NDQ2NzMxYWRiMmUyYjE2MTU0Y2M5YjY4MGM1YzU5MWZhZDg4MzlkYzFmOTNjNDM4NDUxZGExNGVjNzNiNzQyNzBmYjU2Y2Q2MDA5NjRlN2Y3NzU0MDY3YTRiMDE5OWUxMzIxNTRmMWNiYjdhMDQ3MjIxYTg3NmYzMDYwZDAzOTUyNTcwM2Q2ZThlNjg5YjExMzdjNGFiZmY0MmI0Nzc0ODdiOTRlODk3MGI1YjZmNjA5YjU5MzUzODc5NzcyOTllOGRjNzQxYjE3YjI2YTQzZjRlMTYzODU3MjM1ZmQzNTJmZDE1ZmY3ZjFkNTNiMDFiNmRiNSIsInRpbWVTdGFtcCI6MC4zMDg2NzEwNzEwMjUwNzIyLCJzaW5nQWRkcmVzcyI6IjIyMy4yMDQuODcuNTYiLCJ0eXBlIjoiR09PR0xFIiwiaWF0IjoxNzgxMDc3NDAzLCJleHAiOjE3ODEwODgyMDMsImlzcyI6ImNzYXRrMTgifQ.4FFHP5lPlR7iaByR5fW9g0zAGwc2p--7H-VMR1_ywkc',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    }

    json_data = {'performId': performId, 'roundId': roundId}

    try:
        response = requests.post('https://www.allticket.com/api-booking/seat-available', cookies=cookies, headers=headers, json=json_data, verify=False, impersonate="chrome")
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}

# === ฟังก์ชันใหม่ สำหรับดึงข้อมูลที่นั่งในโซนที่เลือก ===
def getSeat(performId, roundId, zoneId):
    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        'G_ENABLED_IDPS': 'google',
        '_ga_ERZFFGWN5D': 'GS2.2.s1781079920$o5$g1$t1781081499$j11$l0$h978463243',
        'aws-waf-token': '007be20d-3076-4d21-bb5d-51466c3b7f11:NQoAvuo+X88bAAAA:4arYjrr9qY5NR8yrNc6iQZov9PvYnyzoPmP13iSI3YVdWyMYeawewNSL//yKrru/hOc32SOvrJWdUb6MICijrUNpnJ36EA4wFnnfkYuHISUMarBZyEej0QYRG8XK03FpsM4FUpACq3Cp8nGGqURqwqLdSAib95FJTF2YLeDEj71sYxOjnrP+SzBLe2ol6B60lIuCkJzMkrdSKM/5nnF3LvivaW0g7AAXvKrjohAlDCp59m2UFkrJoOaV',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBsYXkyMTk0N0BnbWFpbC5jb20iLCJ1cmxiYWNrIjoid3d3LmFsbHRpY2tldC5jb20iLCJwYXltZW50Q2hhbm5lbCI6IkMwNyIsInRpY2tldFR5cGUiOiIwMSIsImxhbmciOiJFIiwiZGF0YSI6ImM0YTgyZTMyOTY5YmUxYzU3OWFjZDFmNTI4ZWUxODA5YzYzYWM4OTBhMGFlN2VjOGFmZDAyYmQ3OTJjNjFlYjg4YWYxOGRjYTI0NDdhOTEwMWZjZDYxZjJmZjQzZDJmOGQ0M2VkODI5NThmMDg0NWFiNmI2OGZjYTE0NWFkOWQyMzM4Y2YyMmJjZmUyYjJkYTM2N2U3ODAxMDEzZWFiM2NiYzYyYTE1MzE5MTFjYzYyOTAzZmY4YWMxYTM5ZTljNGM5Y2UxNzJhYjNiNDQ1MjY0NjEzZmRkOTg4ZTljZGJlN2Y0Yjk2ZjNjMTAxNGFjYWYxMDA5ZDQ0ZWIyYWIyMjBiYzU4OTVjYWY1OWQ2ZDY1OTBkNjU0YjExZTkxYTMwNTNhMjcxZjMyMjM4ODJiNmJkYTRmZjI2NWZkNzY1ZTViOTY3MDhmYTY3ZWI4NzVmOWM2YTJlM2UxZjc1YTU3ZjVlNDNjNWY4YjJkMTU1NDJmMmQ3Zjg3MWMyMTkyMjk1YzZhMTJkZjhjNjJmZTJiYTBkZjMyZDkxNDgxYzJjZjM4NDNmODQxMTg2YmM5ZTk5Yzk4YWQxN2NmNzM1MjUwNmIzMjEzZTM0ZGI3NTJhYWQ4OTdmMDhiNjMwMzM0NDlmNzRiNmJjZjI4YjhjOTJlYTA0OGY0MzM4NTZhOTVmY2ZmYWQ5NGY2MmQzNjI1NDQ2NzMxYWRiMmUyYjE2MTU0Y2M5YjY4MGM1YzU5MWZhZDg4MzlkYzFmOTNjNDM4NDUxZGExNGVjNzNiNzQyNzBmYjU2Y2Q2MDA5NjRlN2Y3NzU0MDY3YTRiMDE5OWUxMzIxNTRmMWNiYjdhMDQ3MjIxYTg3NmYzMDYwZDAzOTUyNTcwM2Q2ZThlNjg5YjExMzdjNGFiZmY0MmI0Nzc0ODdiOTRlODk3MGI1YjZmNjA5YjU5MzUzODc5NzcyOTllOGRjNzQxYjE3YjI2YTQzZjRlMTYzODU3MjM1ZmQzNTJmZDE1ZmY3ZjFkNTNiMDFiNmRiNSIsInRpbWVTdGFtcCI6MC4zMDg2NzEwNzEwMjUwNzIyLCJzaW5nQWRkcmVzcyI6IjIyMy4yMDQuODcuNTYiLCJ0eXBlIjoiR09PR0xFIiwiaWF0IjoxNzgxMDc3NDAzLCJleHAiOjE3ODEwODgyMDMsImlzcyI6ImNzYXRrMTgifQ.4FFHP5lPlR7iaByR5fW9g0zAGwc2p--7H-VMR1_ywkc',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    }

    json_data = {
        'performId': performId,
        'roundId': roundId,
        'zoneId': zoneId,
    }

    try:
        response = requests.post('https://www.allticket.com/api-booking/get-seat', cookies=cookies, headers=headers, json=json_data, verify=False, impersonate="chrome")
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}