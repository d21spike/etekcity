from .required.etekcity import EtekCity
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import Light, PLATFORM_SCHEMA, ATTR_BRIGHTNESS

_LOGGER = logging.getLogger(__name__)

CONF_DOMAIN = "etekcity"
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    
    email = config[CONF_EMAIL]
    password = config[CONF_PASSWORD]
    devices = []

    etek = EtekCity(email, password)
    if not etek.login():
        _LOGGER.error("Could not connect to VeSync")
        return

    for device_num in etek.devices:
        if etek.devices[device_num].Device_Type == "ESWD16":
            devices.append(EtekSwitchLight(hass, etek.devices[device_num]))

    if len(devices):
        add_entities(devices)
    else:
        _LOGGER.error("Could not locate any EtekCity switches")
        
        
class EtekSwitchLight(Light):
    
    def __init__(self, hass, light):
        _LOGGER.info("Initializing EtekSwitchLight %s" % light.Name)
        
        self._hass = hass
        self._name = light.Name
        self._state = False
        if light.RGB_Status == "on": self._state = True
        self.brightness = light.Brightness
        self.color = { "Red": 0, "Green": 0, "Blue": 0 }
        self.light = light
        
    
    def _switch(state):
        _LOGGER.info("Toggling EtekSwitchLight %s to state %s" % (self._name, state))
        
        self.light.set_rgb_status(state)
        if self.light.Status == state:
            return True
    
    
    def _query_state(self):
        _LOGGER.info("Querying state for EtekSwitchLight %s" % self._name)
        
        self.light.device_info()
        if self.light.RGB_Status == "on": return True
        
    @property
    def name(self):
        """ Return the name of the light """
        return self._name
        
        
    @property
    def brightness(self):
        """ Return the birghtness of the light """
        return self.brightness
        
        
    @property
    def is_on(self):
        """ Return if the light is on """
        return self._state
    
    def update(self):
        """ Update device state """
        self._state = self._query_state()
            
    
    def turn_on(self, **kwargs):
        """ Turn on switch RGB Light """
        if self._light("on"): self._state = True
        
        
    def turn_off(self, **kwargs):
        """ Turn off switch RGB Light """
        if self._light("off"): self._state = False