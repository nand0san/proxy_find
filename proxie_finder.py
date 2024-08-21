import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import asyncio
import aiohttp
import time


async def test_proxy(session, host, port, timeout=15):
    proxy_url = f"http://{host}:{port}"
    try:
        start_time = time.time()
        async with session.get('http://httpbin.org/ip', proxy=proxy_url, timeout=timeout) as response:
            if response.status == 200:
                content = await response.json()
                if 'origin' in content:
                    return f"{(time.time() - start_time):.2f}", content['origin']
        return "Failed", None
    except Exception as e:
        return f"Error: {str(e)}", None


async def get_proxies_with_test(limit=None):
    url = 'https://free-proxy-list.net/'
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []

    table = soup.find('table', class_='table table-striped table-bordered')
    rows = table.tbody.find_all('tr')

    if limit:
        rows = rows[:limit]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for row in rows:
            columns = row.find_all('td')
            host = columns[0].text.strip()
            port = columns[1].text.strip()
            proxy = {
                'host': host,
                'port': port,
                'country': columns[3].text.strip(),
                'anonymity': columns[4].text.strip(),
                'https': columns[6].text.strip(),
                'last_checked': columns[7].text.strip(),
                'extraction_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            task = asyncio.ensure_future(test_proxy(session, host, port))
            tasks.append((proxy, task))

        total = len(tasks)
        for i, (proxy, task) in enumerate(tasks, 1):
            response_time, detected_ip = await task
            proxy['response_time'] = response_time
            proxy['detected_ip'] = detected_ip if detected_ip else "N/A"
            proxies.append(proxy)

            if not response_time.startswith("Error") and response_time != "Failed":
                print(f"Proxy exitoso ({i}/{total}): {proxy['host']}:{proxy['port']} - Tiempo: {response_time}s")

            if i % 10 == 0:
                print(f"Progreso: {i}/{total} proxies probados")

    return proxies


def save_proxies(filename, limit=None):
    proxies = asyncio.get_event_loop().run_until_complete(get_proxies_with_test(limit))
    print(f"\nSe probaron {len(proxies)} proxies.")

    # Filtrar y ordenar los proxies
    working_proxies = [p for p in proxies if not p['response_time'].startswith("Error") and p['response_time'] != "Failed"]
    working_proxies.sort(key=lambda x: float(x['response_time']))

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['host', 'port', 'country', 'anonymity', 'https', 'last_checked', 'extraction_date', 'response_time', 'detected_ip']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for proxy in working_proxies:
            writer.writerow(proxy)

    print(f"Se encontraron {len(working_proxies)} proxies funcionando.")
    print(f"Proxies guardados en {filename}")

    # Mostrar los 10 mejores proxies
    print("\nLos 10 mejores proxies:")
    for proxy in working_proxies[:10]:
        print(f"{proxy['host']}:{proxy['port']} - Tiempo: {proxy['response_time']}s - IP: {proxy['detected_ip']}")


if __name__ == "__main__":
    save_proxies('proxies_working.csv', limit=200)
