import requests, hashlib, json, time, pprint, random
from etek_dimmer import EtekDimmer

class EtekCity:
	
	account_id = ''
	app_version = '2.9.1'
	devices = {}
	devToken = ''
	email = ''
	language = 'en'
	mobile_id = ''
	password = ''
	password_md5 = ''
	phone_brand = 'SM-G930K'
	phone_os = 'Android 5.1.1'
	server_ip = ''
	time_zone = 'America/Manaus'
	token = ''
	user_type = '1'
	printer = pprint.PrettyPrinter(indent=4)
	
	headers = {
			'Content-Type': 'application/json; charset=utf-8',
			'Host': 'smartapi.vesync.com',
			'Connection': 'keep-alive',
			'Accept-Encoding': 'gzip',
			'User-Agent': 'okhttp/3.12.1'
		}
		
	def __init__(self, email, password):
		self.email = email
		self.password = password
		self.password_md5 = hashlib.md5(bytes(self.password, 'utf-8')).hexdigest()
		self.mobile_id = '020000%02x%02x%02x%02x%02x' % (random.randint(0, 255), random.randint(0, 255), 
														random.randint(0, 255), random.randint(0, 255), 
														random.randint(0, 255))
		
	def login(self):
		success = False
		if self.email == '' or self.password == '':
			print ('Credentials are required!')
		else:
			print ('Attempting login...\r\n')
			
			json_data = {
					'acceptLanguage': self.language,
					'accountID': self.account_id,
					'appVersion': self.app_version,
					'devToken': self.devToken,
					'email': self.email,
					'method': "login",
					'password': self.password_md5,
					'phoneBrand': self.phone_brand,
					'phoneOS': self.phone_os,
					'timeZone': self.time_zone,
					'token': self.token,
					'traceId': self.get_time(),
					'userType': self.user_type
				}
			
			url = 'https://smartapi.vesync.com/cloud/v1/user/login'
			response = requests.post(url, headers=self.headers, json=json_data)
			response_json = response.json()
			if response_json['result'] is not None:
				if 'token' in response_json['result']:
					self.account_id = response_json['result']['accountID']
					self.headers['accountID'] = self.account_id
					self.token = response_json['result']['token']
					print ('Account ID: %s' % self.account_id)
					print ('Token: %s' % self.token)
					
					self.headers['tk'] = self.token					
					self.get_time_zone()
					self.headers['tz'] = self.time_zone
					self.get_server()
					self.get_devices()
					
					success = True
			
		return success
		
	def get_time_zone(self):
		url = 'https://smartapi.vesync.com/cloud/v1/user/getUserTimeZone'
		
		json_data = {
				'acceptLanguage': self.language,
				'accountID': self.account_id,
				'appVersion': self.app_version,
				'method': 'getUserTimeZone',
				'phoneBrand': self.phone_brand,
				'phoneOS': self.phone_os,
				'timeZone': self.time_zone,
				'token': self.token,
				'traceId': self.get_time()
			}
			
		response = requests.post(url, headers=self.headers, json=json_data)
		response_json = response.json()
		if response_json['result'] is not None:
			if 'userTimeZone' in response_json['result']:
				self.time_zone = response_json['result']['userTimeZone']
				
		print ('Time Zone: %s' % self.time_zone)
		
		return
		
	def get_server(self):
		url = 'https://smartapi.vesync.com/v1/7A/getServerIP'
		response = requests.get(url, headers=self.headers)
		response_json = response.json()
		
		if response_json is not None:
			if 'serverIP' in response_json:
				self.server_ip = response_json['serverIP']
			
		print ('Server IP: %s' % self.server_ip)
		return
		
	def get_devices(self):
		self.devices = {}
		url = 'https://smartapi.vesync.com/cloud/v2/deviceManaged/devices'
		
		json_data = {
				'acceptLanguage': self.language,
				'accountID': self.account_id,
				'appVersion': self.app_version,
				'method': 'devices',
				'phoneBrand': self.phone_brand,
				'phoneOS': self.phone_os,
				'timeZone': self.time_zone,
				'token': self.token,
				'traceId': self.get_time()
			}
		
		account_info = {
				'account_id': self.account_id,
				'app_version': self.app_version,
				'language': self.language,
				'mobile_id': self.mobile_id,
				'phone_brand': self.phone_brand,
				'phone_os': self.phone_os,
				'server_ip': self.server_ip,
				'time_zone': self.time_zone,
				'token': self.token,
				'user_type': self.user_type,
			}
		
		response = requests.post(url, json=json_data)
		response_json = response.json()
		if response_json['result'] is not None:
			if response_json['result']['total'] > 0:
				for device in response_json['result']['list']:
					if device['deviceType'] == 'ESWD16':
						self.devices[len(self.devices)] = EtekDimmer(device, account_info)
					
		print ('Devices: ')
		self.printer.pprint (self.devices)
			
	
	def get_time(self):
		time_stamp = int(round(time.time() * 1000))
		
		return time_stamp