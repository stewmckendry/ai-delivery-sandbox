import { Router } from 'express';

const router = Router();

const mockMissions = [
  {
    id: 'mission-001',
    lessonBlockId: 'block-001',
    title: 'Sound Isolation - A',
    type: 'phoneme',
    content: {
      letter: 'a',
      audioURL: '/audio/a.mp3'
    },
    badgeId: 'badge-001'
  },
  {
    id: 'mission-004',
    lessonBlockId: 'block-001',
    title: 'Vocabulary Scene - A Words',
    type: 'vocab',
    content: {
      stickers: ['apple', 'ant', 'ax'],
      sceneImage: '/images/kitchen.png'
    },
    badgeId: 'badge-002'
  }
];

router.get('/', (req, res) => {
  const { blockId } = req.query;
  if (!blockId) return res.status(400).json({ error: 'Missing blockId' });
  const missions = mockMissions.filter(m => m.lessonBlockId === blockId);
  res.json(missions);
});

router.get('/:id', (req, res) => {
  const mission = mockMissions.find(m => m.id === req.params.id);
  if (!mission) return res.status(404).json({ error: 'Mission not found' });
  res.json(mission);
});

export default router;