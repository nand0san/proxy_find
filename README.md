# Proxy Finder and Tester

This repository contains two Python scripts for finding and testing HTTP proxies:

1. `proxie_finder.py`: Extracts free proxies from a public list and performs initial tests.
2. `proxie_test.py`: Conducts advanced tests on the extracted proxies.

Repository: [https://github.com/nand0san/proxy_find](https://github.com/nand0san/proxy_find)

## Requirements

- Python 3.7+
- Required Python packages:
  - requests
  - beautifulsoup4
  - aiohttp

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/nand0san/proxy_find.git
   cd proxy_find
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install requests beautifulsoup4 aiohttp
   ```

## Usage

### Proxy Finder

Run the proxy finder script to gather and initially test proxies:

```
python proxie_finder.py
```

This script will:
- Scrape free proxies from https://free-proxy-list.net/
- Perform initial tests on each proxy
- Save working proxies to `proxies_working.csv`

### Advanced Proxy Tester

After running the finder, use the advanced tester to further verify the proxies:

```
python proxie_test.py
```

This script will:
- Read proxies from `proxies_working.csv`
- Perform advanced tests on each proxy
- Save verified proxies to `proxies_verified.csv`

## Script Details

### proxie_finder.py

- Scrapes proxies from a free proxy list website
- Tests each proxy asynchronously for basic connectivity
- Saves proxies that pass initial tests to a CSV file
- Includes information such as IP, port, country, anonymity level, and HTTPS support

### proxie_test.py

- Reads the proxies extracted by the first script
- Performs more thorough tests, including:
  - Checking multiple URLs (HTTP and HTTPS)
  - Validating responses
  - Measuring response times
- Uses multithreading to test proxies concurrently
- Saves detailed results, including working status, detected IP, and average response time

## Output

Both scripts generate CSV files with the following information:

- Host
- Port
- Country
- Anonymity level
- HTTPS support
- Last checked time
- Extraction date
- Working status
- Detected IP (may differ from the proxy's IP)
- Average response time

### Sample Output

#### proxies_working.csv

```csv
host,port,country,anonymity,https,last_checked,extraction_date,response_time,detected_ip
163.5.196.217,8081,Netherlands,anonymous,no,1 min ago,2024-08-21 13:01:54,0.33,163.5.196.217
74.208.245.106,8888,United States,anonymous,no,1 min ago,2024-08-21 13:01:54,0.35,74.208.245.106
162.223.90.130,80,United States,elite proxy,no,1 min ago,2024-08-21 13:01:54,0.35,162.223.90.130
68.178.203.69,8899,United States,anonymous,no,1 min ago,2024-08-21 13:01:54,0.51,68.178.203.69
20.24.43.214,80,Singapore,elite proxy,no,1 min ago,2024-08-21 13:01:54,0.56,20.24.43.214
15.204.161.192,18080,United States,elite proxy,yes,19 secs ago,2024-08-21 13:01:54,0.77,77.111.247.224
```

#### proxies_verified.csv

```csv
host,port,country,anonymity,https,last_checked,extraction_date,response_time,detected_ip,is_working,avg_response_time
35.185.196.38,3128,United States,anonymous,yes,10 mins ago,2024-08-21 13:01:54,1.15,"10.0.0.73, 34.168.217.206",Yes,0.45
79.175.189.223,1080,Iran,elite proxy,yes,1 min ago,2024-08-21 13:01:54,1.16,79.175.189.223,Yes,1.14
15.204.161.192,18080,United States,elite proxy,yes,19 secs ago,2024-08-21 13:01:54,0.77,77.111.247.62,Yes,1.52
181.188.27.162,8080,Trinidad and Tobago,elite proxy,yes,1 min ago,2024-08-21 13:01:54,7.91,181.188.27.162,Yes,3.35
189.240.60.168,9090,Mexico,elite proxy,yes,1 min ago,2024-08-21 13:01:54,3.55,189.240.60.168,Yes,4.31
47.251.43.115,33333,United States,anonymous,yes,1 min ago,2024-08-21 13:01:54,12.92,47.251.43.115,Yes,4.61
189.240.60.163,9090,Mexico,elite proxy,yes,19 secs ago,2024-08-21 13:01:54,3.69,189.240.60.168,Yes,4.80
```

## Notes

- The scripts use SSL verification disabling, which should be used cautiously in production environments.
- Proxy availability and performance can change rapidly. Regular re-testing is recommended.
- Using free proxies comes with risks. Use at your own discretion and avoid transmitting sensitive data.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/nand0san/proxy_find/issues) if you want to contribute.

## License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.