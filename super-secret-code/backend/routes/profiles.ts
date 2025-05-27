import { Router } from 'express';

const router = Router();

let mockProfiles: any[] = [];

// Create profile
router.post('/', (req, res) => {
  const profile = { id: `profile-${Date.now()}`, ...req.body };
  mockProfiles.push(profile);
  res.status(201).json({ message: 'Profile created', profile });
});

// List all profiles
router.get('/', (_req, res) => {
  res.json(mockProfiles);
});

// Update profile
router.patch('/:id', (req, res) => {
  const index = mockProfiles.findIndex(p => p.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Profile not found' });
  mockProfiles[index] = { ...mockProfiles[index], ...req.body };
  res.json({ message: 'Profile updated', profile: mockProfiles[index] });
});

// Delete profile
router.delete('/:id', (req, res) => {
  const index = mockProfiles.findIndex(p => p.id === req.params.id);
  if (index === -1) return res.status(404).json({ error: 'Profile not found' });
  const removed = mockProfiles.splice(index, 1);
  res.json({ message: 'Profile deleted', removed });
});

export default router;