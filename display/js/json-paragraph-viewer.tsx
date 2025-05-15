import { useState, useEffect } from 'react';

// Sample database structure - replace with your actual data or API call
const sampleDatabase = {
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
  const [database, setDatabase] = useState(sampleDatabase);
  const [selectedFileKey, setSelectedFileKey] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

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
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">JSON Paragraph Database Viewer</h1>
        <p className="text-gray-600">Select a file to view its paragraphs</p>
      </header>

      {isLoading ? (
        <div className="flex justify-center items-center h-40">
          <p className="text-lg text-gray-600">Loading database...</p>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <label htmlFor="fileSelect" className="block text-sm font-medium text-gray-700 mb-2">
              Select File
            </label>
            <select
              id="fileSelect"
              className="w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
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

          {selectedFile ? (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4 text-gray-800">{selectedFile.title}</h2>
              <div className="space-y-4">
                {selectedFile.paragraphs.map((paragraph, index) => (
                  <p key={index} className="text-gray-700 leading-relaxed">
                    {paragraph}
                  </p>
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-white p-6 rounded-lg shadow-md text-center">
              <p className="text-gray-500">Please select a file to view its contents</p>
            </div>
          )}

          <div className="mt-6 text-sm text-gray-500">
            <p>Database contains {Object.keys(database).length} files</p>
          </div>
        </>
      )}
    </div>
  );
}