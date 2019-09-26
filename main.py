from etekcity import EtekCity
		
		
def main():
	etek_city = EtekCity('', '')
	if etek_city.login():
		dimmer = etek_city.devices[0]
		dimmer.print_info()
		# dimmer.set_brightness(50)
		# dimmer.set_status('off')
		# dimmer.set_rgb_status('off')
		# dimmer.set_rgb_color(255, 0, 0)
		# dimmer.set_rgb('on', 255, 255, 0)
	
	
main()