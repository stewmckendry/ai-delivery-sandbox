import { Router } from 'express';

const router = Router();

const mockLibrary = {
  'profile-001': [
    { id: 'story-001', title: 'A Bat', coverImage: '/images/a-bat-cover.png' },
    { id: 'story-002', title: 'Le Bec', coverImage: '/images/le-bec-cover.png' }
  ]
};

router.get('/', (req, res) => {
  const { profileId } = req.query;
  if (!profileId) return res.status(400).json({ error: 'Missing profileId' });
  const stories = mockLibrary[profileId as string] || [];
  res.json(stories);
});

export default router;