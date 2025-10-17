// frontend/src/components/DocumentationLog.jsx
import React, { useState, useEffect } from 'react';
import { getLogs, addLog } from '../api';

export default function DocumentationLog() {
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState('');
  const [newLog, setNewLog] = useState({ log_type: 'Update', details: '' });

  const handleLogin = async () => {
    try {
      const response = await getLogs(password);
      setLogs(response.data);
      setIsLoggedIn(true);
      setError('');
    } catch (err) {
      setError('Authentication failed.');
    }
  };

  const handleAddLog = async (e) => {
    e.preventDefault();
    try {
        await addLog(newLog, password);
        // Refresh logs
        const response = await getLogs(password);
        setLogs(response.data);
        setNewLog({ log_type: 'Update', details: '' }); // Reset form
    } catch (err) {
        setError('Failed to add log entry.');
    }
  };

  if (!isLoggedIn) {
    return (
      <div>
        <h2>Admin Log Access</h2>
        <input
          type="password"
          placeholder="Enter Admin Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    );
  }

  return (
    <div>
        <h2>Project Documentation Log</h2>
        <form onSubmit={handleAddLog}>
            <select value={newLog.log_type} onChange={e => setNewLog({...newLog, log_type: e.target.value})}>
                <option>Update</option>
                <option>Issue</option>
                <option>Maintenance</option>
            </select>
            <input
              type="text"
              placeholder="Log details"
              value={newLog.details}
              onChange={e => setNewLog({...newLog, details: e.target.value})}
              required
            />
            <button type="submit">Add Log</button>
        </form>
        <hr/>
        {logs.map(log => (
            <div key={log.id} style={{ border: '1px solid #555', padding: '10px', margin: '10px 0' }}>
                <p><strong>{log.log_type}</strong> ({new Date(log.timestamp).toLocaleString()})</p>
                <p>{log.details}</p>
            </div>
        ))}
    </div>
  );
}