import { Router } from 'express';

const router = Router();

let mockProgress: any[] = [];

// Submit progress
router.post('/', (req, res) => {
  const progress = { id: `progress-${Date.now()}`, dateCompleted: new Date(), ...req.body };
  mockProgress.push(progress);
  res.status(201).json({ message: 'Progress recorded', progress });
});

// Fetch progress by profile ID
router.get('/', (req, res) => {
  const { profileId } = req.query;
  if (!profileId) return res.status(400).json({ error: 'Missing profileId' });

  const results = mockProgress.filter(p => p.childProfileId === profileId);
  res.json(results);
});

export default router;