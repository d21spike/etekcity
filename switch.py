from .required.etekcity import EtekCity
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA

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
        _LOGGER.error("Could not connect to EvSync")
        return

    for device_num in etek.devices:
        if etek.devices[device_num].Device_Family == "Switches":
            devices.append(EtekSwitch(hass, etek.devices[device_num]))

    if len(devices):
        add_entities(devices)
    else:
        _LOGGER.error("Could not locate the EtekCity switch named %s" % switch_name)


class EtekSwitch(SwitchDevice):

    def __init__(self, hass, switch):
        _LOGGER.info("Initializing EtekSwitch %s" % switch.Name)

        self._hass = hass
        self._name = switch.Name
        self._state = False
        if switch.Status == "on": self._state = True
        self.switch = switch


    def _switch(self, state):
        _LOGGER.info("Toggling EtekSwitch %s to state %s" % (self._name, state))

        self.switch.set_status(state)
        if self.switch.Status == state:
            return True


    def _query_state(self):
        _LOGGER.info("Querying state for EtekSwitch %s" % self._name)

        self.switch.device_info()
        if self.switch.Status == "on": return True


    @property
    def should_poll(self):
        """ Return the polling state """
        return True


    @property
    def name(self):
        """ Return the name of the switch """
        return self._name


    @property
    def is_on(self):
        return self._state


    def update(self):
        """ Update device state """
        self._state = self._query_state()


    def turn_on(self, **kwargs):
        """ Turn on switch """
        if self._switch("on"): self._state = True


    def turn_off(self, **kwargs):
        """ Turn off switch """
        if self._switch("off"): self._state = False
