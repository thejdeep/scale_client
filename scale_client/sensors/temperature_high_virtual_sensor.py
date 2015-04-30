from scale_client.sensors.virtual_sensor import VirtualSensor

import logging
log = logging.getLogger(__name__)


class TemperatureHighVirtualSensor(VirtualSensor):
    def __init__(self, broker, device=None, threshold=28.0):
        super(TemperatureHighVirtualSensor, self).__init__(broker=broker, device=device, interval=None)
        self._threshold = threshold

    def get_type(self):
        return "temperature_high"

    def on_event(self, event, topic):
        et = event.get_type()
        ed = event.get_raw_data()

        if et != "temperature":
            return

        if ed > self._threshold:
            new_event = self.make_event_with_raw_data(raw, priority=4)
            new_event.data["condition"] = {
                    "threshold": {
                        "operator": ">",
                        "value": self._threshold
                    }
                }
            self.publish(new_event)

    def policy_check(self, event):
        return False
