import requests, hashlib, json, time, pprint

class EtekDimmer:

        Active_Time = 0
        Brightness = 0
        CID = ''
        Config_Type = ''
        Connection_Status = ''
        Connection_Type = ''
        Device_Type = ''
        Device_Family = ''
        Image = ''
        Indicator_light = 'off'
        Name = ''
        Region = ''
        RGB_Status = 'off'
        RGB_Red = 0
        RGB_Green = 0
        RGB_Blue = 0
        Status = ''
        UUID = ''

        printer = pprint.PrettyPrinter(indent=4)
        headers = {
                        'accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Host': 'smartapi.vesync.com',
                        'Connection': 'Keep-Alive',
                        'Accept-Encoding': 'gzip',
                        'User-Agent': 'okhttp/3.12.1'
                }
        account_info = {}

        def __init__(self, device_json, account_info):
                self.CID = device_json['cid']
                self.Config_Type = device_json['configModule']
                self.Connection_Status = device_json['connectionStatus']
                self.Connection_Type = device_json['connectionType']
                self.Image = device_json['deviceImg']
                self.Name = device_json['deviceName']
                self.Region = device_json['deviceRegion']
                self.Status = device_json['deviceStatus']
                self.Device_Type = device_json['deviceType']
                self.Device_Family = device_json['type']
                self.UUID = device_json['uuid']
                self.account_info = account_info

                self.headers['tk'] = self.account_info['token']
                self.headers['accountid'] = self.account_info['account_id']
                self.headers['tz'] = self.account_info['time_zone']
                self.headers['accept-language'] = self.account_info['language']
                self.headers['appversion'] = self.account_info['app_version']

                self.device_info()

        def device_info(self):
                url = 'https://smartapi.vesync.com/dimmer/v1/device/devicedetail'

                json_data = {
                        'acceptLanguage': self.account_info['language'],
                        'accountID': self.account_info['account_id'],
                        'appVersion': self.account_info['app_version'],
                        'method': 'devicedetail',
                        'mobileId': self.account_info['mobile_id'],
                        'phoneBrand': self.account_info['phone_brand'],
                        'phoneOS': self.account_info['phone_os'],
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'traceId': self.get_time(),
                        'uuid': self.UUID
                        }

                response = requests.post(url, headers=self.headers, json=json_data)
                response_json = response.json()
                if response_json is not None:
                        if 'activeTime' in response_json:
                                self.Active_Time = response_json['activeTime']
                        if 'brightness' in response_json:
                                self.Brightness = int(response_json['brightness'])
                        if 'connectionStatus' in response_json:
                                self.Connection_Status = response_json['connectionStatus']
                        if 'deviceImg' in response_json:
                                self.Image = response_json['deviceImg']
                        if 'deviceStatus' in response_json:
                                self.Status = response_json['deviceStatus']
                        if 'devicename' in response_json:
                                self.Name = response_json['devicename']
                        if 'indicatorlightstatus' in response_json:
                                self.Indicator_light = response_json['indicatorlightstatus']
                        if 'rgbStatus' in response_json:
                                self.RGB_Status = response_json['rgbStatus']
                        if 'rgbValue' in response_json:
                                self.RGB_Red = response_json['rgbValue']['red']
                                self.RGB_Green = response_json['rgbValue']['green']
                                self.RGB_Blue = response_json['rgbValue']['blue']

                return

        def set_brightness(self, brightness):
                print ('Current Brightness: %i' % self.Brightness)
                if brightness == self.Brightness:
                        print ('Requested brightness matches current brightness, no change needed.')
                        return

                url = 'https://smartapi.vesync.com/dimmer/v1/device/updatebrightness'

                json_data = {
                        'accountID': self.account_info['account_id'],
                        'brightness': brightness,
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'uuid': self.UUID
                        }

                response = requests.put(url, headers=self.headers, json=json_data)
                self.device_info()

                print ('New Brightness: %i' % self.Brightness)

                return

        def set_status(self, status):
                print ('Current Status: %s' % self.Status)
                if status == self.Status:
                        print ('Requested status matches current status, no change needed.')
                        return

                url = 'https://smartapi.vesync.com/dimmer/v1/device/devicestatus'

                json_data = {
                        'accountID': self.account_info['account_id'],
                        'status': status,
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'uuid': self.UUID
                        }

                response = requests.put(url, headers=self.headers, json=json_data)
                self.device_info()

                print ('New Status: %s' % self.Status)

                return

        def set_rgb(self, status, red, green, blue):
                print ('Current RGB Status: %s, Values: R:%i | G:%i | B:%i' %
                        (self.RGB_Status, self.RGB_Red, self.RGB_Green, self.RGB_Blue))
                if status == self.RGB_Status and red == self.RGB_Red and green == self.RGB_Green and blue == self.RGB_Blue:
                        print ('Requested changes match current values, no change needed.')
                        return

                url = 'https://smartapi.vesync.com/dimmer/v1/device/devicergbstatus'

                json_data = {
                        'accountID': self.account_info['account_id'],
                        'rgbValue': {
                                        'blue': blue,
                                        'green': green,
                                        'red': red
                                },
                        'status': status,
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'uuid': self.UUID
                        }

                response = requests.put(url, headers=self.headers, json=json_data)
                self.device_info()

                print ('New RGB Status: %s, Values: R:%i | G:%i | B:%i' %
                        (self.RGB_Status, self.RGB_Red, self.RGB_Green, self.RGB_Blue))

                return

        def set_rgb_status(self, status):
                print ('Current RGB Status: %s' % self.RGB_Status)
                if status == self.RGB_Status:
                        print ('Requested status matches current status, no change needed.')
                        return

                url = 'https://smartapi.vesync.com/dimmer/v1/device/devicergbstatus'

                json_data = {
                        'accountID': self.account_info['account_id'],
                        'status': status,
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'uuid': self.UUID
                        }

                response = requests.put(url, headers=self.headers, json=json_data)
                self.device_info()

                print ('New RGB Status: %s' % self.RGB_Status)

                return

        def set_rgb_color(self, red, green, blue):
                print ('Current RGB Values: R:%i | G:%i | B:%i' % (self.RGB_Red, self.RGB_Green, self.RGB_Blue))
                if red == self.RGB_Red and green == self.RGB_Green and blue == self.RGB_Blue:
                        print ('Requested changes match current values, no change needed.')
                        return

                url = 'https://smartapi.vesync.com/dimmer/v1/device/devicergbstatus'

                json_data = {
                        'accountID': self.account_info['account_id'],
                        'rgbValue': {
                                        'blue': blue,
                                        'green': green,
                                        'red': red
                                },
                        'status': self.RGB_Status,
                        'timeZone': self.account_info['time_zone'],
                        'token': self.account_info['token'],
                        'uuid': self.UUID
                        }

                response = requests.put(url, headers=self.headers, json=json_data)
                self.device_info()

                print ('New RGB Values: R:%i | G:%i | B:%i' % (self.RGB_Red, self.RGB_Green, self.RGB_Blue))

                return

        def print_info(self):
                self.device_info()

                print ('================ %s Dimmer Info ================' % self.Name)
                print ('Active Time: %i' % self.Active_Time)
                print ('Brightness: %i' % self.Brightness)
                print ('CID: %s' % self.CID)
                print ('Config Type: %s' % self.Config_Type)
                print ('Connection Status: %s' % self.Connection_Status)
                print ('Connection Type: %s' % self.Connection_Type)
                print ('Device Type: %s' % self.Device_Type)
                print ('Device Family: %s' % self.Device_Family)
                print ('Device Image: %s' % self.Image)
                print ('Indicator Light: %s' % self.Indicator_light)
                print ('Name: %s' % self.Name)
                print ('Region: %s' % self.Region)
                print ('RGB Status: %s' % self.RGB_Status)
                print ('RGB Values: R:%i | G:%i | B:%i' % (self.RGB_Red, self.RGB_Green, self.RGB_Blue))
                print ('Status: %s' % self.Status)
                print ('UUID: %s' % self.UUID)
                print ('================================================')

                return

        def get_time(self):
                time_stamp = int(round(time.time() * 1000))

                return time_stamp