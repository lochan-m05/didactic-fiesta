# Job Discovery Platform

A comprehensive AI-powered job discovery platform that scrapes job postings from multiple sources, analyzes them using NLP, and provides advanced search and filtering capabilities.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

### Installation

1. **Clone and setup**
```bash
git clone <your-repo-url>
cd job-discovery-platform
```

2. **Start with Docker**
```bash
cd docker
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Task Monitor: http://localhost:5555

## 🏗️ Architecture

```
Frontend (React) ↔ API (FastAPI) ↔ Database (MongoDB)
                      ↓
               Celery Workers ↔ Redis ↔ Web Scrapers
```

## 📋 Features

### Core Features
- **Hashtag-based Job Search** - Search using `#bca`, `#fresher`, `#python`
- **Multi-source Scraping** - LinkedIn, Naukri, Indeed, Glassdoor
- **Real-time Processing** - Async scraping with status updates
- **AI/NLP Analysis** - Sentiment analysis, skill extraction, job categorization
- **Contact Extraction** - Extract recruiter emails, phones, LinkedIn profiles
- **Advanced Filters** - Time, location, experience, salary filters
- **Export Data** - CSV, Excel, JSON export options

### Technical Features
- **Anti-bot Protection** - Proxy rotation, user-agent rotation
- **Scalable Architecture** - Microservices with Docker
- **Real-time Updates** - WebSocket support
- **Comprehensive API** - RESTful API with OpenAPI docs
- **Monitoring Stack** - Prometheus + Grafana

## 🔧 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

## 📚 API Usage Examples

### Search Jobs by Hashtags
```bash
curl -X POST "http://localhost:8000/api/jobs/search/hashtags" \
     -H "Content-Type: application/json" \
     -d '{"hashtags": ["bca", "fresher", "python"]}'
```

### Start Real-time Scraping
```bash
curl -X POST "http://localhost:8000/api/scraping/start" \
     -H "Content-Type: application/json" \
     -d '{"hashtags": ["react", "javascript"]}'
```

### Extract Contact Information
```bash
curl -X POST "http://localhost:8000/api/contacts/extract" \
     -H "Content-Type: application/json" \
     -d '{"job_urls": ["https://linkedin.com/jobs/view/123"]}'
```

## 🛠️ Tech Stack

**Backend:** FastAPI, MongoDB, Redis, Celery, Selenium, spaCy, NLTK
**Frontend:** React 18, Material-UI, React Query, Chart.js
**DevOps:** Docker, Nginx, Prometheus, Grafana

## 📁 Project Structure

```
job-discovery-platform/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── models/    # Database models
│   │   ├── scrapers/  # Web scrapers
│   │   ├── nlp/       # NLP processing
│   │   ├── api/       # API routes
│   │   └── tasks/     # Celery tasks
├── frontend/          # React frontend
├── docker/           # Docker configuration
└── config/           # Configuration files
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.
