// frontend/src/pages/Converter.jsx
import React, { useState } from 'react';
import { getFileColumns, convertAndDownload } from '../api';

const TALLY_FIELDS = ['Date', 'Party', 'Amount']; // The required fields

export default function Converter() {
  const [file, setFile] = useState(null);
  const [fileColumns, setFileColumns] = useState([]);
  const [mappings, setMappings] = useState(
    TALLY_FIELDS.reduce((acc, field) => ({ ...acc, [field]: '' }), {})
  );
  const [status, setStatus] = useState({ message: '', error: '' });

  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setStatus({ message: 'Analyzing file...', error: '' });
    setFileColumns([]);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await getFileColumns(formData);
      setFileColumns(response.data.columns);
      setStatus({ message: 'File analyzed. Please map columns.', error: '' });
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to read file.';
      setStatus({ message: '', error: errorMsg });
    }
  };

  const handleMappingChange = (tallyField, fileColumn) => {
    setMappings((prev) => ({ ...prev, [tallyField]: fileColumn }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setStatus({ message: '', error: 'Please select a file.' });
      return;
    }

    setStatus({ message: 'Processing...', error: '' });

    const formData = new FormData();
    formData.append('file', file);
    formData.append('mappings', JSON.stringify(mappings));

    try {
        const response = await convertAndDownload(formData);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'tally_output.xml');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        setStatus({ message: 'Conversion successful! Download started.', error: '' });
    } catch (err) {
        const errorData = await err.response.data.text();
        const errorJson = JSON.parse(errorData);
        setStatus({ message: '', error: `Conversion Failed: ${errorJson.error}` });
    }
  };

  return (
    <div>
      <h1>Tally Converter</h1>
      <p>1. Upload your .xlsx or .csv file</p>
      <input type="file" accept=".xlsx, .csv" onChange={handleFileChange} />

      {fileColumns.length > 0 && (
        <form onSubmit={handleSubmit}>
          <p>2. Map your columns to Tally fields</p>
          {TALLY_FIELDS.map((field) => (
            <div key={field} style={{ margin: '10px 0' }}>
              <label style={{ marginRight: '10px', minWidth: '80px', display: 'inline-block' }}>{field}:</label>
              <select
                value={mappings[field]}
                onChange={(e) => handleMappingChange(field, e.target.value)}
                required
              >
                <option value="">Select Column</option>
                {fileColumns.map((col) => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>
          ))}
          <button type="submit" style={{ marginTop: '15px' }}>Convert and Download XML</button>
        </form>
      )}

      {status.message && <p style={{ color: '#6bff9b' }}>{status.message}</p>}
      {status.error && <p style={{ color: '#ff6b6b' }}>{status.error}</p>}
    </div>
  );
}