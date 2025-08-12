"""
Database connection and operations for MongoDB
"""
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, TEXT
from bson import ObjectId
import redis
import json

from app.config import settings
from app.models.schemas import JobPosting, HashtagSearchRequest
from loguru import logger


class Database:
    """MongoDB database operations"""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database = None
        self.redis_client = None
    
    async def connect(self):
        """Connect to MongoDB and Redis"""
        try:
            # MongoDB connection
            self.client = AsyncIOMotorClient(settings.mongodb_url)
            self.database = self.client[settings.mongodb_db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Create indexes
            await self._create_indexes()
            
            # Redis connection
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
            
        except Exception as e:
            logger.error(f"Failed to connect to databases: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from databases"""
        if self.client:
            self.client.close()
        if self.redis_client:
            self.redis_client.close()
        logger.info("Disconnected from databases")
    
    async def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Job postings collection indexes
            jobs_collection = self.database.job_postings
            await jobs_collection.create_index([("hashtags", ASCENDING)])
            await jobs_collection.create_index([("source", ASCENDING)])
            await jobs_collection.create_index([("posted_date", DESCENDING)])
            await jobs_collection.create_index([("scraped_at", DESCENDING)])
            await jobs_collection.create_index([("location", ASCENDING)])
            await jobs_collection.create_index([("is_active", ASCENDING)])
            
            # Text search index
            await jobs_collection.create_index([
                ("title", TEXT),
                ("description", TEXT),
                ("company.name", TEXT)
            ])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")
    
    async def save_job_posting(self, job: JobPosting) -> str:
        """Save a job posting to the database"""
        try:
            job_dict = job.dict(by_alias=True, exclude={"id"})
            result = await self.database.job_postings.insert_one(job_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to save job posting: {e}")
            raise
    
    async def search_jobs(
        self,
        hashtags: List[str],
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Search job postings based on hashtags"""
        try:
            # Build query
            query = {
                "is_active": True,
                "hashtags": {"$in": [tag.lower() for tag in hashtags]}
            }
            
            # Count total results
            total_count = await self.database.job_postings.count_documents(query)
            
            # Execute search with pagination
            cursor = self.database.job_postings.find(query).sort("posted_date", DESCENDING)
            jobs_cursor = cursor.skip(offset).limit(limit)
            jobs = await jobs_cursor.to_list(length=limit)
            
            # Convert ObjectId to string
            for job in jobs:
                job["_id"] = str(job["_id"])
            
            return {
                "jobs": jobs,
                "total_count": total_count,
                "has_more": offset + len(jobs) < total_count
            }
            
        except Exception as e:
            logger.error(f"Failed to search jobs: {e}")
            raise


# Global database instance
db = Database()
