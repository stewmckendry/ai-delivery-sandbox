import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { SoundIsolation } from '../components/learning/SoundIsolation';

vi.mock('../hooks/useAudio', () => ({
  useAudio: () => vi.fn()
}));

describe('<SoundIsolation />', () => {
  it('renders a letter button and plays audio on click', async () => {
    render(<SoundIsolation letter="a" audioURL="/audio/a.mp3" />);
    const button = screen.getByRole('button', { name: 'a' });
    expect(button).toBeInTheDocument();
    await userEvent.click(button);
  });
});