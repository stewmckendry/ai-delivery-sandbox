import { Router } from 'express';
import authRoutes from './auth';
import profilesRoutes from './profiles';
import progressRoutes from './progress';
import blocksRoutes from './blocks';
import missionsRoutes from './missions';
import storiesRoutes from './stories';
import libraryRoutes from './library';

const router = Router();

router.use('/auth', authRoutes);
router.use('/profiles', profilesRoutes);
router.use('/progress', progressRoutes);
router.use('/blocks', blocksRoutes);
router.use('/missions', missionsRoutes);
router.use('/stories', storiesRoutes);
router.use('/library', libraryRoutes);

router.get('/ping', (_req, res) => {
  res.send('pong');
});

export default router;