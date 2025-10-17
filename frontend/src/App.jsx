// frontend/src/App.js
import React, { useState } from 'react';
import Converter from './pages/Converter.jsx';
import DocumentationLog from './components/DocumentationLog.jsx';

const styles = {
  container: {
    backgroundColor: '#282c34',
    minHeight: '100vh',
    padding: '20px',
    color: 'white',
    fontFamily: 'sans-serif',
  },
  nav: { marginBottom: '30px' },
  button: {
    margin: '0 10px',
    padding: '10px 15px',
    fontSize: '1rem',
    cursor: 'pointer',
    backgroundColor: '#61dafb',
    border: 'none',
    borderRadius: '5px'
  }
};

function App() {
  const [view, setView] = useState('converter'); // 'converter' or 'admin'

  return (
    <div style={styles.container}>
      <nav style={styles.nav}>
        <button style={styles.button} onClick={() => setView('converter')}>Converter</button>
        <button style={styles.button} onClick={() => setView('admin')}>Admin Log</button>
      </nav>
      <hr/>
      {view === 'converter' ? <Converter /> : <DocumentationLog />}
    </div>
  );
}

export default App;