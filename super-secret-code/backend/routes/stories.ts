import { Router } from 'express';

const router = Router();

const mockStories = [
  {
    id: 'story-001',
    title: 'A Bat',
    language: 'english',
    pages: ['/images/a-bat-1.png', '/images/a-bat-2.png'],
    sightWords: ['a', 'the']
  },
  {
    id: 'story-002',
    title: 'Le Bec',
    language: 'french',
    pages: ['/images/le-bec-1.png', '/images/le-bec-2.png'],
    sightWords: ['le', 'du']
  }
];

router.get('/', (_req, res) => {
  res.json(mockStories);
});

router.get('/:id', (req, res) => {
  const story = mockStories.find(s => s.id === req.params.id);
  if (!story) return res.status(404).json({ error: 'Story not found' });
  res.json(story);
});

export default router;