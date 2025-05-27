# Super Secret Code - Module 1

An interactive early literacy platform for children. This repo contains the frontend and backend code for Module 1: introducing letters, phonological awareness, sight words, vocabulary, and story reading.

---

## 📁 Folder Structure
```
super-secret-code/
├── backend/               # Express API, PostgreSQL schema, routes
│   ├── routes/            # API endpoints
│   ├── tests/             # Vitest + Supertest API tests
│   └── vitest.config.ts
├── frontend/              # Vite + React frontend app
│   ├── components/        # UI and learning components
│   ├── tests/             # React Testing Library
│   └── vitest.config.ts
├── public/                # Assets: audio, images, pdfs
├── mock/                  # Mock JSON data for dev
└── README.md
```

---

## 🚀 Deployment Instructions

### Frontend (Vercel/Netlify)
1. Link `super-secret-code/frontend` folder to project
2. Set env var: `VITE_API_BASE_URL=https://your-api-url`
3. Host assets in `public/`

### Backend (Railway)
1. Link `super-secret-code/backend` folder
2. Add env: `DATABASE_URL`, `PORT`
3. Auto-deploy on commit

---

## 🧪 Run Tests

### Backend:
```bash
cd super-secret-code/backend
npx vitest run
```

### Frontend:
```bash
cd super-secret-code/frontend
npx vitest run
```

---

## ✅ Module 1 Features Completed
- Onboarding & Avatar builder
- Mission map with block tiles
- All mission types (sound, vocab, story, etc.)
- Audio integration
- Badge & progress tracking
- Story reader + Library
- Printable worksheets
- Parent dashboard

---

## 📦 Next Steps (Module 2)
- Add new letter blocks (e.g., Block 2 letters)
- Adaptive difficulty / branching paths
- Progress analytics for parents/teachers
- Multiplayer profiles on same device
- Game & mini-mission expansion

---

For questions, contact: [ProductPod 🧠]
