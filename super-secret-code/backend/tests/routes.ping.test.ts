import request from 'supertest';
import express from 'express';
import routes from '../routes';

describe('Ping route', () => {
  const app = express();
  app.use(routes);

  it('responds with pong', async () => {
    const res = await request(app).get('/ping');
    expect(res.status).toBe(200);
    expect(res.text).toBe('pong');
  });
});