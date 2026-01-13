# Ready2Intern Frontend

React + TypeScript + Vite frontend for the Ready2Intern resume evaluation system.

## Setup

### Prerequisites
- Node.js 18+
- npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173

## Features

- ✨ Modern UI with Tailwind CSS
- 🌓 Dark/Light theme toggle
- 📱 Responsive design
- ⚡ Fast refresh with Vite
- 🔒 TypeScript for type safety

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/            # Page components
│   ├── contexts/         # React contexts (Theme, etc.)
│   ├── services/         # API client services
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── public/               # Static assets
└── index.html            # HTML template
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Router** - Routing (ready for future use)
