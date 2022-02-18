# Household Chores

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/moimartb)
[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmoimart%2Fhousehold-chores)

- Do you need to incentivize your kids to their chores?
- Do you want your kids to be fairly rewarded for their tasks at home?
- Do you want to know when to take care of the next garbage pickup coming to your house?

Household Chores is an application for the whole family to be used with Home Automation systems like [Home Assistant](https://www.home-assistant.io/).

It helps track the daily chores for all members of the family you want and adds a reward when a track is completed. At midnight, the tasks are reset, the scores are accrued and the tracking starts again.

![Kid Chores Dashboard in Home Assistant](https://raw.githubusercontent.com/moimart/household-chores/main/images/kids_chores.jpeg)

Optionally, if you have a Google Calendar with the dates of the Garbage Pickup (very common in Germany, for example), you can create an easier-to-consume sensor that tells when you have to take out your garbage for pickup. As it is a more straightforward sensor, it helps you create more powerful automations. (Don't forget to share your calendar with the service account email)

![Garbage Sensors in Home Assistant](https://raw.githubusercontent.com/moimart/household-chores/main/images/garbage_sensors.jpeg)

## Home Assistant Add-on

You can use Household Chores as a home assistant add-on. To install it, go to Home Assistant Add-on store and search or add this repository from the UI.

After installation, go to the configuration tab and edit the options as follows:

### To add kids

1. You need to add an array for as many kids as you want as follows:

```
kids:
  - id: kid1
    name: Bobby McTrouble
    unit_of_measurement: $ # The type of reward for the scores. It can be money, hours, gummy bears
  - id: kid2
    name: Dennis Mitchell
    unit_of_measurement: 🍭
```

2. Add a second array with all the tasks for your kids. Pay atention for 'kidid' key as that links the task to the specific kid:

```
tasks:
  - kidid: kid1
    id: bed
    name: Do the bed
    value: 1
  - kidid: kid2
    id: grass
    name: Cut the grass of our neighbor George Wilson
    value: 5
```

3. [Optional] If you want to have the sensor for the next garbage pickup. These are the optional configuration parameters to add:

Add the types of garbage and the translations for each. The former uses these strings to identify the events for the garbage pickup. The latter gives the events a more concise name to be shown in the sensor

```
types_of_garbage:
  - Biogut
  - Hausmüll
  - Wertstoffe
  - Paper
garbage_translations:
  - id: Biogut
    tr: Bio
  - id: Hausmüll
    tr: Gray Garbage
  - id: Wertstoffe
    tr: Plastic
  - id: Paper
    tr: Paper
```

In order to access your Google Calendar, you need to create a service account and add the credentials you find in the credentials.json you can get from Google's console. Just populate the same fields into the options as such:

```
  google_service_account:
    type: "(fill the value for this field from credentials.json)"
    project_id: "(fill the value for this field from credentials.json)"
    private_key_id: "(fill the value for this field from credentials.json)"
    private_key: "(fill the value for this field from credentials.json)"
    client_email: "(fill the value for this field from credentials.json)"
    client_id: "(fill the value for this field from credentials.json)"
    auth_uri: "(fill the value for this field from credentials.json)"
    token_uri: "(fill the value for this field from credentials.json)"
    auth_provider_x509_cert_url: "(fill the value for this field from credentials.json)"
    client_x509_url: "(fill the value for this field from credentials.json)"
```

Lastly add how often you want to check the calendar for updates in seconds:

```
update_interval: 43200 # 12 hours = 60*60*12
```

## Home Assistant Stand-alone service

If you want to run this as a separate service, either as local service on a machine or a docker image, you need to:

1. Create a copy of rename_config.yaml and call it chores_config.yaml
2. Populate kids as shown in the example inside of the file _kids.yaml_
3. Configure the garbage types, translations and update interval for calendar fetching as shown in the example of your new _chores_config.yaml_
4. [Optional] if you want to fetch your calendar, create a Google service account and copy the credentials.json file from the Google's Console into the root folder
5. Edit the chores_config.yaml to setup the MQTT client:

```
mqtt:
  username: homeassistant
  password:
  host: "1.2.3.4"
  port: 1883
```

6. Start the service with python start.py

## MQTT-based app

1. Create a copy of rename_config.yaml and call it chores_config.yaml
2. Populate kids as shown in the example inside of the file _kids.yaml_
3. Configure the garbage types, translations and update interval for calendar fetching as shown in the example of your new _chores_config.yaml_
4. [Optional] if you want to fetch your calendar, create a Google service account and copy the credentials.json file from the Google's Console into the root folder
5. Edit the chores_config.yaml to setup the MQTT client:

```
mqtt:
  username: mqtt_user
  password:
  host: "1.2.3.4"
  port: 1883
```

6. Start the service with python start.py

the following MQTT paths are of your interest:

to listen to:

```
kikkei/household/kids/{kid_id}/state => Shows the score of each kid
kikkei/household/garbage/next => Shows the name of the next upcoming garbage pick up
kikkei/household/garbage/next_date => Shows the date or day of the next upcoming garbage pick up
```

to send commands for updates:

```
kikkei/household/{kid_id}/{task_id}/command => Send ON to increase the score of the day; OFF to decrease
```
