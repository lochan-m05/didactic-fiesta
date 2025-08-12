"""
Configuration settings for the Job Discovery Platform
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Database Configuration
    mongodb_url: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    mongodb_db_name: str = Field(default="job_discovery", env="MONGODB_DB_NAME")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_cache_ttl: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # Celery Configuration
    celery_broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=1, env="API_WORKERS")
    debug: bool = Field(default=True, env="DEBUG")
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    
    # JWT Configuration
    jwt_secret_key: str = Field(default="your-jwt-secret-key", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=1440, env="JWT_EXPIRE_MINUTES")
    
    # Scraping Configuration
    scraping_delay_min: int = Field(default=1, env="SCRAPING_DELAY_MIN")
    scraping_delay_max: int = Field(default=5, env="SCRAPING_DELAY_MAX")
    max_concurrent_requests: int = Field(default=10, env="MAX_CONCURRENT_REQUESTS")
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    
    # Proxy Configuration
    proxy_enabled: bool = Field(default=False, env="PROXY_ENABLED")
    proxy_list: List[str] = Field(default_factory=list, env="PROXY_LIST")
    proxy_rotation_enabled: bool = Field(default=True, env="PROXY_ROTATION_ENABLED")
    
    # Anti-bot Configuration
    user_agent_rotation: bool = Field(default=True, env="USER_AGENT_ROTATION")
    headless_browser: bool = Field(default=True, env="HEADLESS_BROWSER")
    captcha_solver_api_key: Optional[str] = Field(default=None, env="CAPTCHA_SOLVER_API_KEY")
    
    # NLP Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    spacy_model: str = Field(default="en_core_web_sm", env="SPACY_MODEL")
    max_text_length: int = Field(default=5000, env="MAX_TEXT_LENGTH")
    
    # Email Configuration
    smtp_server: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", env="LOG_FILE")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=100, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_burst: int = Field(default=20, env="RATE_LIMIT_BURST")
    
    # Export Configuration
    max_export_records: int = Field(default=10000, env="MAX_EXPORT_RECORDS")
    export_cache_ttl: int = Field(default=300, env="EXPORT_CACHE_TTL")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Supported job boards and their configurations
JOB_BOARDS_CONFIG = {
    "linkedin": {
        "enabled": True,
        "base_url": "https://www.linkedin.com/jobs/search",
        "rate_limit": 60,  # requests per minute
        "requires_auth": True,
    },
    "naukri": {
        "enabled": True,
        "base_url": "https://www.naukri.com/jobs-search",
        "rate_limit": 120,
        "requires_auth": False,
    },
    "indeed": {
        "enabled": True,
        "base_url": "https://www.indeed.com/jobs",
        "rate_limit": 100,
        "requires_auth": False,
    },
    "glassdoor": {
        "enabled": True,
        "base_url": "https://www.glassdoor.com/Job/jobs.htm",
        "rate_limit": 50,
        "requires_auth": False,
    },
    "freshers_live": {
        "enabled": True,
        "base_url": "https://www.fresherslive.com/jobs",
        "rate_limit": 80,
        "requires_auth": False,
    },
    "twitter": {
        "enabled": True,
        "base_url": "https://twitter.com/search",
        "rate_limit": 300,  # Twitter API rate limit
        "requires_auth": True,
    },
}

# Time filter configurations
TIME_FILTERS = {
    "24h": {"hours": 24},
    "3d": {"days": 3},
    "7d": {"days": 7},
    "14d": {"days": 14},
    "30d": {"days": 30},
}

# Job categories and their keywords
JOB_CATEGORIES = {
    "software_development": [
        "python developer", "java developer", "javascript", "react", "node.js",
        "full stack", "frontend", "backend", "mobile app", "android", "ios"
    ],
    "data_science": [
        "data scientist", "machine learning", "ai", "data analyst", "big data",
        "python", "r programming", "sql", "tableau", "power bi"
    ],
    "digital_marketing": [
        "digital marketing", "seo", "social media", "content marketing",
        "google ads", "facebook ads", "email marketing"
    ],
    "sales": [
        "sales executive", "business development", "inside sales", "field sales",
        "account manager", "sales manager"
    ],
    "hr": [
        "human resources", "hr generalist", "recruiter", "talent acquisition",
        "hr business partner", "compensation"
    ],
    "finance": [
        "financial analyst", "accountant", "finance manager", "investment",
        "banking", "audit", "tax"
    ],
    "fresher": [
        "fresher", "entry level", "graduate trainee", "intern", "junior",
        "0-1 years", "campus placement"
    ]
}
