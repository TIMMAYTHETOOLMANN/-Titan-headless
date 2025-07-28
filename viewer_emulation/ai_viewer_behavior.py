import random, time
class ViewerBehavior:
    def simulate_actions(self, duration: int):
        actions = ['pause','play','seek','volume_change']
        for _ in range(duration):
            action = random.choice(actions)
            print(f'[AI Behavior] Performing {action}')
            time.sleep(random.uniform(0.5, 3.0))
