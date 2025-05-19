import React, { useState, useEffect } from 'react';

// Define TypeScript interfaces for your JSON structure
interface CourseData {
  times_taught: number;
  num_reviews: number;
  avg_rating: number;
  merged_reviews: string;
}

interface Courses {
  [courseCode: string]: CourseData;
}

interface ProfessorData {
  all_merged_reviews: {
    courses: Courses;
  };
}

interface Database {
  [professorId: string]: ProfessorData;
}

// CSS styles without Tailwind
const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '900px',
    margin: '0 auto',
    padding: '24px',
    backgroundColor: '#f9f9f9',
    minHeight: '100vh'
  },
  header: {
    marginBottom: '32px'
  },
  heading: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '8px'
  },
  subheading: {
    color: '#666',
    fontSize: '16px'
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
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    marginBottom: '20px'
  },
  professorName: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '16px',
    color: '#333'
  },
  courseTable: {
    width: '100%',
    borderCollapse: 'collapse' as const,
    marginBottom: '20px'
  },
  tableHeader: {
    textAlign: 'left' as const,
    padding: '10px',
    borderBottom: '2px solid #eee',
    color: '#555',
    fontWeight: 'bold'
  },
  tableCell: {
    padding: '10px',
    borderBottom: '1px solid #eee',
    color: '#333'
  },
  reviewsSection: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#f5f5f5',
    borderRadius: '4px'
  },
  reviewsHeading: {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '10px',
    color: '#444'
  },
  reviewText: {
    lineHeight: '1.6',
    color: '#555',
    whiteSpace: 'pre-wrap' as const
  },
  noReviews: {
    fontStyle: 'italic',
    color: '#888'
  },
  emptyMessage: {
    textAlign: 'center' as const,
    color: '#666'
  },
  footer: {
    marginTop: '24px',
    fontSize: '14px',
    color: '#666'
  },
  error: {
    backgroundColor: '#fee',
    color: '#c00',
    padding: '12px',
    borderRadius: '4px',
    marginBottom: '16px'
  },
  folderInput: {
    display: 'flex',
    marginBottom: '16px'
  },
  folderPath: {
    flexGrow: 1,
    padding: '8px 12px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    marginRight: '8px'
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#4a90e2',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  statHighlight: {
    fontWeight: 'bold',
    color: '#4a90e2'
  },
  courseCodeCell: {
    fontWeight: 'bold',
    color: '#333'
  },
  goodRating: {
    color: '#2e7d32',
    fontWeight: 'bold'
  },
  averageRating: {
    color: '#ff9800',
    fontWeight: 'bold'
  },
  poorRating: {
    color: '#c62828',
    fontWeight: 'bold'
  }
};

export default function ProfessorProfileViewer() {
  const [database, setDatabase] = useState<Database>({});
  const [selectedProfessorId, setSelectedProfessorId] = useState<string>('');
  const [selectedProfessor, setSelectedProfessor] = useState<ProfessorData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [folderPath, setFolderPath] = useState<string>('data/summaries');

  // Effect to update selected professor when ID changes
  useEffect(() => {
    if (selectedProfessorId && database[selectedProfessorId]) {
      setSelectedProfessor(database[selectedProfessorId]);
    } else {
      setSelectedProfessor(null);
    }
  }, [selectedProfessorId, database]);

  // Function to handle professor selection
  const handleProfessorSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedProfessorId(e.target.value);
  };

  // Function to update folder path
  const handleFolderPathChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFolderPath(e.target.value);
  };

  // Helper function to render rating with color
  const renderRating = (rating: number) => {
    if (rating === 0) return <span>No Rating</span>;
    if (rating >= 4) {
      return <span style={styles.goodRating}>{rating.toFixed(2)}</span>;
    } else if (rating >= 3) {
      return <span style={styles.averageRating}>{rating.toFixed(2)}</span>;
    } else {
      return <span style={styles.poorRating}>{rating.toFixed(2)}</span>;
    }
  };

  // Count total courses and reviews for a professor
  const calculateProfessorStats = (courses: Courses) => {
    let totalCourses = 0;
    let totalReviews = 0;
    let totalTimesRated = 0;
    let sumRatings = 0;

    Object.keys(courses).forEach(courseCode => {
      const course = courses[courseCode];
      totalCourses++;
      totalReviews += course.num_reviews;
      totalTimesRated += course.times_taught;
      
      if (course.avg_rating > 0) {
        sumRatings += course.avg_rating;
      }
    });

    const overallAvgRating = totalCourses > 0 ? sumRatings / totalCourses : 0;

    return {
      totalCourses,
      totalReviews,
      totalTimesRated,
      overallAvgRating
    };
  };

  // Import JSON files directly
  const loadProfessorsFromDirectory = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Method 1: Try using dynamic import to get all JSON files
      // This approach requires your bundler (webpack, vite, etc.) to support it
      const importAllJsonFiles = async () => {
        try {
          // First, try the index.json approach (fallback for environments where dynamic imports are limited)
          const response = await fetch(`${folderPath}/index.json`);
          
          if (response.ok) {
            const fileList = await response.json();
            const newDatabase: Database = {};
            
            // Load each professor JSON file listed in the index
            for (const fileName of fileList) {
              try {
                const profResponse = await fetch(`${folderPath}/${fileName}`);
                
                if (!profResponse.ok) {
                  console.error(`Failed to load ${fileName}: ${profResponse.statusText}`);
                  continue;
                }
                
                const professorData = await profResponse.json();
                
                // Extract professor ID (remove .json extension)
                const professorId = fileName.replace('.json', '');
                newDatabase[professorId] = professorData;
              } catch (fileError) {
                console.error(`Error loading ${fileName}:`, fileError);
              }
            }
            
            return newDatabase;
          } else {
            throw new Error("Index.json approach failed, trying directory reading approach");
          }
        } catch (indexError) {
          console.log("Index approach failed, trying direct import...");
          // Method 2: Try to use fetch or specific file imports (better for production)
          
          // For Node.js environments with fs access
          if (typeof window !== 'undefined' && window.fs) {
            try {
              // Read directory using fs if it's available in the environment
              const files = await window.fs.readdir(folderPath);
              const jsonFiles = files.filter(file => file.endsWith('.json'));
              
              const newDatabase: Database = {};
              
              for (const fileName of jsonFiles) {
                try {
                  const fileData = await window.fs.readFile(`${folderPath}/${fileName}`, { encoding: 'utf8' });
                  const professorData = JSON.parse(fileData);
                  const professorId = fileName.replace('.json', '');
                  newDatabase[professorId] = professorData;
                } catch (err) {
                  console.error(`Error reading file ${fileName}:`, err);
                }
              }
              
              return newDatabase;
            } catch (fsError) {
              console.error("Error using fs:", fsError);
              throw fsError;
            }
          } else {
            throw new Error("No method available to read directory contents");
          }
        }
      };
      
      const newDatabase = await importAllJsonFiles();
      
      if (Object.keys(newDatabase).length === 0) {
        throw new Error("No professor data found in the specified directory");
      }
      
      setDatabase(newDatabase);
      
      // If there are professors, select the first one
      const ids = Object.keys(newDatabase);
      if (ids.length > 0) {
        setSelectedProfessorId(ids[0]);
      }
      
    } catch (e) {
      setError(`Error loading professor profiles: ${e instanceof Error ? e.message : String(e)}`);
      console.error("Error loading professor profiles:", e);
      
      // Fall back to the alternative loading method
      loadSampleProfessorData();
    } finally {
      setIsLoading(false);
    }
  };

  // Direct import method for bundlers like webpack that support require.context
  const importJsonFiles = () => {
    try {
      // This is a webpack-specific feature - will need to be adjusted based on your bundler
      // For vite, you would use something like import.meta.glob
      if (typeof require !== 'undefined' && require.context) {
        const context = require.context('data/summaries', false, /\.json$/);
        const newDatabase: Database = {};
        
        context.keys().forEach((key) => {
          const fileName = key.replace('./', '');
          const professorId = fileName.replace('.json', '');
          const professorData = context(key);
          newDatabase[professorId] = professorData;
        });
        
        return newDatabase;
      } else {
        throw new Error("require.context not available");
      }
    } catch (e) {
      console.error("Error importing JSON files:", e);
      throw e;
    }
  };

  // Function to load sample professor data for demonstration
  const loadSampleProfessorData = () => {
    const sampleDatabase: Database = {
      "prof_smith": {
        all_merged_reviews: {
          courses: {
            "INST126": {
              times_taught: 3,
              num_reviews: 5,
              avg_rating: 4.2,
              merged_reviews: "Professor Smith explains concepts clearly and is always available during office hours. Assignments were challenging but fair. Highly recommended!\n\nGreat professor who is passionate about the subject. Lectures were engaging and informative."
            },
            "INST326": {
              times_taught: 2,
              num_reviews: 3,
              avg_rating: 3.8,
              merged_reviews: "The course was well-structured. Professor Smith provides good feedback on assignments. Sometimes the pace was too fast for complex topics."
            }
          }
        }
      },
      "prof_johnson": {
        all_merged_reviews: {
          courses: {
            "INST228": {
              times_taught: 4,
              num_reviews: 8,
              avg_rating: 2.7,
              merged_reviews: "Lectures were disorganized. Grading was inconsistent and feedback was minimal.\n\nThe course material is interesting but the teaching style didn't work for me.\n\nAssignments often unclear with vague requirements."
            },
            "INST208M": {
              times_taught: 1,
              num_reviews: 2,
              avg_rating: 3.5,
              merged_reviews: "This course was better organized than others. Professor Johnson seems to be improving their teaching approach."
            }
          }
        }
      }
    };
    
    setDatabase(sampleDatabase);
    setSelectedProfessorId(Object.keys(sampleDatabase)[0]);
  };

  // Load professors when the component mounts
  useEffect(() => {
    // First try to load from folder, fall back to sample data if that fails
    loadProfessorsFromDirectory().catch(() => {
      loadSampleProfessorData();
    });
  }, []); // Only run on mount, folder changes will be handled by the Load button

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.heading}>Professor Profile Viewer</h1>
        <p style={styles.subheading}>View teaching history and student reviews</p>
      </header>

      <div style={styles.folderInput}>
        <input
          type="text"
          value={folderPath}
          onChange={handleFolderPathChange}
          placeholder="Path to professor JSON files folder"
          style={styles.folderPath}
        />
        <button 
          onClick={loadProfessorsFromDirectory}
          style={styles.button}
        >
          Load Professors
        </button>
      </div>

      {error && (
        <div style={styles.error}>
          {error}
        </div>
      )}

      {isLoading ? (
        <div style={styles.loadingContainer}>
          <p style={styles.loadingText}>Loading professor profiles...</p>
        </div>
      ) : (
        <>
          <div style={styles.formGroup}>
            <label htmlFor="professorSelect" style={styles.label}>
              Select Professor
            </label>
            <select
              id="professorSelect"
              style={styles.select}
              value={selectedProfessorId}
              onChange={handleProfessorSelect}
              disabled={Object.keys(database).length === 0}
            >
              {Object.keys(database).length === 0 ? (
                <option value="">No professor profiles available</option>
              ) : (
                <>
                  <option value="">-- Select a professor --</option>
                  {Object.keys(database).map((id) => (
                    <option key={id} value={id}>
                      {id.replace('prof_', '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                </>
              )}
            </select>
          </div>

          {selectedProfessor ? (
            <div style={styles.contentBox}>
              <h2 style={styles.professorName}>
                {selectedProfessorId.replace('prof_', '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </h2>
              
              {/* Professor Stats Summary */}
              {(() => {
                const stats = calculateProfessorStats(selectedProfessor.all_merged_reviews.courses);
                return (
                  <div style={styles.contentBox}>
                    <p>
                      <strong>Courses Taught:</strong> <span style={styles.statHighlight}>{stats.totalCourses}</span> | 
                      <strong> Total Times Taught:</strong> <span style={styles.statHighlight}>{stats.totalTimesRated}</span> | 
                      <strong> Total Reviews:</strong> <span style={styles.statHighlight}>{stats.totalReviews}</span> | 
                      <strong> Overall Rating:</strong> {renderRating(stats.overallAvgRating)}
                    </p>
                  </div>
                );
              })()}
              
              {/* Course Table */}
              <h3 style={styles.reviewsHeading}>Course History</h3>
              <table style={styles.courseTable}>
                <thead>
                  <tr>
                    <th style={styles.tableHeader}>Course</th>
                    <th style={styles.tableHeader}>Times Taught</th>
                    <th style={styles.tableHeader}>Reviews</th>
                    <th style={styles.tableHeader}>Rating</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.keys(selectedProfessor.all_merged_reviews.courses).map((courseCode) => {
                    const course = selectedProfessor.all_merged_reviews.courses[courseCode];
                    return (
                      <tr key={courseCode}>
                        <td style={{...styles.tableCell, ...styles.courseCodeCell}}>{courseCode}</td>
                        <td style={styles.tableCell}>{course.times_taught}</td>
                        <td style={styles.tableCell}>{course.num_reviews}</td>
                        <td style={styles.tableCell}>{renderRating(course.avg_rating)}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              
              {/* Reviews Section */}
              <div style={styles.reviewsSection}>
                <h3 style={styles.reviewsHeading}>Student Reviews by Course</h3>
                
                {Object.keys(selectedProfessor.all_merged_reviews.courses).map((courseCode) => {
                  const course = selectedProfessor.all_merged_reviews.courses[courseCode];
                  return (
                    <div key={courseCode} style={{marginBottom: '20px'}}>
                      <h4 style={{fontSize: '16px', fontWeight: 'bold', marginBottom: '5px'}}>
                        {courseCode} ({renderRating(course.avg_rating)})
                      </h4>
                      
                      {course.merged_reviews ? (
                        <p style={styles.reviewText}>{course.merged_reviews}</p>
                      ) : (
                        <p style={styles.noReviews}>No reviews available for this course.</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div style={styles.contentBox}>
              <p style={styles.emptyMessage}>
                {Object.keys(database).length === 0 
                  ? "No professor profiles loaded. Please check the folder path and try again." 
                  : "Please select a professor to view their profile"}
              </p>
            </div>
          )}

          <div style={styles.footer}>
            <p>Database contains {Object.keys(database).length} professor profiles</p>
          </div>
        </>
      )}
    </div>
  );
}