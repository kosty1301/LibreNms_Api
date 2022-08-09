#!/usr/bin/python3

# Original https://github.com/RaymiiOrg/librenms-api-alerts
# Docs https://github.com/librenms/librenms/tree/master/doc/API

import requests


class LibreNMSAPI:
	def __init__(self, auth_token, request_headers, api_url):
		self.api_url = api_url
		self.headers = request_headers
		self.auth_token = auth_token
		self.devices_url = self.api_url + "devices/"
		self.alerts_url = self.api_url + "alerts"
		self.alert_url = self.api_url + "alert/"
		self.service_url = self.api_url + "services/"
		self.rules_url = self.api_url + "rules/"

	def get_json_response(self, url):
		return requests.get(url, headers=self.headers).json()

	def get_alert_rule(self, rule_id):
		url = self.rules_url + str(rule_id)
		return self.get_json_response(url)["rules"][0]

	def get_alert(self, alert_id):
		url = self.alert_url + str(alert_id)
		return self.get_json_response(url)

	def list_sevice_critical(self):
		url = self.service_url + '?state=2'
		return self.get_json_response(url)['services'][0]

	def list_devices(self):
		url = self.devices_url
		return self.get_json_response(url)["devices"]

	def get_device(self, device_id):
		url = self.devices_url + str(device_id)
		return self.get_json_response(url)["devices"][0]

	def get_all_or_type_devices(self, dev_type=None):
		url = self.devices_url
		response = self.get_json_response(url)["devices"]
		if dev_type:
			return [device for device in response if device['os'] == dev_type]
		return response

	def get_service_for_device(self, hostname):
		url = self.service_url + hostname
		return self.get_json_response(url)["services"][0]

	def add_service_for_device(self, hostname, data):
		url = self.service_url + hostname
		return requests.post(url, headers=self.headers, json=data).json()

	def delete_service_via_id(self, service_id):
		url = self.service_url + str(service_id)
		return requests.delete(url, headers=self.headers).json()

	# Patch requests Don't Work in LibreNms :(
	def edit_service_via_id(self, service_id, data):
		req = self.service_url + str(service_id)
		return requests.patch(req, headers=self.headers, json=data).json()

	def service_is_already_added(self, hostname, service_desc):
		services = self.get_service_for_device(hostname)
		for service in services:
			if service['service_desc'] == service_desc:
				return service
		return False


if __name__ == "__main__":


	# Exemple:
	auth_token = "Your_Token"
	api_url = "https://exemple.com/api/v0/"

	request_headers = {
		"Accept-Language": "en-US,en;q=0.5",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"X-Auth-Token": auth_token,
		"Connection": "keep-alive"
	}

	api = LibreNMSAPI(
		auth_token=auth_token,
		request_headers=request_headers,
		api_url=api_url
	)
	alerts = api.list_sevice_critical()
	for alert in alerts:
		print(alert)
