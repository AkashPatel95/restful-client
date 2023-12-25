
import argparse
import requests
import json
import csv

class RestfulClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self):
        parser = argparse.ArgumentParser(description="Simple command-line REST client.")
        parser.add_argument("method", choices=["get", "post"], help="Request method")
        parser.add_argument("endpoint", help="Request endpoint URI fragment")
        parser.add_argument("-d", "--data", help="Data to send with the request")
        parser.add_argument("-o", "--output", help="Output to .json or .csv file (default: dump to stdout)")

        return parser

    def run(self):
        args = self.parser.parse_args()

        url = f"{self.BASE_URL}{args.endpoint}"
        data = json.loads(args.data) if args.data else None

        if args.method == "get":
            response = self.get_request(url)
        elif args.method == "post":
            response = self.post_request(url, data)

        self.handle_response(response, args.output)

    def get_request(self, url):
        response = requests.get(url)
        return response

    def post_request(self, url, data):
        headers = {"Content-type": "application/json; charset=UTF-8"}
        response = requests.post(url, json=data, headers=headers)
        return response

    def handle_response(self, response, output_file):
        print(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code // 100 != 2:
            print(f"Error: {response.text}")
            exit(1)

        if output_file:
            if output_file.endswith(".json"):
                self.write_json(response.json(), output_file)
            elif output_file.endswith(".csv"):
                self.write_csv(response.json(), output_file)
            else:
                print("Unsupported output format. Please use .json or .csv.")
        else:
            print(json.dumps(response.json(), indent=2))

    def write_json(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data written to {filename}")

    def write_csv(self, data, filename):
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data written to {filename}")

if __name__ == "__main__":
    client = RestfulClient()
    client.run()
