import csv
import requests
import time
from collections import namedtuple
from requests.exceptions import RequestException
import urllib3
import concurrent.futures

# Desactivar advertencias de SSL inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ProxyTest = namedtuple('ProxyTest', ['url', 'validation_method'])


def validate_ip_response(response):
    try:
        json_response = response.json()
        return 'ip' in json_response or 'origin' in json_response
    except ValueError:
        return len(response.text.strip()) < 50  # Asumimos que es una IP si es un texto corto


def validate_google(response):
    return '<title>Google</title>' in response.text


PROXY_TESTS = [
    ProxyTest('http://httpbin.org/ip', validate_ip_response),
    ProxyTest('https://api.ipify.org', validate_ip_response),
    ProxyTest('https://www.google.com', validate_google)
]


def extract_ip(response):
    try:
        json_response = response.json()
        return json_response.get('ip') or json_response.get('origin')
    except ValueError:
        return response.text.strip() if len(response.text.strip()) < 50 else None


def test_proxy(proxy, timeout=10):
    proxy_url = f"http://{proxy['host']}:{proxy['port']}"
    proxies = {"http": proxy_url, "https": proxy_url}
    results = []
    detected_ip = None

    for test in PROXY_TESTS:
        try:
            start_time = time.time()
            response = requests.get(test.url, proxies=proxies, timeout=timeout, verify=False)
            end_time = time.time()

            if response.status_code == 200 and test.validation_method(response):
                if not detected_ip:
                    detected_ip = extract_ip(response)
                results.append((True, end_time - start_time))
            else:
                results.append((False, None))
        except RequestException:
            results.append((False, None))

    success_rate = sum(1 for r in results if r[0]) / len(results)
    avg_response_time = sum(r[1] for r in results if r[1] is not None) / len(results) if results else 0

    proxy['is_working'] = 'Yes' if success_rate >= 0.5 else 'No'
    proxy['detected_ip'] = detected_ip if detected_ip else "N/A"
    proxy['avg_response_time'] = f"{avg_response_time:.2f}" if avg_response_time else "N/A"

    return proxy


def main():
    proxies = []
    with open('proxies_working.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            proxies.append(row)

    print(f"Cargados {len(proxies)} proxies para verificación.")

    # Usar ThreadPoolExecutor para probar los proxies en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}

        tested_proxies = []
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future.result()
            tested_proxies.append(proxy)

            if proxy['is_working'] == 'Yes':
                print(f"Proxy funcionando: {proxy['host']}:{proxy['port']} - Tiempo: {proxy['avg_response_time']}s - IP: {proxy['detected_ip']}")

    # Ordenar proxies por tiempo de respuesta (solo los que funcionan)
    working_proxies = [p for p in tested_proxies if p['is_working'] == 'Yes']
    working_proxies.sort(key=lambda x: float(x['avg_response_time']))

    # Asegurarnos de que tenemos todos los campos necesarios
    output_fieldnames = fieldnames + ['is_working', 'detected_ip', 'avg_response_time']
    output_fieldnames = list(dict.fromkeys(output_fieldnames))  # Eliminar duplicados si los hay

    # Escribir resultados en un nuevo archivo CSV
    with open('proxies_verified.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_fieldnames)

        writer.writeheader()
        for proxy in working_proxies + [p for p in tested_proxies if p['is_working'] == 'No']:
            writer.writerow(proxy)

    print("\nResultados guardados en 'proxies_verified.csv'")

    print(f"\nProxies funcionando: {len(working_proxies)}/{len(tested_proxies)}")
    for proxy in working_proxies[:10]:  # Mostrar solo los 10 mejores
        print(f"{proxy['host']}:{proxy['port']} ({proxy['country']}) - Anónimo: {proxy['anonymity']}, HTTPS: {proxy['https']}, Tiempo: {proxy['avg_response_time']}s")


if __name__ == "__main__":
    main()
