import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.get('/', (_req, res) => {
  res.send('Super Secret Code Backend is running');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});