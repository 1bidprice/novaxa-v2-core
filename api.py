import requests

class TelegramAPI:
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        self.session = requests.Session()

    def send_message(self, chat_id, text):
        url = self.api_url + "sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        return self.session.post(url, data=payload)

    def delete_webhook(self):
        url = self.api_url + "deleteWebhook"
        return self.session.post(url)

    def set_webhook(self, url):
        full_url = self.api_url + "setWebhook"
        return self.session.post(full_url, data={"url": url})


class DataProcessor:
    def format_user(self, user):
        return f"{user.first_name} ({user.id})"
