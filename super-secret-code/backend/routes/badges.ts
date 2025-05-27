import { Router } from 'express';

const router = Router();

const mockBadges = [
  { id: 'badge-001', title: 'Explorer A', icon: 'badge-a.png', description: 'Completed first phoneme mission' },
  { id: 'badge-002', title: 'Vocab Victor', icon: 'badge-vocab.png', description: 'Completed a vocabulary mission' }
];

router.get('/', (_req, res) => {
  res.json(mockBadges);
});

export default router;