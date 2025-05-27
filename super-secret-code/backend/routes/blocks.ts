import { Router } from 'express';

const router = Router();

const mockBlocks = [
  {
    id: 'block-001',
    blockNumber: 1,
    language: 'english',
    letterSet: ['a', 'e', 'm', 's', 't'],
    storyId: 'story-001',
    worksheetURL: '/pdfs/worksheet-block-1-en.pdf'
  },
  {
    id: 'block-002',
    blockNumber: 1,
    language: 'french',
    letterSet: ['a', 'e', 'm', 's', 't'],
    storyId: 'story-002',
    worksheetURL: '/pdfs/worksheet-block-1-fr.pdf'
  }
];

router.get('/', (_req, res) => {
  res.json(mockBlocks);
});

router.get('/:id', (req, res) => {
  const block = mockBlocks.find(b => b.id === req.params.id);
  if (!block) return res.status(404).json({ error: 'Block not found' });
  res.json(block);
});

export default router;