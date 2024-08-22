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

1. For default tests:
   ```
   python proxie_test.py
   ```

2. For testing with a specific target URL:
   ```
   python proxie_test.py --target https://example.com
   ```

This script will:
- Read proxies from `proxies_working.csv`
- Perform advanced tests on each proxy (either default tests or against the specified target URL)
- Provide real-time feedback on the testing progress
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
  - Checking multiple URLs (HTTP and HTTPS) or a specific target URL
  - Validating responses
  - Measuring response times
- Provides real-time feedback on testing progress
- Saves detailed results, including working status, detected IP, and average response time
- Allows custom tests to be easily added

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
- Test results for each URL tested

### Sample Output

`proxies_working.csv`
```
host,port,country,anonymity,https,last_checked,extraction_date,response_time,detected_ip
20.111.54.16,8123,France,elite proxy,no,1 min ago,2024-08-22 11:33:14,0.35,20.111.54.16
20.206.106.192,8123,Brazil,elite proxy,no,1 min ago,2024-08-22 11:33:14,0.53,20.206.106.192
162.223.90.130,80,United States,elite proxy,no,1 min ago,2024-08-22 11:33:14,0.55,162.223.90.130
...

```

`proxies_verified.csv`
```
host,port,country,anonymity,https,last_checked,extraction_date,response_time,detected_ip,is_working,avg_response_time,test_http://httpbin.org/ip,test_https://api.ipify.org,test_https://www.google.com
94.242.240.36,3128,Luxembourg,anonymous,yes,1 min ago,2024-08-22 11:33:14,0.80,94.242.240.36,Yes,0.38,Pass,Pass,Pass
15.204.161.192,18080,United States,elite proxy,yes,20 mins ago,2024-08-22 11:33:14,1.44,77.111.247.46,Yes,0.52,Pass,Pass,Fail
181.188.27.162,8080,Trinidad and Tobago,elite proxy,yes,20 mins ago,2024-08-22 11:33:14,1.62,181.188.27.162,Yes,0.59,Pass,Pass,Fail
...
```

## Notes

- The scripts use SSL verification disabling, which should be used cautiously in production environments.
- Proxy availability and performance can change rapidly. Regular re-testing is recommended.
- Using free proxies comes with risks. Use at your own discretion and avoid transmitting sensitive data.
- The timeout for each proxy test is set to 5 seconds to balance between thoroughness and speed.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/nand0san/proxy_find/issues) if you want to contribute.

## License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.