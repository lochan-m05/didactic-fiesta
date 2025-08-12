"""
Pydantic models for the Job Discovery Platform
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class JobSource(str, Enum):
    """Enum for job sources"""
    LINKEDIN = "linkedin"
    NAUKRI = "naukri" 
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    FRESHERS_LIVE = "freshers_live"
    TWITTER = "twitter"


class TimeFilter(str, Enum):
    """Enum for time filters"""
    LAST_24H = "24h"
    LAST_3D = "3d"
    LAST_7D = "7d"
    LAST_14D = "14d"
    LAST_30D = "30d"


class ExperienceLevel(str, Enum):
    """Enum for experience levels"""
    FRESHER = "fresher"
    ENTRY_LEVEL = "entry_level"
    MID_LEVEL = "mid_level"
    SENIOR_LEVEL = "senior_level"
    EXECUTIVE = "executive"


class JobType(str, Enum):
    """Enum for job types"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"


class ContactInfo(BaseModel):
    """Model for contact information"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_profile: Optional[str] = None
    twitter_handle: Optional[str] = None
    whatsapp_available: bool = False


class CompanyInfo(BaseModel):
    """Model for company information"""
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None


class JobPosting(BaseModel):
    """Model for job posting"""
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    company: CompanyInfo
    location: str
    job_type: JobType = JobType.FULL_TIME
    experience_level: ExperienceLevel = ExperienceLevel.ENTRY_LEVEL
    skills_required: List[str] = []
    posted_date: datetime = Field(default_factory=datetime.now)
    job_url: str
    source: JobSource
    contact_info: Optional[ContactInfo] = None
    hashtags: List[str] = []
    scraped_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


class HashtagSearchRequest(BaseModel):
    """Model for hashtag-based search"""
    hashtags: List[str] = Field(..., min_items=1, max_items=10)


class APIResponse(BaseModel):
    """Generic API response model"""
    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
