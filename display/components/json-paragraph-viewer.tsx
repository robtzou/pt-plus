import React, { useState, useEffect } from 'react';

// Define TypeScript interfaces
interface ParagraphFile {
  title: string;
  paragraphs: string[];
}

interface Database {
  [key: string]: ParagraphFile;
}

// CSS styles without Tailwind
const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '24px',
    backgroundColor: '#f9f9f9',
    minHeight: '100vh'
  },
  header: {
    marginBottom: '32px'
  },
  heading: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '8px'
  },
  subheading: {
    color: '#666'
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '160px'
  },
  loadingText: {
    fontSize: '18px',
    color: '#666'
  },
  formGroup: {
    marginBottom: '24px'
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#444',
    marginBottom: '8px'
  },
  select: {
    width: '100%',
    border: '1px solid #ccc',
    borderRadius: '4px',
    padding: '8px 12px',
    backgroundColor: 'white',
    outline: 'none'
  },
  contentBox: {
    backgroundColor: 'white',
    padding: '24px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  contentTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    marginBottom: '16px',
    color: '#333'
  },
  paragraph: {
    color: '#444',
    lineHeight: '1.6',
    marginBottom: '16px'
  },
  emptyMessage: {
    textAlign: 'center' as const,
    color: '#666'
  },
  footer: {
    marginTop: '24px',
    fontSize: '14px',
    color: '#666'
  }
};

// Sample database structure - replace with your actual data or API call
const sampleDatabase: Database = {
  "file1": {
    "title": "Introduction to React",
    "paragraphs": [
      "React is a JavaScript library for building user interfaces.",
      "It allows developers to create large web applications that can change data without reloading the page.",
      "The main purpose of React is to be fast, scalable, and simple."
    ]
  },
  "file2": {
    "title": "Working with JSON",
    "paragraphs": [
      "JSON (JavaScript Object Notation) is a lightweight data-interchange format.",
      "It is easy for humans to read and write and easy for machines to parse and generate.",
      "JSON is text-based and language-independent, making it an ideal data-exchange format."
    ]
  },
  "file3": {
    "title": "Database Fundamentals",
    "paragraphs": [
      "A database is an organized collection of structured information, or data, typically stored electronically in a computer system.",
      "Databases are designed to store, retrieve, modify, and delete data efficiently.",
      "Most databases use structured query language (SQL) for writing and querying data.",
      "NoSQL databases like MongoDB store data in more flexible formats like JSON documents."
    ]
  }
};

export default function JsonParagraphViewer() {
  const [database, setDatabase] = useState<Database>(sampleDatabase);
  const [selectedFileKey, setSelectedFileKey] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<ParagraphFile | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Effect to update selected file when key changes
  useEffect(() => {
    if (selectedFileKey && database[selectedFileKey]) {
      setSelectedFile(database[selectedFileKey]);
    } else {
      setSelectedFile(null);
    }
  }, [selectedFileKey, database]);

  // Function to handle file selection
  const handleFileSelect = (e) => {
    setSelectedFileKey(e.target.value);
  };

  // Simulating loading data from an API
  const loadDatabase = () => {
    setIsLoading(true);
    // Simulate API call with timeout
    setTimeout(() => {
      setDatabase(sampleDatabase);
      setIsLoading(false);
    }, 500);
  };

  // Load database on component mount
  useEffect(() => {
    loadDatabase();
  }, []);

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.heading}>JSON Paragraph Database Viewer</h1>
        <p style={styles.subheading}>Select a file to view its paragraphs</p>
      </header>

      {isLoading ? (
        <div style={styles.loadingContainer}>
          <p style={styles.loadingText}>Loading database...</p>
        </div>
      ) : (
        <>
          <div style={styles.formGroup}>
            <label htmlFor="fileSelect" style={styles.label}>
              Select File
            </label>
            <select
              id="fileSelect"
              style={styles.select}
              value={selectedFileKey}
              onChange={handleFileSelect}
            >
              <option value="">-- Select a file --</option>
              {Object.keys(database).map((key) => (
                <option key={key} value={key}>
                  {database[key].title || key}
                </option>
              ))}
            </select>
          </div>

          <div style={styles.contentBox}>
            {selectedFile ? (
              <>
                <h2 style={styles.contentTitle}>{selectedFile.title}</h2>
                <div>
                  {selectedFile.paragraphs.map((paragraph, index) => (
                    <p key={index} style={styles.paragraph}>
                      {paragraph}
                    </p>
                  ))}
                </div>
              </>
            ) : (
              <p style={styles.emptyMessage}>Please select a file to view its contents</p>
            )}
          </div>

          <div style={styles.footer}>
            <p>Database contains {Object.keys(database).length} files</p>
          </div>
        </>
      )}
    </div>
  );
}