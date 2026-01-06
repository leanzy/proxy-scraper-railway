from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time

app = Flask(__name__)
CORS(app)  # CORS sorununu çözer

# Tüm proxy kaynakları (172+ kaynak!)
PROXY_SOURCES = {
    'HTTP': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt',
        'https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
        'https://raw.githubusercontent.com/ProxyDown/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/prxchks/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/caliphdev/ProxyList/main/http.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/astro76/Proxy-List/main/http.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/ProxyList/main/http.txt',
        'https://raw.githubusercontent.com/andigw/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/iammohitsharma/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/TechyNilesh/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/roxtar/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/hex4g/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/optcce/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/zero12a/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/proxy-list-proxy/list-proxy/main/http.txt',
        'https://www.proxyscan.io/download?type=http',
        'https://proxyspace.pro/http.txt',
        'http://worm.rip/http.txt',
        'https://openproxylist.xyz/http.txt',
        'https://proxylist.me/api/v1/list?type=http&format=text',
        'http://proxydb.net/plain?protocol=http',
        'http://pubproxy.com/api/proxy?limit=50&format=txt&type=http'
    ],
    'HTTPS': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
        'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
        'https://www.proxyscan.io/download?type=https',
        'https://proxyspace.pro/https.txt',
        'https://proxylist.me/api/v1/list?type=https&format=text',
        'http://proxydb.net/plain?protocol=https',
        'http://pubproxy.com/api/proxy?limit=50&format=txt&type=https'
    ],
    'SOCKS4': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
        'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks4.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt',
        'https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks4.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/ProxyDown/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/prxchks/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/caliphdev/ProxyList/main/socks4.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/astro76/Proxy-List/main/socks4.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/ProxyList/main/socks4.txt',
        'https://raw.githubusercontent.com/andigw/proxy-list/master/socks4.txt',
        'https://raw.githubusercontent.com/iammohitsharma/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/Volodichev/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/TechyNilesh/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/roxtar/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/hex4g/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/optcce/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/zero12a/proxy-list/main/socks4.txt',
        'https://raw.githubusercontent.com/proxy-list-proxy/list-proxy/main/socks4.txt',
        'https://www.proxyscan.io/download?type=socks4',
        'https://proxyspace.pro/socks4.txt',
        'http://worm.rip/socks4.txt',
        'https://openproxylist.xyz/socks4.txt',
        'https://proxylist.me/api/v1/list?type=socks4&format=text',
        'http://proxydb.net/plain?protocol=socks4',
        'http://pubproxy.com/api/proxy?limit=50&format=txt&type=socks4'
    ],
    'SOCKS5': [
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/socks5.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
        'https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/ProxyDown/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/prxchks/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/caliphdev/ProxyList/main/socks5.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/astro76/Proxy-List/main/socks5.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/ProxyList/main/socks5.txt',
        'https://raw.githubusercontent.com/andigw/proxy-list/master/socks5.txt',
        'https://raw.githubusercontent.com/iammohitsharma/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/Volodichev/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/TechyNilesh/Proxy-List/master/socks5.txt',
        'https://raw.githubusercontent.com/roxtar/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/hex4g/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/optcce/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/zero12a/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/proxy-list-proxy/list-proxy/main/socks5.txt',
        'https://www.proxyscan.io/download?type=socks5',
        'https://proxyspace.pro/socks5.txt',
        'http://worm.rip/socks5.txt',
        'https://openproxylist.xyz/socks5.txt',
        'https://proxylist.me/api/v1/list?type=socks5&format=text',
        'http://proxydb.net/plain?protocol=socks5',
        'http://pubproxy.com/api/proxy?limit=50&format=txt&type=socks5'
    ],
    'ALL': [
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
        'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
        'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/proxies.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/proxiesmaster/Free-Proxy-List/main/proxies.txt',
        'https://raw.githubusercontent.com/ObcbO/getproxy/master/proxy.txt',
        'https://raw.githubusercontent.com/turulixi2/freeproxy/main/proxy.txt',
        'https://raw.githubusercontent.com/miannoni/Free-Proxies/main/proxies.txt',
        'https://raw.githubusercontent.com/Infernex01/Proxy-Scrapper/main/proxies.txt',
        'https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies.txt',
        'https://raw.githubusercontent.com/ScrapeSecu/Free-Proxy-List/main/proxy.txt',
        'https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxies.txt',
        'https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/all.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/ALL_RAW.txt',
        'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/all.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/all.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/all.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/all.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/all.txt',
        'https://raw.githubusercontent.com/UserR3X/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt',
        'https://raw.githubusercontent.com/BlackSnowDot/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/ProxyDown/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/prxchks/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/caliphdev/ProxyList/main/all.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/astro76/Proxy-List/main/all.txt',
        'https://raw.githubusercontent.com/BlueSkyXN/ProxyList/main/all.txt',
        'https://raw.githubusercontent.com/andigw/proxy-list/master/all.txt',
        'https://raw.githubusercontent.com/iammohitsharma/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/Volodichev/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/TechyNilesh/Proxy-List/master/all.txt',
        'https://raw.githubusercontent.com/roxtar/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/hex4g/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/optcce/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/zero12a/proxy-list/main/all.txt',
        'https://raw.githubusercontent.com/proxy-list-proxy/list-proxy/main/all.txt',
        'https://spys.me/proxy.txt',
        'https://multiproxy.org/txt_all/proxy.txt',
        'https://rootjazz.com/proxies/proxies.txt',
        'http://alexa.lr2b.com/proxies.txt',
        'http://pubproxy.com/api/proxy?limit=50&format=txt'
    ]
}

CHECK_URLS = {
    'Google': 'https://www.google.com',
    'Netflix': 'https://www.netflix.com',
    'Crunchyroll': 'https://www.crunchyroll.com',
    'Hotmail': 'https://outlook.live.com',
}

# Scrape endpoint
@app.route('/api/scrape', methods=['POST'])
def scrape_proxies():
    data = request.json
    proxy_type = data.get('type', 'ALL')
    
    sources = PROXY_SOURCES.get(proxy_type, PROXY_SOURCES['ALL'])
    all_proxies = set()
    
    print(f"🔍 Scraping {len(sources)} sources for {proxy_type} proxies...")
    
    for i, url in enumerate(sources):
        try:
            response = requests.get(url, timeout=10)
            proxies = response.text.strip().split('\n')
            
            for proxy in proxies:
                proxy = proxy.strip()
                if proxy and ':' in proxy and len(proxy.split(':')) == 2:
                    all_proxies.add(proxy)
            
            print(f"✅ Source {i+1}/{len(sources)}: {len(all_proxies)} total proxies")
        except Exception as e:
            print(f"❌ Error on {url}: {str(e)}")
            continue
    
    result = list(all_proxies)
    print(f"🎯 Total scraped: {len(result)} unique proxies")
    
    return jsonify({
        'success': True,
        'total': len(result),
        'proxies': result,
        'sources_checked': len(sources)
    })

# Check endpoint
@app.route('/api/check', methods=['POST'])
def check_proxies():
    data = request.json
    proxies = data.get('proxies', [])
    target = data.get('target', 'Google')
    timeout = data.get('timeout', 5)
    
    test_url = CHECK_URLS.get(target, CHECK_URLS['Google'])
    working = []
    bad = []
    
    print(f"⚡ Checking {len(proxies)} proxies against {target}...")
    
    def check_single(proxy):
        try:
            proxy_url = f'http://{proxy}'
            response = requests.get(
                test_url,
                proxies={'http': proxy_url, 'https': proxy_url},
                timeout=timeout
            )
            if response.status_code == 200:
                return ('working', proxy)
        except:
            pass
        return ('bad', proxy)
    
    # Parallel checking
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(check_single, proxies)
        
        for status, proxy in results:
            if status == 'working':
                working.append(proxy)
            else:
                bad.append(proxy)
    
    print(f"✅ Working: {len(working)} | ❌ Bad: {len(bad)}")
    
    return jsonify({
        'success': True,
        'working': working,
        'bad': bad,
        'total_working': len(working),
        'total_bad': len(bad)
    })

# Info endpoint
@app.route('/api/info', methods=['GET'])
def get_info():
    total_sources = sum(len(sources) for sources in PROXY_SOURCES.values())
    return jsonify({
        'total_sources': total_sources,
        'sources_by_type': {k: len(v) for k, v in PROXY_SOURCES.items()},
        'check_targets': list(CHECK_URLS.keys())
    })

if __name__ == '__main__':
    print("🚀 Proxy Scraper Backend API Starting...")
    print(f"📊 Total sources available: {sum(len(s) for s in PROXY_SOURCES.values())}")
    app.run(host='0.0.0.0', port=5000, debug=True)