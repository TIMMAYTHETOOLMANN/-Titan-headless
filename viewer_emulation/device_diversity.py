import random
class DeviceEmulator:
    def get_user_agent(self):
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (Linux; Android 10)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)'
        ]
        ua = random.choice(ua_list)
        print(f'[Device Emulation] Using User-Agent: {ua}')
        return ua
