**Super Secret Code - Module 1 Technical Specification**

---

### 📊 Data Models

#### 1. `User`
```json
{
  "id": "uuid",
  "email": "string",
  "passwordHash": "string",
  "subscriptionStatus": "free_trial | active | expired",
  "createdAt": "datetime"
}
```

#### 2. `ChildProfile`
```json
{
  "id": "uuid",
  "userId": "User.id",
  "nickname": "string",
  "languagePreference": "english | french | bilingual",
  "presentationLanguage": "english | french",
  "avatar": {
    "letter": "char",
    "color": "string",
    "face": "string",
    "accessory": "string",
    "transport": "string"
  },
  "createdAt": "datetime"
}
```

#### 3. `LessonBlock`
```json
{
  "id": "uuid",
  "blockNumber": "int",
  "language": "english | french",
  "letterSet": ["a", "e", "m", "s", "t"],
  "storyId": "Story.id"
}
```

#### 4. `Mission`
```json
{
  "id": "uuid",
  "lessonBlockId": "LessonBlock.id",
  "title": "string",
  "type": "phoneme | blend | vocab | story | game",
  "content": "json",
  "badgeId": "Badge.id"
}
```

#### 5. `Badge`
```json
{
  "id": "uuid",
  "title": "string",
  "icon": "string",
  "description": "string"
}
```

#### 6. `Story`
```json
{
  "id": "uuid",
  "title": "string",
  "language": "english | french",
  "pages": ["text or image links"],
  "sightWords": ["a", "the"]
}
```

#### 7. `Progress`
```json
{
  "id": "uuid",
  "childProfileId": "ChildProfile.id",
  "missionId": "Mission.id",
  "completed": "boolean",
  "badgeEarned": "boolean",
  "dateCompleted": "datetime"
}
```

---

### 🌐 API Design: Key Routes

#### 🧠 Progress Tracking: POST
```http
POST /progress
Content-Type: application/json
```

**Request body:**
```json
{
  "childProfileId": "uuid",
  "missionId": "uuid",
  "completed": true,
  "badgeEarned": true
}
```

**Response:**
```json
{
  "message": "Progress recorded",
  "badge": {
    "title": "Explorer A",
    "icon": "badge-a.png"
  }
}
```

This route allows frontend components to submit mission completion and unlock badges.

#### 🔐 Auth
```
POST /auth/signup          → create parent account
POST /auth/login           → authenticate parent
POST /auth/otp-login       → one-time passcode login (optional)
```

#### 👨‍👩‍👧 Parent & Child Management
```
GET    /users/me                      → fetch parent profile
POST   /profiles                      → create child profile
GET    /profiles                      → list all child profiles
PATCH  /profiles/:id                  → update a child profile
DELETE /profiles/:id                  → delete a child profile
```

#### 📚 Lessons & Missions
```
GET  /blocks                          → list all lesson blocks
GET  /blocks/:id                      → get one lesson block
GET  /missions?blockId=XYZ           → list missions in block
GET  /missions/:id                    → get a single mission
```

#### 🧠 Progress Tracking
```
GET   /progress?profileId=XYZ        → fetch all progress for child
POST  /progress                      → submit mission completion
```

#### 🏆 Badges & Rewards
```
GET  /badges                          → list available badges
GET  /backpack?profileId=XYZ         → child’s earned badges
```

#### 📖 Stories & Library
```
GET  /stories                         → list all stories
GET  /stories/:id                     → get one story
GET  /library?profileId=XYZ          → list unlocked stories
```

---

### 🏠 Backend Architecture

| Layer | Description |
|-------|-------------|
| **Frontend** | React web app (supports EN/FR toggle, responsive design) |
| **API Gateway** | RESTful Express.js API |
| **Business Logic** | Handles game logic, mission validation, progress unlocks |
| **Database** | PostgreSQL (or Firebase/Firestore if realtime sync is needed) |
| **Auth** | Auth0, Supabase Auth, or Firebase Auth for email/password + OTP |
| **Storage** | S3 or Firebase Storage for audio/image assets |
| **Payments** | Stripe integration for subscriptions |
| **PDF Generator** | Server-side rendering for printable worksheets |