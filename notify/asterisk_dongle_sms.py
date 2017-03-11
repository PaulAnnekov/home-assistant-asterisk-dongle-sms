"""
Asterisk Dongle SMS send platform for notify component.
"""
import logging

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TARGET, BaseNotificationService, PLATFORM_SCHEMA)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['asterisk-ami==0.1.0']

CONF_DONGLE = 'dongle'
CONF_ADDRESS = 'address'
CONF_PORT = 'port'
CONF_USER = 'user'
CONF_PASSWORD = 'password'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DONGLE): cv.string,
    vol.Required(CONF_ADDRESS): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.Required(CONF_USER): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

_LOGGER = logging.getLogger(__name__)


def get_service(hass, config):
    """Get the Asterisk notification service."""
    dongle = config.get(CONF_DONGLE)
    address = config.get(CONF_ADDRESS)
    port = config.get(CONF_PORT)
    user = config.get(CONF_USER)
    password = config.get(CONF_PASSWORD)

    return AsteriskNotificationService(dongle, address, port, user, password)


class AsteriskNotificationService(BaseNotificationService):
    """Implementation of a notification service for Asterisk."""

    def __init__(self, dongle, address, port, user, password):
        """Initialize the service."""
        self._dongle = dongle
        self._address = address
        self._port = port
        self._user = user
        self._password = password

    def send_message(self, message="", **kwargs):
        """Send an SMS to target users."""
        from asterisk.ami import AMIClient
        from asterisk.ami.action import SimpleAction

        client = AMIClient(address=self._address, port=self._port)
        client.login(username=self._user, secret=self._password)

        targets = kwargs.get(ATTR_TARGET)

        if targets is None:
            _LOGGER.exception("No SMS targets, as 'target' is not defined")
            return

        # TODO: add quota per day
        for target in targets:
            _LOGGER.debug("Sending SMS to %s", target)
            action = SimpleAction(
                'DongleSendSMS',
                Device=self._dongle,
                Number=target,
                Message=message,
            )
            client.send_action(action, callback=lambda r: self._on_message(target, r))
            _LOGGER.debug("SMS to %s sent", target)

        client.logoff()

    def _on_message(self, phone, response):
        if response.status is not 'Success':
            _LOGGER.exception("Error sending SMS to %s. Response %s. Keys: %s", phone, response.status, response.keys)
        else:
            _LOGGER.debug("SMS to %s successful", phone)
