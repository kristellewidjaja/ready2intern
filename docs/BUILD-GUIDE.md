# Build Guide: Ready2Intern POC
**Foundation Setup for Vertical Slices Development**

---

## Overview

This guide sets up the complete foundation (frontend + backend + integration) to catch integration issues early. Follow this before starting any feature slices.

**Goal:** Working full-stack application with verified communication between frontend and backend.

**Time Estimate:** 2-3 hours

---

## Prerequisites

### Required Tools
- **Node.js:** v18+ (for frontend)
- **Python:** 3.11+ (for backend)
- **uv:** Latest version (Python package manager)
- **Git:** For version control

### Verify Installation
```bash
node --version    # Should show v18+
python --version  # Should show 3.11+
uv --version      # Should show latest
```

---

## Part 1: Project Structure

### Create Root Directory
```bash
mkdir ready2intern-poc
cd ready2intern-poc
```

### Initialize Git
```bash
git init
```

### Create Directory Structure
```bash
mkdir -p frontend
mkdir -p backend
mkdir -p data/resumes
mkdir -p data/company-tenets
mkdir -p data/sessions
```

### Create Root .gitignore
```bash
cat > .gitignore << 'EOF'
# Data directories
data/resumes/*
data/sessions/*
!data/resumes/.gitkeep
!data/sessions/.gitkeep

# Environment files
.env
.env.local

# OS files
.DS_Store
Thumbs.db
EOF
```

### Create Data Directory Placeholders
```bash
touch data/resumes/.gitkeep
touch data/sessions/.gitkeep
```

---

## Part 2: Backend Setup (FastAPI)

### Navigate to Backend
```bash
cd backend
```

### Initialize Python Project with uv
```bash
uv init
```

### Create pyproject.toml
```bash
cat > pyproject.toml << 'EOF'
[project]
name = "ready2intern-backend"
version = "0.1.0"
description = "Backend API for Ready2Intern POC"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "python-multipart>=0.0.6",
    "anthropic>=0.18.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF
```

### Install Dependencies
```bash
uv pip install -e .
```

### Create Backend Directory Structure
```bash
mkdir -p app/api/routes
mkdir -p app/core
mkdir -p app/models
mkdir -p app/services
touch app/__init__.py
touch app/api/__init__.py
touch app/api/routes/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
```

### Create Environment File
```bash
cat > .env << 'EOF'
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here

# File Storage
DATA_DIR=../data
MAX_FILE_SIZE_MB=5
EOF
```

### Create Configuration (app/core/config.py)
```bash
cat > app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # CORS
    cors_origins: List[str] = ["http://localhost:5173"]
    
    # Anthropic API
    anthropic_api_key: str
    
    # File Storage
    data_dir: str = "../data"
    max_file_size_mb: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
EOF
```

### Create Health Check Route (app/api/routes/health.py)
```bash
cat > app/api/routes/health.py << 'EOF'
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ready2intern-backend",
        "version": "0.1.0"
    }
EOF
```

### Create Main Application (app/main.py)
```bash
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import health

# Create FastAPI application
app = FastAPI(
    title="Ready2Intern API",
    description="Backend API for Ready2Intern POC",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Ready2Intern API",
        "docs": "/docs",
        "health": "/api/health"
    }
EOF
```

### Create Run Script
```bash
cat > run.py << 'EOF'
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
EOF
```

### Create Backend .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.uv/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
EOF
```

---

## Part 3: Frontend Setup (React + TypeScript + Vite)

### Navigate to Frontend
```bash
cd ../frontend
```

### Initialize Vite Project
```bash
npm create vite@latest . -- --template react-ts
```

### Install Dependencies
```bash
npm install
```

### Install Additional Dependencies
```bash
npm install -D tailwindcss postcss autoprefixer
npm install axios zustand lucide-react
```

### Initialize Tailwind CSS
```bash
npx tailwindcss init -p
```

### Configure Tailwind (tailwind.config.js)
```bash
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          'deep-ocean': '#031926',
          'teal': '#468189',
          'sage': '#77ACA2',
          'mint': '#9DBEBB',
          'cream': '#F4E9CD',
        },
      },
    },
  },
  plugins: [],
}
EOF
```

### Update CSS (src/index.css)
```bash
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  /* Brand Colors */
  --color-primary: #468189;
  --color-primary-dark: #031926;
  --color-secondary: #77ACA2;
  --color-accent: #9DBEBB;
  --color-light: #F4E9CD;
  
  /* Light Mode */
  --bg-primary: #F4E9CD;
  --bg-surface: #FFFFFF;
  --text-primary: #031926;
  --text-secondary: #468189;
  --border-color: #9DBEBB;
}

.dark {
  /* Dark Mode */
  --bg-primary: #031926;
  --bg-surface: rgba(70, 129, 137, 0.2);
  --text-primary: #F4E9CD;
  --text-secondary: #9DBEBB;
  --border-color: #77ACA2;
}

body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: background-color 0.3s ease, color 0.3s ease;
}
EOF
```

### Create API Service (src/services/api.ts)
```bash
mkdir -p src/services
cat > src/services/api.ts << 'EOF'
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};
EOF
```

### Create Environment File
```bash
cat > .env << 'EOF'
VITE_API_URL=http://localhost:8000
EOF
```

### Update App Component (src/App.tsx)
```bash
cat > src/App.tsx << 'EOF'
import { useState, useEffect } from 'react';
import { checkHealth } from './services/api';

function App() {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkHealth();
        setHealthStatus(data);
        setError(null);
      } catch (err) {
        setError('Failed to connect to backend');
        console.error('Health check failed:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHealth();
  }, []);

  return (
    <div className="min-h-screen bg-brand-cream dark:bg-brand-deep-ocean">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-brand-deep-ocean dark:text-brand-cream mb-2">
            Ready2Intern
          </h1>
          <p className="text-brand-teal dark:text-brand-mint">
            AI Internship Readiness Platform
          </p>
        </header>

        <main className="max-w-2xl mx-auto">
          <div className="bg-white dark:bg-brand-teal/20 rounded-lg shadow-lg p-6 border border-brand-mint dark:border-brand-sage">
            <h2 className="text-2xl font-semibold mb-4 text-brand-deep-ocean dark:text-brand-cream">
              System Status
            </h2>
            
            {loading && (
              <div className="text-brand-teal dark:text-brand-mint">
                Checking backend connection...
              </div>
            )}
            
            {error && (
              <div className="bg-red-100 dark:bg-red-900/30 border border-red-400 text-red-700 dark:text-red-300 px-4 py-3 rounded">
                <strong>Error:</strong> {error}
              </div>
            )}
            
            {healthStatus && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-brand-deep-ocean dark:text-brand-cream">
                    Backend Status: <strong>{healthStatus.status}</strong>
                  </span>
                </div>
                <div className="text-sm text-brand-teal dark:text-brand-mint">
                  Service: {healthStatus.service}
                </div>
                <div className="text-sm text-brand-teal dark:text-brand-mint">
                  Version: {healthStatus.version}
                </div>
                <div className="text-sm text-brand-teal dark:text-brand-mint">
                  Timestamp: {new Date(healthStatus.timestamp).toLocaleString()}
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
EOF
```

### Update Main Entry (src/main.tsx)
```bash
cat > src/main.tsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF
```

### Create Frontend .gitignore
```bash
cat > .gitignore << 'EOF'
# Dependencies
node_modules/

# Build
dist/
dist-ssr/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# Logs
*.log

# OS
.DS_Store
EOF
```

---

## Part 4: Integration Verification

### Terminal 1: Start Backend
```bash
cd backend
python run.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Verification Checklist

#### 1. Backend Health Check (Manual)
Open browser: `http://localhost:8000/api/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T...",
  "service": "ready2intern-backend",
  "version": "0.1.0"
}
```

#### 2. Backend API Docs
Open browser: `http://localhost:8000/docs`

**Expected:** Interactive Swagger UI with health endpoint

#### 3. Frontend Application
Open browser: `http://localhost:5173`

**Expected:**
- Page loads successfully
- "Ready2Intern" header displays
- "System Status" card shows
- Green dot with "Backend Status: healthy"
- Backend service info displays
- No console errors

#### 4. Frontend-Backend Communication
Check browser console (F12 → Console)

**Expected:**
- No CORS errors
- Successful API call to `/api/health`
- Health data logged

#### 5. CORS Verification
In browser console, run:
```javascript
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(console.log)
```

**Expected:** Health data logged (no CORS error)

---

## Part 5: Root Documentation

### Create Project Tracking Files

#### PROJECT.md (Project State Tracking)
```bash
cd ..  # Back to root
cp PROJECT.md ready2intern-poc/PROJECT.md
```

#### ISSUES.md (Issue Tracking)
```bash
cp ISSUES.md ready2intern-poc/ISSUES.md
```

> **Note:** These files track project progress and issues. Update them after each feature slice.
> See AGENT-WORKFLOW.md for how to use these files effectively.

### Create Root README.md
```bash
cat > README.md << 'EOF'
# Ready2Intern POC

AI Internship Readiness Platform for college students pursuing tech internships.

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- uv (Python package manager)

### Setup

1. **Clone and Install**
   ```bash
   git clone <repository-url>
   cd ready2intern-poc
   ```

2. **Backend Setup**
   ```bash
   cd backend
   uv pip install -e .
   cp .env.example .env  # Add your Anthropic API key
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```
Backend runs on: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

### Verify Integration

1. Open http://localhost:5173
2. Check "System Status" shows backend as healthy
3. Open http://localhost:8000/docs for API documentation

## Project Structure

```
ready2intern-poc/
├── frontend/           # React + TypeScript + Vite
│   ├── src/
│   │   ├── services/  # API client
│   │   ├── App.tsx    # Main component
│   │   └── main.tsx   # Entry point
│   └── package.json
├── backend/            # FastAPI + Python
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Configuration
│   │   ├── models/    # Data models
│   │   └── services/  # Business logic
│   └── pyproject.toml
└── data/               # File storage
    ├── resumes/        # Uploaded resumes
    ├── company-tenets/ # Company values
    └── sessions/       # Analysis results
```

## Development Workflow

This project uses **vertical slices** - each feature is built end-to-end:
1. Frontend UI component
2. Backend API endpoint
3. Integration and testing
4. Move to next feature

See `BUILD-GUIDE.md` for detailed setup instructions.
See `Ready2Intern-Implementation-Plan.md` for feature development order.
See `AGENT-WORKFLOW.md` for how to work with coding agents.

## Project Tracking

- **PROJECT.md** - Current project state, completed features, lessons learned
- **ISSUES.md** - Known issues, technical debt, enhancement ideas

Update these files after completing each feature slice.

## Technology Stack

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)
- Zustand (state management)

**Backend:**
- FastAPI (Python web framework)
- uv (package manager)
- Anthropic Claude API (LLM)
- File system storage (POC)

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Verify uv installed: `uv --version`
- Check .env file exists with ANTHROPIC_API_KEY

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### CORS errors
- Verify backend is running on port 8000
- Check backend .env has correct CORS_ORIGINS
- Clear browser cache

### Frontend can't connect to backend
- Verify backend is running: http://localhost:8000/api/health
- Check frontend .env has correct VITE_API_URL
- Check browser console for errors
EOF
```

---

## Success Criteria

### ✅ Backend Checklist
- [ ] Backend starts without errors
- [ ] Health endpoint responds at `/api/health`
- [ ] API docs accessible at `/docs`
- [ ] CORS configured correctly
- [ ] Environment variables loaded

### ✅ Frontend Checklist
- [ ] Frontend starts without errors
- [ ] Page renders at `localhost:5173`
- [ ] Tailwind CSS styles applied
- [ ] Custom theme colors working
- [ ] No console errors

### ✅ Integration Checklist
- [ ] Frontend successfully calls backend health endpoint
- [ ] Health status displays in UI
- [ ] No CORS errors in console
- [ ] Both services run simultaneously
- [ ] Data flows from backend to frontend

---

## Next Steps

Once verification is complete:

1. **Commit the foundation:**
   ```bash
   git add .
   git commit -m "feat: initial project scaffold with health check"
   ```

2. **Start Feature Slice 2:** Resume Upload
   - Follow `Ready2Intern-Implementation-Plan.md`
   - Build frontend component
   - Build backend endpoint
   - Test integration
   - Commit when complete

3. **Repeat for each feature slice:**
   - Each slice is independently testable
   - Integration verified at each step
   - No "big bang" integration at the end

---

## Feature Development Workflow

### How to Build a Feature Slice (Example: Resume Upload)

#### Step 1: Plan the Slice
Read the feature slice from Implementation Plan:
- Understand the goal
- Review frontend tasks
- Review backend tasks
- Note acceptance criteria

#### Step 2: Backend First (API Contract)
1. **Create the endpoint file:**
   ```bash
   cd backend/app/api/routes
   touch upload.py
   ```

2. **Define the API contract** (request/response models):
   ```bash
   cd backend/app/models
   touch upload.py
   ```

3. **Implement the endpoint** with stub logic
4. **Register the router** in `app/main.py`
5. **Test in Swagger UI** (`/docs`) - verify request/response structure

#### Step 3: Frontend (UI Component)
1. **Create the component:**
   ```bash
   cd frontend/src/components
   mkdir -p dashboard
   touch dashboard/FileDropzone.tsx
   ```

2. **Build the UI** (no API calls yet)
3. **Test visually** - verify it renders correctly

#### Step 4: Frontend (API Integration)
1. **Add API function** to `src/services/api.ts`:
   ```typescript
   export const uploadResume = async (file: File) => {
     const formData = new FormData();
     formData.append('file', file);
     const response = await api.post('/api/upload', formData, {
       headers: { 'Content-Type': 'multipart/form-data' }
     });
     return response.data;
   };
   ```

2. **Connect component to API**
3. **Handle loading/error states**

#### Step 5: Backend (Full Implementation)
1. **Implement business logic** (file validation, storage, etc.)
2. **Add error handling**
3. **Test edge cases** in Swagger UI

#### Step 6: End-to-End Testing
1. **Test happy path:** Upload valid file → Success
2. **Test error cases:** Invalid file → Error message
3. **Test edge cases:** Large file, wrong format, etc.
4. **Verify file system:** Check `data/resumes/` for saved file

#### Step 7: Commit
```bash
git add .
git commit -m "feat: add resume upload feature (slice 2)"
```

### File Organization Patterns

#### Backend Structure
```
backend/app/
├── api/routes/
│   ├── health.py          # Health check
│   ├── upload.py          # File upload
│   ├── companies.py       # Company list
│   └── analyze.py         # Analysis endpoint
├── models/
│   ├── upload.py          # Upload request/response models
│   ├── company.py         # Company models
│   └── analysis.py        # Analysis models
├── services/
│   ├── file_service.py    # File operations
│   ├── llm_service.py     # Anthropic API calls
│   └── session_service.py # Session management
└── core/
    ├── config.py          # Configuration
    └── dependencies.py    # Shared dependencies
```

#### Frontend Structure
```
frontend/src/
├── components/
│   ├── common/            # Reusable components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Spinner.tsx
│   ├── dashboard/         # Dashboard-specific
│   │   ├── FileDropzone.tsx
│   │   ├── CompanySelector.tsx
│   │   └── JobDescriptionInput.tsx
│   ├── results/           # Results display
│   │   ├── ScoreCard.tsx
│   │   ├── StrengthsSection.tsx
│   │   └── GapsSection.tsx
│   └── layout/            # Layout components
│       ├── Header.tsx
│       └── Footer.tsx
├── services/
│   └── api.ts             # API client
├── hooks/
│   ├── useTheme.ts        # Theme management
│   └── useAnalysis.ts     # Analysis state
├── types/
│   └── index.ts           # TypeScript types
└── utils/
    └── validation.ts      # Validation helpers
```

### API Development Pattern

#### 1. Define Models First (backend/app/models/upload.py)
```python
from pydantic import BaseModel

class UploadResponse(BaseModel):
    session_id: str
    filename: str
    size: int
    message: str
```

#### 2. Create Route (backend/app/api/routes/upload.py)
```python
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    # Implementation here
    pass
```

#### 3. Register in Main (backend/app/main.py)
```python
from app.api.routes import health, upload

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
```

#### 4. Test in Swagger
- Go to `http://localhost:8000/docs`
- Find `/api/upload` endpoint
- Click "Try it out"
- Upload a file
- Verify response

### Component Development Pattern

#### 1. Create Component File
```typescript
// frontend/src/components/dashboard/FileDropzone.tsx
import { useState } from 'react';

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
}

export function FileDropzone({ onFileSelect }: FileDropzoneProps) {
  // Implementation
  return <div>Component UI</div>;
}
```

#### 2. Add to Parent Component
```typescript
// frontend/src/App.tsx
import { FileDropzone } from './components/dashboard/FileDropzone';

function App() {
  const handleFileSelect = (file: File) => {
    console.log('File selected:', file);
  };

  return (
    <div>
      <FileDropzone onFileSelect={handleFileSelect} />
    </div>
  );
}
```

#### 3. Connect to API
```typescript
import { uploadResume } from '../../services/api';

const handleFileSelect = async (file: File) => {
  try {
    const result = await uploadResume(file);
    console.log('Upload success:', result);
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

### State Management Pattern

#### Simple State (useState)
For component-local state:
```typescript
const [file, setFile] = useState<File | null>(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

#### Global State (Zustand)
For app-wide state, create store:
```typescript
// frontend/src/store/analysisStore.ts
import { create } from 'zustand';

interface AnalysisState {
  sessionId: string | null;
  company: string | null;
  jobDescription: string;
  setSessionId: (id: string) => void;
  setCompany: (company: string) => void;
  setJobDescription: (desc: string) => void;
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  sessionId: null,
  company: null,
  jobDescription: '',
  setSessionId: (id) => set({ sessionId: id }),
  setCompany: (company) => set({ company }),
  setJobDescription: (desc) => set({ jobDescription: desc }),
}));
```

Use in components:
```typescript
import { useAnalysisStore } from '../store/analysisStore';

function MyComponent() {
  const { sessionId, setSessionId } = useAnalysisStore();
  // Use state
}
```

### Error Handling Pattern

#### Backend
```python
from fastapi import HTTPException

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX allowed."
        )
    
    # Validate file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB."
        )
    
    # Process file
    try:
        # Save file logic
        pass
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )
```

#### Frontend
```typescript
const handleUpload = async (file: File) => {
  setLoading(true);
  setError(null);
  
  try {
    const result = await uploadResume(file);
    setSessionId(result.session_id);
    // Show success message
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || 'Upload failed';
    setError(errorMessage);
    // Show error to user
  } finally {
    setLoading(false);
  }
};
```

### Testing Each Slice

#### Backend Testing (Manual via Swagger)
1. Go to `http://localhost:8000/docs`
2. Test endpoint with valid data → Should succeed
3. Test with invalid data → Should return error
4. Check response matches model
5. Verify side effects (file saved, etc.)

#### Frontend Testing (Manual in Browser)
1. Open `http://localhost:5173`
2. Test UI interaction → Should work
3. Test API call → Check Network tab (F12)
4. Test error handling → Trigger error, verify message
5. Test loading state → Verify spinner shows

#### Integration Testing
1. Complete user flow from UI to backend
2. Verify data persists (check file system)
3. Verify state updates correctly
4. Test error recovery

### Common Patterns Reference

#### File Upload (Multipart Form Data)
**Backend:**
```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    # Save to file system
```

**Frontend:**
```typescript
const formData = new FormData();
formData.append('file', file);
await api.post('/api/upload', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

#### JSON Request/Response
**Backend:**
```python
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    session_id: str
    company: str
    job_description: str

@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    return {"status": "processing"}
```

**Frontend:**
```typescript
await api.post('/api/analyze', {
  session_id: 'abc123',
  company: 'Amazon',
  job_description: 'Job text...'
});
```

#### Loading States
```typescript
const [loading, setLoading] = useState(false);

const handleAction = async () => {
  setLoading(true);
  try {
    await someApiCall();
  } finally {
    setLoading(false);
  }
};

return loading ? <Spinner /> : <Button onClick={handleAction} />;
```

---

## Quick Reference Commands

### Start Development
```bash
# Terminal 1 - Backend
cd backend && python run.py

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

### Create New Files
```bash
# Backend route
touch backend/app/api/routes/feature.py

# Backend model
touch backend/app/models/feature.py

# Frontend component
touch frontend/src/components/dashboard/Feature.tsx

# Frontend service
# Add function to frontend/src/services/api.ts
```

### Test Endpoints
```bash
# Via Swagger UI
open http://localhost:8000/docs

# Via curl
curl http://localhost:8000/api/health

# Via browser console
fetch('http://localhost:8000/api/health').then(r => r.json()).then(console.log)
```

### Check Logs
```bash
# Backend logs show in terminal running python run.py
# Frontend logs show in browser console (F12)
```

### Restart Services
```bash
# Backend auto-reloads (uvicorn reload mode)
# Frontend auto-reloads (Vite HMR)
# Manual restart: Ctrl+C then restart command
```

---

## Common Issues & Solutions

### Issue: Backend port already in use
**Solution:** Kill process on port 8000
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: Frontend port already in use
**Solution:** Kill process on port 5173
```bash
lsof -ti:5173 | xargs kill -9
```

### Issue: uv command not found
**Solution:** Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Issue: Module not found errors in backend
**Solution:** Reinstall dependencies
```bash
cd backend
uv pip install -e .
```

### Issue: Vite not found
**Solution:** Install frontend dependencies
```bash
cd frontend
npm install
```

---

## Development Tips

### Hot Reload
- **Backend:** Auto-reloads on file changes (uvicorn reload mode)
- **Frontend:** Auto-reloads on file changes (Vite HMR)

### Debugging
- **Backend:** Add `import pdb; pdb.set_trace()` for breakpoints
- **Frontend:** Use browser DevTools (F12)

### Testing Integration
After each feature slice, verify:
1. Frontend UI works
2. Backend API works (test in `/docs`)
3. Frontend → Backend communication works
4. Error handling works

### Code Organization
- Keep components small and focused
- One feature per file
- Test each slice before moving to next
- Commit working code frequently

---

**You now have a complete, verified foundation for vertical slices development. Integration is proven to work. Start building features with confidence!**
