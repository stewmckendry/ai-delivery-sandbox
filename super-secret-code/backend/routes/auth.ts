import { Router } from 'express';

const router = Router();

// POST /auth/signup
router.post('/signup', (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ error: 'Missing email or password' });

  // Mock user creation
  const mockUser = {
    id: 'user-123',
    email,
    subscriptionStatus: 'free_trial',
  };
  res.status(201).json({ message: 'User created', user: mockUser });
});

// POST /auth/login
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  if (email === 'test@example.com' && password === 'password') {
    return res.json({ message: 'Login successful', token: 'mock-token' });
  }
  res.status(401).json({ error: 'Invalid credentials' });
});

export default router;