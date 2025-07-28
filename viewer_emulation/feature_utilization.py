import random
class FeatureUtilizer:
    def utilize_features(self):
        features = ['add_to_playlist','autoplay_chain','watch_later']
        feature = random.choice(features)
        print(f'[Feature Utilization] Engaging: {feature}')
        return feature
