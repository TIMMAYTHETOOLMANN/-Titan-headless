import random
class GeoIPRotator:
    def rotate_proxy(self):
        countries = ['US','UK','JP','IN','DE']
        proxy = f"http://{random.choice(countries)}.proxy.server"
        print(f'[Geo-IP] Rotating to proxy: {proxy}')
        return proxy
