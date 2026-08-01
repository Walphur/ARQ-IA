import { render, screen } from '@testing-library/react';
import App from './App';

test('renderiza marca ARQ-IA en login', () => {
  render(<App />);
  expect(screen.getAllByText(/ARQ-IA/i).length).toBeGreaterThan(0);
});
