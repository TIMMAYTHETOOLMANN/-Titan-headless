import random
class EngagementAI:
    def decide_watch_time(self, video_length: int):
        watch_time = random.randint(int(video_length*0.4), video_length)
        print(f'[Engagement AI] Decided watch time: {watch_time}s')
        return watch_time
