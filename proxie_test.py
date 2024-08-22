import csv
import requests
import time
from collections import namedtuple
from requests.exceptions import RequestException
import urllib3
import argparse

# Desactivar advertencias de SSL inseguro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ProxyTest = namedtuple('ProxyTest', ['url', 'validation_method'])


def validate_url(response, url_string: str) -> bool:
    """Verify that expected url is in response text."""
    return url_string in response.text.lower()


def validate_ip_response(response):
    try:
        json_response = response.json()
        return 'ip' in json_response or 'origin' in json_response
    except ValueError:
        return len(response.text.strip()) < 50  # Asumimos que es una IP si es un texto corto


def extract_ip(response):
    try:
        json_response = response.json()
        return json_response.get('ip') or json_response.get('origin')
    except ValueError:
        return response.text.strip() if len(response.text.strip()) < 50 else None


def test_proxy(proxy, tests, timeout=5):
    proxy_url = f"http://{proxy['host']}:{proxy['port']}"
    proxies = {"http": proxy_url, "https": proxy_url}
    results = []
    detected_ip = None

    for test in tests:
        try:
            start_time = time.time()
            response = requests.get(test.url, proxies=proxies, timeout=timeout, verify=False)
            end_time = time.time()

            if response.status_code == 200 and test.validation_method(response):
                if not detected_ip and test.url in ['http://httpbin.org/ip', 'https://api.ipify.org']:
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
    proxy['test_results'] = {test.url: 'Pass' if result[0] else 'Fail' for test, result in zip(tests, results)}

    return proxy


def main(tests):
    proxies = []
    with open('proxies_working.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            proxies.append(row)

    print(f"Cargados {len(proxies)} proxies para verificación.")

    tested_proxies = []
    for i, proxy in enumerate(proxies, 1):
        print(f"Probando proxy {i}/{len(proxies)}: {proxy['host']}:{proxy['port']}...", end='', flush=True)
        tested_proxy = test_proxy(proxy, tests)
        tested_proxies.append(tested_proxy)

        if tested_proxy['is_working'] == 'Yes':
            print(f" Funcionando - Tiempo: {tested_proxy['avg_response_time']}s - IP: {tested_proxy['detected_ip']}")
            for url, result in tested_proxy['test_results'].items():
                print(f"  {url}: {result}")
        else:
            print(" No funciona")

    # Ordenar proxies por tiempo de respuesta (solo los que funcionan)
    working_proxies = [p for p in tested_proxies if p['is_working'] == 'Yes']
    working_proxies.sort(key=lambda x: float(x['avg_response_time']))

    # Asegurarnos de que tenemos todos los campos necesarios
    output_fieldnames = fieldnames + ['is_working', 'detected_ip', 'avg_response_time'] + [f"test_{url}" for url, _ in tests]
    output_fieldnames = list(dict.fromkeys(output_fieldnames))  # Eliminar duplicados si los hay

    # Escribir resultados en un nuevo archivo CSV
    with open('proxies_verified.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_fieldnames)

        writer.writeheader()
        for proxy in working_proxies + [p for p in tested_proxies if p['is_working'] == 'No']:
            row = proxy.copy()
            for url, result in proxy['test_results'].items():
                row[f"test_{url}"] = result
            del row['test_results']
            writer.writerow(row)

    print("\nResultados guardados en 'proxies_verified.csv'")

    print(f"\nProxies funcionando: {len(working_proxies)}/{len(tested_proxies)}")
    for proxy in working_proxies[:10]:  # Mostrar solo los 10 mejores
        print(f"{proxy['host']}:{proxy['port']} ({proxy['country']}) - Anónimo: {proxy['anonymity']}, HTTPS: {proxy['https']}, Tiempo: {proxy['avg_response_time']}s")
        for url, result in proxy['test_results'].items():
            print(f"  {url}: {result}")


if __name__ == "__main__":
    # Definir los tests predeterminados
    DEFAULT_TESTS = [
        ProxyTest('http://httpbin.org/ip', validate_ip_response),
        ProxyTest('https://api.ipify.org', validate_ip_response),
        ProxyTest('https://www.google.com', lambda r: validate_url(r, 'google'))
    ]

    # Para añadir un nuevo test personalizado, simplemente agrega una nueva entrada a DEFAULT_TESTS.
    # Por ejemplo:
    # DEFAULT_TESTS.append(ProxyTest('https://example.com', lambda r: validate_url(r, 'example')))

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Test proxies with optional target URL.')
    parser.add_argument('--target', help='Target URL to test')

    args = parser.parse_args()

    # Determinar qué tests usar
    if args.target:
        tests = [ProxyTest(args.target, lambda r: validate_url(r, args.target.split('//')[1]))]
        print(f"Probando proxies con URL objetivo: {args.target}")
    else:
        tests = DEFAULT_TESTS
        print("Probando proxies con tests predeterminados")

    # Ejecutar el programa principal
    main(tests)
