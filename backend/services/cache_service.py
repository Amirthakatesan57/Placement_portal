"""
Redis Cache Service Layer
Milestone 8: API Performance Optimization and Caching Using Redis

This service provides:
- Cache get/set/delete operations
- Cache key generation
- Cache expiry management
- Cache invalidation strategies
"""

import redis
import json
import hashlib
import logging
from datetime import datetime, timezone
from functools import wraps
from flask import current_app, request

logger = logging.getLogger(__name__)

# Cache expiry times (in seconds)
CACHE_EXPIRY = {
    'default': 300,              # 5 minutes
    'job_listings': 600,         # 10 minutes
    'company_search': 300,       # 5 minutes
    'student_search': 300,       # 5 minutes
    'dashboard_stats': 180,      # 3 minutes
    'user_profile': 600,         # 10 minutes
    'placement_stats': 900,      # 15 minutes
    'admin_stats': 120,          # 2 minutes
}


class CacheService:
    """
    Redis Cache Service for API Optimization
    Milestone 8: Performance Optimization
    """
    
    def __init__(self, redis_url='redis://localhost:6379/0'):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            logger.info("Redis cache service initialized successfully")
        except Exception as e:
            logger.warning(f" Redis cache disabled: {str(e)}")
            self.enabled = False
            self.redis_client = None
    
    def _generate_key(self, prefix, *args, **kwargs):
        """
        Generate unique cache key from arguments
        
        Args:
            prefix: Key prefix (e.g., 'job_listings')
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            str: Unique cache key
        """
        # Create hash from arguments
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"ppa_v3:{prefix}:{key_hash}"
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.enabled or not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            else:
                logger.debug(f"Cache MISS: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
    
    def set(self, key, value, expiry=None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expiry: Expiry time in seconds (default: 300)
            
        Returns:
            bool: Success status
        """
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            expiry = expiry or CACHE_EXPIRY['default']
            serialized = json.dumps(value, default=str)
            self.redis_client.setex(key, expiry, serialized)
            logger.debug(f"Cache SET: {key} (expiry: {expiry}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False
    
    def delete(self, key):
        """
        Delete value from cache
        
        Args:
            key: Cache key
            
        Returns:
            bool: Success status
        """
        if not self.enabled or not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False
    
    def delete_pattern(self, pattern):
        """
        Delete all keys matching pattern
        
        Args:
            pattern: Key pattern (e.g., 'ppa_v2:job_listings:*')
            
        Returns:
            int: Number of keys deleted
        """
        if not self.enabled or not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Cache DELETE PATTERN: {pattern} ({deleted} keys)")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Cache delete pattern error: {str(e)}")
            return 0
    
    def invalidate_user_cache(self, user_id):
        """
        Invalidate all cache for a specific user
        
        Args:
            user_id: User ID
        """
        if not self.enabled:
            return
        
        patterns = [
            f"ppa_v2:*:user_{user_id}:*",
            f"ppa_v2:dashboard_stats:user_{user_id}",
            f"ppa_v2:user_profile:user_{user_id}"
        ]
        
        for pattern in patterns:
            self.delete_pattern(pattern)
    
    def invalidate_company_cache(self, company_id):
        """
        Invalidate all cache for a specific company
        
        Args:
            company_id: Company ID
        """
        if not self.enabled:
            return
        
        patterns = [
            f"ppa_v2:*:company_{company_id}:*",
            f"ppa_v2:job_listings:company_{company_id}",
            f"ppa_v2:company_search:*{company_id}*"
        ]
        
        for pattern in patterns:
            self.delete_pattern(pattern)
    
    def invalidate_all_job_cache(self):
        """Invalidate all job listings cache"""
        if self.enabled:
            self.delete_pattern("ppa_v2:job_listings:*")
    
    def invalidate_all_student_cache(self):
        """Invalidate all student search cache"""
        if self.enabled:
            self.delete_pattern("ppa_v2:student_search:*")
    
    def invalidate_all_company_cache(self):
        """Invalidate all company search cache"""
        if self.enabled:
            self.delete_pattern("ppa_v2:company_search:*")
    
    def invalidate_dashboard_cache(self):
        """Invalidate all dashboard stats cache"""
        if self.enabled:
            self.delete_pattern("ppa_v2:dashboard_stats:*")
    
    def get_stats(self):
        """
        Get cache statistics
        
        Returns:
            dict: Cache statistics
        """
        if not self.enabled or not self.redis_client:
            return {
                'enabled': False,
                'message': 'Redis cache is disabled'
            }
        
        try:
            info = self.redis_client.info('stats')
            keys_count = self.redis_client.dbsize()
            
            return {
                'enabled': True,
                'keys_count': keys_count,
                'hits': info.get('keyspace_hits', 0),
                'misses': info.get('keyspace_misses', 0),
                'hit_rate': self._calculate_hit_rate(info),
                'memory_used': self._get_memory_usage(),
                'connected_clients': info.get('connected_clients', 0)
            }
        except Exception as e:
            logger.error(f"Cache stats error: {str(e)}")
            return {
                'enabled': True,
                'error': str(e)
            }
    
    def _calculate_hit_rate(self, info):
        """Calculate cache hit rate percentage"""
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)
    
    def _get_memory_usage(self):
        """Get Redis memory usage in MB"""
        try:
            info = self.redis_client.info('memory')
            return round(info.get('used_memory', 0) / 1024 / 1024, 2)
        except:
            return 0


# Global cache service instance
cache_service = None


def init_cache_service(app):
    """
    Initialize cache service with Flask app
    
    Args:
        app: Flask application instance
        
    Returns:
        CacheService: Initialized cache service
    """
    global cache_service
    
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
    cache_service = CacheService(redis_url)
    
    logger.info(f"Cache Service Initialized: {'Enabled' if cache_service.enabled else 'Disabled'}")
    
    return cache_service

def cached(prefix, expiry=None, key_func=None):
    """
    Decorator for caching API responses
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip caching if cache is disabled
            if not cache_service or not cache_service.enabled:
                return f(*args, **kwargs)
            
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                from flask_login import current_user
                user_id = current_user.id if current_user.is_authenticated else 'anonymous'
                
                request_args = {
                    'args': args,
                    'kwargs': kwargs,
                    'request_args': dict(request.args) if request else {}
                }
                
                cache_key = cache_service._generate_key(prefix, user_id, **request_args)
            
            # Try to get from cache
            cached_value = cache_service.get(cache_key)
            if cached_value is not None:
                from flask import jsonify
                return jsonify(cached_value)
            
            # Execute function and get the Flask Response object
            result = f(*args, **kwargs)
            
            # Cache the result
            try:
                cache_expiry = expiry or CACHE_EXPIRY.get(prefix, CACHE_EXPIRY['default'])
                
                # FIX 2: Only cache the raw dictionary, NOT the Flask Response wrapper
                if hasattr(result, 'get_json') and result.get_json():
                    cache_service.set(cache_key, result.get_json(), expiry=cache_expiry)
            except Exception as e:
                logger.error(f"Cache set error in decorator: {str(e)}")
            
            return result
        
        return decorated_function
    return decorator

def invalidate_cache(pattern):
    """
    Decorator for invalidating cache after data modification
    
    Args:
        pattern: Cache key pattern to invalidate
        
    Returns:
        Decorated function
        
    Example:
        @invalidate_cache('ppa_v2:job_listings:*')
        def create_job_drive():
            # ... create drive ...
            return drive
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Execute function first
            result = f(*args, **kwargs)
            
            # Then invalidate cache
            if cache_service and cache_service.enabled:
                cache_service.delete_pattern(pattern)
            
            return result
        
        return decorated_function
    return decorator