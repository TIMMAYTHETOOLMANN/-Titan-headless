import random
class HumanInteraction:
    def simulate_engagement(self):
        actions = ['like','subscribe','comment','toggle_captions']
        action = random.choice(actions)
        print(f'[Human Interaction] Performing: {action}')
        return action
