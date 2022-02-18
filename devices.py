device = {
    "identifiers": ["Kikkei Labs Household"],
    "name": "Household Activities Calendar",
    "model": "Kikkei-household-0",
    "manufacturer": "Kikkei Labs",
}

garbage_config = {
    "mqtt_topic_next": "homeassistant/sensor/kikkei/household_next/config",
    "mqtt_payload_next": {
        "availability_topic": "kikkei/household/garbage",
        "state_topic": "kikkei/household/garbage/next",
        "name": "Next Garbage",
        "unique_id": "next_garbage",
        "payload_available": "ON",
        "payload_not_available": "OFF",
        "device": device
    },
    "mqtt_topic_next_date": "homeassistant/sensor/kikkei/household_next_date/config",
    "mqtt_payload_next_date": {
        "availability_topic": "kikkei/household/garbage",
        "state_topic": "kikkei/household/garbage/next_date",
        "name": "Next Garbage Day",
        "unique_id": "next_garbage_date",
        "payload_available": "ON",
        "payload_not_available": "OFF",
        "device": device
    }
}

kids_device = {
    "identifiers": ["Kid"],
    "name": "Household Chores's #'s Activities",
    "model": "Kikkei-household-1",
    "manufacturer": "Kikkei Labs",
}

hass_kid_entity = {
    "generic_switch": 'homeassistant/switch/kikkei-kids-#/?-switch/config',
    "generic_switch_config": {
        "availability_topic": "kikkei/household/garbage",
        "state_topic": "kikkei/household/kids/#/?/state",
        "name": "",
        "unique_id": "",
        "object_id": "",
        "payload_available": "ON",
        "payload_not_available": "OFF",
        #"json_attributes_topic": "kikkei/household/#/%/attributes",
        "state_on": "true",
        "state_off": "false",
        "command_topic": "kikkei/household/#/?/command",
        "device": kids_device
    }
}

hass_kid_sensor = {
    "generic_sensor": "homeassistant/sensor/kikkei-kids-#/config",
    "generic_sensor_config": {
        "availability_topic": "kikkei/household/garbage",
        "state_topic": "kikkei/household/kids/#/state",
        "name": "",
        "unique_id": "",
        "payload_available": "ON",
        "payload_not_available": "OFF",
        #"json_attributes_topic": "kikkei/household/#/attributes",
        "device": kids_device
    }
}
