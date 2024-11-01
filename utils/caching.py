import redis
import pickle

class CacheManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)
    
    def cache_recommendations(self, user_id, recommendations, expiration=3600):
        data = pickle.dumps(recommendations)
        self.r.setex(f"rec:{user_id}", expiration, data)
    
    def get_cached_recommendations(self, user_id):
        data = self.r.get(f"rec:{user_id}")
        if data:
            return pickle.loads(data)
        else:
            return None
