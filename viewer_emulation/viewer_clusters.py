import random
class ViewerCluster:
    def simulate_cluster(self, viewers: int):
        print(f'[Cluster Simulation] Simulating {viewers} viewer group')
        return [{'viewer_id': i, 'behavior': random.choice(['active','passive'])}
                for i in range(viewers)]
