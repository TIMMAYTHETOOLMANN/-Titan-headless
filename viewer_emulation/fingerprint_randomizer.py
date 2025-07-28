import random
class FingerprintRandomizer:
    def randomize_fingerprint(self):
        fingerprint = {
            'canvas': random.randint(1000,9999),
            'webgl': random.randint(1000,9999),
            'audio': random.randint(1000,9999)
        }
        print(f'[Fingerprint] Randomized: {fingerprint}')
        return fingerprint
