import random
class BandwidthSimulator:
    def simulate_bandwidth(self):
        speeds = [1,3,5,10,20]  # Mbps
        chosen = random.choice(speeds)
        print(f'[Bandwidth] Simulating {chosen} Mbps stream')
        return chosen
