import { Router } from 'express';
import authRoutes from './auth';
import profilesRoutes from './profiles';

const router = Router();

router.use('/auth', authRoutes);
router.use('/profiles', profilesRoutes);

router.get('/ping', (_req, res) => {
  res.send('pong');
});

export default router;