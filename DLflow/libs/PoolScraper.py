import requests
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

"""
Usage:
    scraper = PoolScraper(json=True, workers=5, timeout=180)
    
    requests_data = []
    method = 'POST'
    url = 'http://protectai.com'
    data = {"experiment_ids": [1234],
            "max_results": 9999,
            "run_view_type": "ACTIVE_ONLY",
            "order_by": ["attributes.start_time DESC"]}
    headers = None
    request_data = {'method': method, 'url': url, 'data': data, 'headers': headers}
    requests_data.append(req_data)
    
    responses = scraper.scrape(reqs_data)
    for r in responses:
        print(r.status, r.text)
"""


class PoolScraper:
    def __init__(self, json=False, workers=5, timeout=7200):
        self.failed = []
        self.responses = []
        self.workers = workers
        self.json = json
        self.timeout = timeout

    # Function to fetch data from server
    def fetch(self, session, req_data):
        method = req_data["method"]
        url = req_data["url"]
        headers = req_data["headers"]
        data = req_data["data"]

        if data is not None:
            data = json.dumps(data)
        try:
            if method == "GET":
                with session.get(url) as response:
                    response = self.check_failed(response, req_data)

            elif method == "POST":
                if self.json:
                    with session.post(url, json=data, headers=headers) as response:
                        response = self.check_failed(response, req_data)
                else:
                    with session.post(url, data=data, headers=headers) as response:
                        response = self.check_failed(response, req_data)
        except Exception:
            return None

        return response

    def check_failed(self, response, req_data):
        if response.status_code != 200:
            print(
                f"[-] Failed::{response.status_code}::{req_data['method']} {req_data['url']}"
            )
            self.failed.append(req_data)
        else:
            if req_data in self.failed:
                self.failed.remove(req_data)

        return response

    async def get_data_asynchronous(self, reqs_data):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            with requests.Session() as session:
                # Set any session parameters here before calling `fetch`
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.fetch,
                        *(
                            session,
                            req_data,
                        ),  # Allows us to pass in multiple arguments to `fetch`
                    )
                    for req_data in reqs_data
                ]
                self.responses = await asyncio.gather(*tasks)
                return self.responses

    def do_retries(self, retries, loop, reqs_data):
        while len(self.failed) > 0:
            retries = retries - 1
            self.retry(loop, reqs_data)
            if retries == 0:
                break

    def retry(self, loop, reqs_data):
        future = asyncio.ensure_future(self.get_data_asynchronous(reqs_data))
        self.responses += loop.run_until_complete(future)

    def scrape(self, reqs_data, retries=3):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.get_data_asynchronous(reqs_data))
        self.responses += loop.run_until_complete(future)

        # Retry failures
        self.do_retries(retries, loop, reqs_data)

        # Reset responses so we can reuse this object in more PoolScraper calls
        responses = self.responses
        self.responses = []

        return responses
