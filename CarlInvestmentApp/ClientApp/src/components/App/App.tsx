import React from 'react';
import { Home } from '../Home/Home';

export const App: React.FC = () => {
  return (
    <div>
      <React.StrictMode>
        <div>
          <Home />
        </div>
      </React.StrictMode>
    </div>
  );
}
