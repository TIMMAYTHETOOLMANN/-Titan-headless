import random, time
class BufferingSimulator:
    def simulate_buffering(self):
        events = random.randint(1,3)
        for _ in range(events):
            print('[Buffering] Simulating network lag...')
            time.sleep(random.uniform(1.0, 2.5))
        return events
