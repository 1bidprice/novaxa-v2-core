class ServiceIntegration:
    def __init__(self):
        self.services = {}

    def register_service(self, name, handler):
        self.services[name] = handler

    def handle_event(self, service, event_data):
        if service in self.services:
            return self.services[service](event_data)
        return f"Service {service} not found."


class NotificationSystem:
    def send_alert(self, message):
        print(f"[ALERT] {message}")
