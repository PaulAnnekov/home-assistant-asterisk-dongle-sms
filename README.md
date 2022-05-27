# Home Assistant SMS Notification via Asterisk AMI DongleSendSMS

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

This notification component allows you to send SMS via your GSM dongle connected to Asterisk via 
[chan_dongle](https://github.com/bg111/asterisk-chan-dongle) driver. It uses Asterisk AMI api to send DongleSendSMS 
command.

## Installation

### HACS

[Guide](https://hacs.xyz/docs/faq/custom_repositories/)

### Manual

Copy `custom_components/asterisk_dongle_sms/` contents from repo into `custom_components/asterisk_dongle_sms/` 
   [directory](https://home-assistant.io/developers/component_loading/).

## Configuration

1. Configure Asterisk AMI by editing `/etc/asterisk/manager.conf`:
   
   ```ini
   [general]
   # enables AMI api
   enabled = yes
   # sets listen port
   port = 5038
   # listen interface
   bindaddr = 127.0.0.1
   
   # user name
   [smart-home]
   # user password
   secret=your_password
   # privileges, that's all we need for calling DongleSendSMS
   read=call
   write=call
   ```
   
   Restart Asterisk.
   
2. Add the following lines to the `configuration.yaml`:

  ```yaml
  notify:
    - name: sms
      platform: asterisk_dongle_sms
      dongle: dongle0 # insert your dongle name, run `dongle show devices` in Asterisk CLI and check `ID` column
      address: localhost # Asterisk server IP address
      port: 5038 # Asterisk AMI port
      user: smart-home # Asterisk AMI user name
      password: your_password # Asterisk AMI user password
  ```

5. Add [automation](https://home-assistant.io/docs/automation/action/).
