import requests
import browser_cookie3
import main

cj = browser_cookie3.chrome(domain_name='allticket.com')

jwt_token = None

def setToken(token):
    print("HERE")
    global jwt_token
    jwt_token = token


def info(namePerform):

    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'authorization': jwt_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.allticket.com/event/RockonTheBeach2026',
        'accept-language': 'en',
        # 'cookie': '_ga=GA1.2.343711809.1774242358; _gid=GA1.2.1045221530.1774242358; G_ENABLED_IDPS=google; cookieconsent_status=allow; cookies-strictly=true; cookies-performance=false; aws-waf-token=d55ed907-d79b-49f7-adba-af81ce780a23:NQoAjfNSoKsOAAAA:4vfLCleXCzCw6Ly0cQsgboC2WHu+OqHVpPT8er1KOLAANgN9qif+k69hS2QvByBt22Um8kgioNUZ40IOVam6w7Ykz4JtSDHt++VM58sPELtQsq/H78jq3MFoDp2kq3yrXrNRN1QvtFT8KrGErRCApp4PYpjLDdMABLfUPM5SkrZHTPC/J1XKcHTKyFs1bt5HxTEKdUhRS9W+je6UgpGEZaM5IxiXhBzRzJf9EnnjZCFxfaJ/pj0IOtt0XEk32yYX+zag/q/sybs=; _gat=1; _ga_ERZFFGWN5D=GS2.2.s1774264804$o3$g1$t1774266525$j60$l0$h37194473',
        'priority': 'u=1, i',
    }

    params = {
        'time': '1774266525170',
    }

    response = requests.get(
        f'https://www.allticket.com/master/event_info/{namePerform}.json',
        params=params,
        cookies=cj,
        headers=headers,
        verify=False
    )
    
    return response.json()

# หารอบที่สแดง
def getRound(performId):
    
    
    # print("CJ : ", cj)
    
    # print("BEFORE GET : ", jwt_token)

    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        '_gid': 'GA1.2.1045221530.1774242358',
        'G_ENABLED_IDPS': 'google',
        '_ga_ERZFFGWN5D': 'GS2.2.s1774242504$o1$g1$t1774244701$j56$l0$h1022027588',
        'aws-waf-token': 'd55ed907-d79b-49f7-adba-af81ce780a23:NQoAoeQonAJZAAAA:Q1GSu8ChFrRtBVEYMRihbnwnxZRUiw7DU1T5cfinYCNWGl1rEPJIUmUNyV7Zvf6fWXqkvcAE+KpZq03/+HdwtJXazCUJCfIOiTPuBDIsiN2XkuAa3bfm8AJRGfiYPAka99s+wgUW7qd7aGNMsoQ8+8kMAUXB3RAPJJ0UsA4fjSU7RLzZInFedu3/0limzBdUw47T+bkLbazfr01gM30xvsj4cH00iUhOcKant0mRP0hnUv53ZFrgg2mU',
    }

    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'authorization': jwt_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.allticket.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.allticket.com/event/RockonTheBeach2026',
        'accept-language': 'en',
        # 'cookie': '_ga=GA1.2.343711809.1774242358; _gid=GA1.2.1045221530.1774242358; G_ENABLED_IDPS=google; _ga_ERZFFGWN5D=GS2.2.s1774242504$o1$g1$t1774244701$j56$l0$h1022027588; aws-waf-token=d55ed907-d79b-49f7-adba-af81ce780a23:NQoAoeQonAJZAAAA:Q1GSu8ChFrRtBVEYMRihbnwnxZRUiw7DU1T5cfinYCNWGl1rEPJIUmUNyV7Zvf6fWXqkvcAE+KpZq03/+HdwtJXazCUJCfIOiTPuBDIsiN2XkuAa3bfm8AJRGfiYPAka99s+wgUW7qd7aGNMsoQ8+8kMAUXB3RAPJJ0UsA4fjSU7RLzZInFedu3/0limzBdUw47T+bkLbazfr01gM30xvsj4cH00iUhOcKant0mRP0hnUv53ZFrgg2mU',
        'priority': 'u=1, i',
    }

    json_data = {
        'performId': str(performId),
    }

    response = requests.post('https://www.allticket.com/api-booking/get-round', cookies=cj, headers=headers, json=json_data, verify=False)
    
    print("TEST : ", response)
    print("TEST : ", response.text)
    
    return response.json()
    
    
def seatAvailable(performId, roundId):

    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        '_gid': 'GA1.2.1045221530.1774242358',
        'G_ENABLED_IDPS': 'google',
        '_gat': '1',
        '_ga_ERZFFGWN5D': 'GS2.2.s1774242504$o1$g1$t1774245532$j60$l0$h1022027588',
        'aws-waf-token': 'd55ed907-d79b-49f7-adba-af81ce780a23:NQoAj40onqlZAAAA:aFI11aYT59IXGGE6hC4GCz1T91fnpJoB4pPg/i501SCSI58tjR8pVTbeSUzoz0YaeQDE8VUJVRZItlYOBDuJnmiM4s2aKcRSGDoCFPFY1d5bNDDAOMGMh35QWM1jK67JCd2azCs4/vpPIuqfGPadjCKMsAqkPkV6Bh4VCMPJVZVVdru5DctZDbPTlkAr6RfJMpl4r36tB3UM+MZnljLJPwrE4aWFX6p/OhDoZ+vaEXyNRQHiFJRuUyWb',
    }

    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'authorization': jwt_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.allticket.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.allticket.com/event/RockonTheBeach2026',
        'accept-language': 'en',
        # 'cookie': '_ga=GA1.2.343711809.1774242358; _gid=GA1.2.1045221530.1774242358; G_ENABLED_IDPS=google; _gat=1; _ga_ERZFFGWN5D=GS2.2.s1774242504$o1$g1$t1774245532$j60$l0$h1022027588; aws-waf-token=d55ed907-d79b-49f7-adba-af81ce780a23:NQoAj40onqlZAAAA:aFI11aYT59IXGGE6hC4GCz1T91fnpJoB4pPg/i501SCSI58tjR8pVTbeSUzoz0YaeQDE8VUJVRZItlYOBDuJnmiM4s2aKcRSGDoCFPFY1d5bNDDAOMGMh35QWM1jK67JCd2azCs4/vpPIuqfGPadjCKMsAqkPkV6Bh4VCMPJVZVVdru5DctZDbPTlkAr6RfJMpl4r36tB3UM+MZnljLJPwrE4aWFX6p/OhDoZ+vaEXyNRQHiFJRuUyWb',
        'priority': 'u=1, i',
    }

    json_data = {
        'performId': performId,
        'roundId': roundId,
    }

    response = requests.post('https://www.allticket.com/api-booking/seat-available', cookies=cj, headers=headers, json=json_data, verify=False)
    
    return response.json()


def reserve(performId, roundId, zoneId, screenLabel, seatType, seatAmount, consentId, consentvalue):
    

    cookies = {
        '_ga': 'GA1.2.343711809.1774242358',
        '_gid': 'GA1.2.1045221530.1774242358',
        'G_ENABLED_IDPS': 'google',
        'cookieconsent_status': 'allow',
        'cookies-strictly': 'true',
        'cookies-performance': 'false',
        'aws-waf-token': 'd55ed907-d79b-49f7-adba-af81ce780a23:NQoAmOtQ498IAAAA:zlCAYTkydf+TDCOFGuaRF1G+FqZE46hjbHucicy7KsoeJozzYf//sLWKB87bt++6AxNHbWWanmy+iWlvKEOY34VOWpvniFoEx3wV08ohypaHdpD7/lV5Z681QgX5wWqZaSvGW3goOfEMUEH+SfsDj7/oMuaOhFz90hBVESNSgPynKaHvMSfkm8scHhKgPcAnG4GhUg3aFCIpcn98DIOba9TSJVuNGASUpILQGDSpOYwGAiZPw5oOjiEiBwXXrVSkaclw4p4If20=',
        '_gat': '1',
        '_ga_ERZFFGWN5D': 'GS2.2.s1774264804$o3$g1$t1774265674$j52$l0$h37194473',
    }

    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'authorization': jwt_token,
        'atk-z-data': 'U2FsdGVkX1+U0XD1kjp3biGCGaQqKynSTylCCFI+CbBip5k45pVAVMMSYXP6VsAqU1QmBabr74utHcUUJkyTfMwSS+nSuoeFWI3erpdSyHzP5htYnXcapb5O4VyFS77FEZwK5AyMM/MRmAA3DGU5Q7u3XBmMJltF7/oLbLFNh/NzT4US6i6GkqZtF0ZspW+4',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'origin': 'https://www.allticket.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.allticket.com/event/RockonTheBeach2026',
        'accept-language': 'en',
        # 'cookie': '_ga=GA1.2.343711809.1774242358; _gid=GA1.2.1045221530.1774242358; G_ENABLED_IDPS=google; cookieconsent_status=allow; cookies-strictly=true; cookies-performance=false; aws-waf-token=d55ed907-d79b-49f7-adba-af81ce780a23:NQoAmOtQ498IAAAA:zlCAYTkydf+TDCOFGuaRF1G+FqZE46hjbHucicy7KsoeJozzYf//sLWKB87bt++6AxNHbWWanmy+iWlvKEOY34VOWpvniFoEx3wV08ohypaHdpD7/lV5Z681QgX5wWqZaSvGW3goOfEMUEH+SfsDj7/oMuaOhFz90hBVESNSgPynKaHvMSfkm8scHhKgPcAnG4GhUg3aFCIpcn98DIOba9TSJVuNGASUpILQGDSpOYwGAiZPw5oOjiEiBwXXrVSkaclw4p4If20=; _gat=1; _ga_ERZFFGWN5D=GS2.2.s1774264804$o3$g1$t1774265674$j52$l0$h37194473',
        'priority': 'u=1, i',
    }

    json_data = {
        'performId': performId,
        'roundId': roundId,
        'zoneId': zoneId,
        'screenLabel': zoneId,
        'seatTo': {
            'seatType': seatType,
            'seatAmount': seatAmount,
        },
        'shirtTo': [],
        'consents': [
            {
                'consentId': consentId,
                'consentvalue': consentvalue,
            },
        ],
    }

    response = requests.post('https://www.allticket.com/api-booking/handler-reserve', cookies=cookies, headers=headers, json=json_data, verify=False)
    

    return response.json()


# เช็คการจอง
def checkBooking(uuid):
    
    
    
    cookies = {
    '_ga': 'GA1.2.343711809.1774242358',
    '_gid': 'GA1.2.1045221530.1774242358',
    'G_ENABLED_IDPS': 'google',
    '_gat': '1',
    'aws-waf-token': 'd55ed907-d79b-49f7-adba-af81ce780a23:NQoAj40onqlZAAAA:aFI11aYT59IXGGE6hC4GCz1T91fnpJoB4pPg/i501SCSI58tjR8pVTbeSUzoz0YaeQDE8VUJVRZItlYOBDuJnmiM4s2aKcRSGDoCFPFY1d5bNDDAOMGMh35QWM1jK67JCd2azCs4/vpPIuqfGPadjCKMsAqkPkV6Bh4VCMPJVZVVdru5DctZDbPTlkAr6RfJMpl4r36tB3UM+MZnljLJPwrE4aWFX6p/OhDoZ+vaEXyNRQHiFJRuUyWb',
    '_ga_ERZFFGWN5D': 'GS2.2.s1774242504$o1$g1$t1774245550$j42$l0$h1022027588',
    }

    headers = {
        'sec-ch-ua-platform': '"macOS"',
        'authorization': jwt_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'origin': 'https://www.allticket.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.allticket.com/event/RockonTheBeach2026',
        'accept-language': 'en',
        # 'cookie': '_ga=GA1.2.343711809.1774242358; _gid=GA1.2.1045221530.1774242358; G_ENABLED_IDPS=google; _gat=1; aws-waf-token=d55ed907-d79b-49f7-adba-af81ce780a23:NQoAj40onqlZAAAA:aFI11aYT59IXGGE6hC4GCz1T91fnpJoB4pPg/i501SCSI58tjR8pVTbeSUzoz0YaeQDE8VUJVRZItlYOBDuJnmiM4s2aKcRSGDoCFPFY1d5bNDDAOMGMh35QWM1jK67JCd2azCs4/vpPIuqfGPadjCKMsAqkPkV6Bh4VCMPJVZVVdru5DctZDbPTlkAr6RfJMpl4r36tB3UM+MZnljLJPwrE4aWFX6p/OhDoZ+vaEXyNRQHiFJRuUyWb; _ga_ERZFFGWN5D=GS2.2.s1774242504$o1$g1$t1774245550$j42$l0$h1022027588',
        'priority': 'u=1, i',
    }

    json_data = {
        'uuid': uuid,
    }
    
    response = requests.post('https://www.allticket.com/api-verify/check-booking', cookies=cj, headers=headers, json=json_data, verify=False)
    
    return response.json()