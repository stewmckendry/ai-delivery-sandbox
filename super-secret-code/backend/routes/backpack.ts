import { Router } from 'express';

const router = Router();

const mockBackpack = {
  'profile-001': [
    { id: 'badge-001', title: 'Explorer A', icon: 'badge-a.png', description: 'Completed first phoneme mission' }
  ]
};

router.get('/', (req, res) => {
  const { profileId } = req.query;
  if (!profileId) return res.status(400).json({ error: 'Missing profileId' });
  const badges = mockBackpack[profileId as string] || [];
  res.json(badges);
});

export default router;