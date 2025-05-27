import { Router } from 'express';
import authRoutes from './auth';

const router = Router();

router.use('/auth', authRoutes);
router.get('/ping', (_req, res) => {
  res.send('pong');
});

export default router;