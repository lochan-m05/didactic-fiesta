"""
Base scraper class with anti-bot protection and utility functions
"""
import asyncio
import random
import time
import re
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger

from app.config import settings
from app.models.schemas import JobPosting, JobSource, CompanyInfo, ContactInfo


class BaseScraper(ABC):
    """Base scraper class with common functionality"""
    
    def __init__(self, source: JobSource):
        self.source = source
        self.user_agent = UserAgent()
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
    
    async def initialize(self):
        """Initialize scraper resources"""
        connector = aiohttp.TCPConnector(limit=settings.max_concurrent_requests)
        timeout = aiohttp.ClientTimeout(total=settings.request_timeout)
        
        self.session = aiohttp.ClientSession(
            headers=self.get_random_headers(),
            connector=connector,
            timeout=timeout
        )
        
        logger.info(f"Initialized {self.source} scraper")
    
    async def cleanup(self):
        """Cleanup scraper resources"""
        if self.session:
            await self.session.close()
        logger.info(f"Cleaned up {self.source} scraper")
    
    def get_random_headers(self) -> Dict[str, str]:
        """Get random headers to mimic real browser requests"""
        return {
            'User-Agent': self.user_agent.random if settings.user_agent_rotation else self.user_agent.chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch page content with error handling"""
        try:
            await asyncio.sleep(random.uniform(
                settings.scraping_delay_min, 
                settings.scraping_delay_max
            ))
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    logger.debug(f"Fetched {url}")
                    return content
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str:
            return None
            
        date_str = date_str.strip().lower()
        now = datetime.now()
        
        # Common patterns
        if 'day' in date_str and 'ago' in date_str:
            days_match = re.search(r'(\d+)\s+days?\s+ago', date_str)
            if days_match:
                days = int(days_match.group(1))
                return now - timedelta(days=days)
        
        if 'hour' in date_str and 'ago' in date_str:
            hours_match = re.search(r'(\d+)\s+hours?\s+ago', date_str)
            if hours_match:
                hours = int(hours_match.group(1))
                return now - timedelta(hours=hours)
        
        if 'yesterday' in date_str:
            return now - timedelta(days=1)
        
        if 'today' in date_str:
            return now
        
        # Default to now if can't parse
        return now
    
    def extract_contact_info(self, text: str) -> Optional[ContactInfo]:
        """Extract contact information from text"""
        if not text:
            return None
            
        contact_info = ContactInfo()
        
        # Email regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info.email = emails[0]
        
        # Phone regex (Indian format)
        phone_patterns = [
            r'(\+91[-\s]?)?[6-9]\d{9}',
            r'(\+91[-\s]?)?[6-9]\d{4}[-\s]?\d{5}',
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                contact_info.phone = phones[0]
                break
        
        # LinkedIn profile
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_matches = re.findall(linkedin_pattern, text)
        if linkedin_matches:
            contact_info.linkedin_profile = f"https://{linkedin_matches[0]}"
        
        return contact_info if any([contact_info.email, contact_info.phone, contact_info.linkedin_profile]) else None
    
    @abstractmethod
    async def search_jobs(self, hashtags: List[str], **kwargs) -> List[JobPosting]:
        """Search for jobs based on hashtags"""
        pass
