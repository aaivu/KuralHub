import React, { useState, useEffect } from 'react'
import { ChevronDown, ChevronUp, Search, Grid, List, Eye } from 'lucide-react'

const BenchmarkComponent = () => {
  const [data, setData] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [viewMode, setViewMode] = useState('card') // 'card' or 'table'
  const [expandedLanguage, setExpandedLanguage] = useState('')
  const [expandedDataset, setExpandedDataset] = useState('')

  // Fetch the benchmark data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // In production, replace with actual API call
        // const response = await fetch('/api/benchmarks');
        // const jsonData = await response.json();

        // For demo purposes, using the sample data
        const sampleData = {
          'Amharic (am)': {
            ASED: [
              {
                model: 'hubert-base-ls960',
                val_accuracy: 0.88,
                test_accuracy: 0.89,
                logs_path: 'am_ASED_hubert-base-ls960',
              },
              {
                model: 'hubert-large-ls960-ft',
                val_accuracy: 0.64,
                test_accuracy: 0.63,
                logs_path: 'am_ASED_hubert-large-ls960-ft',
              },
              {
                model: 'wav2vec2-base',
                val_accuracy: 0.75,
                test_accuracy: 0.75,
                logs_path: 'am_ASED_wav2vec2-base',
              },
            ],
          },
          'Bengali (bn)': {
            BANSpEmo: [
              {
                model: 'hubert-base-ls960',
                val_accuracy: 0.52,
                test_accuracy: 0.41,
                logs_path: 'bn_BANSpEmo_hubert-base-ls960',
              },
              {
                model: 'hubert-large-ls960-ft',
                val_accuracy: 0.24,
                test_accuracy: 0.23,
                logs_path: 'bn_BANSpEmo_hubert-large-ls960-ft',
              },
            ],
            SUBESCO: [
              {
                model: 'hubert-base-ls960',
                val_accuracy: 0.77,
                test_accuracy: 0.78,
                logs_path: 'bn_SUBESCO_hubert-base-ls960',
              },
              {
                model: 'whisper-small',
                val_accuracy: 0.88,
                test_accuracy: 0.89,
                logs_path: 'bn_SUBESCO_whisper-small',
              },
            ],
          },
        }

        setData(sampleData)
        setIsLoading(false)
      } catch (error) {
        console.error('Error loading benchmark data:', error)
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  // Toggle language expansion
  const toggleLanguage = (language: string) => {
    setExpandedLanguage(expandedLanguage === language ? '' : language)
  }

  // Toggle dataset expansion
  const toggleDataset = (dataset: string) => {
    setExpandedDataset(expandedDataset === dataset ? '' : dataset)
  }

  // Card View Component
  const CardView = () => {
    return (
      <div className="space-y-8">
        {Object.entries(data).map(([language, datasets]) => (
          <div
            key={language}
            className="border border-gray-200 rounded-lg overflow-hidden"
          >
            <div
              className={`flex justify-between items-center px-6 py-4 bg-gray-50 cursor-pointer ${expandedLanguage === language ? 'border-b border-gray-200' : ''}`}
              onClick={() => toggleLanguage(language)}
            >
              <h3 className="text-xl font-bold text-gray-800">{language}</h3>
              <div className="flex items-center">
                <span className="text-gray-500 mr-2">
                  {Object.keys(datasets).length} datasets
                </span>
                {expandedLanguage === language ? (
                  <ChevronUp className="h-5 w-5" />
                ) : (
                  <ChevronDown className="h-5 w-5" />
                )}
              </div>
            </div>

            {expandedLanguage === language && (
              <div className="p-6 space-y-6">
                {Object.entries(datasets).map(([datasetName, models]) => (
                  <div
                    key={datasetName}
                    className="border border-gray-200 rounded-lg overflow-hidden"
                  >
                    <div
                      className={`flex justify-between items-center px-4 py-3 bg-gray-50 cursor-pointer ${expandedDataset === `${language}_${datasetName}` ? 'border-b border-gray-200' : ''}`}
                      onClick={() =>
                        toggleDataset(`${language}_${datasetName}`)
                      }
                    >
                      <h4 className="font-semibold text-gray-700">
                        {datasetName}
                      </h4>
                      <div className="flex items-center">
                        <span className="text-gray-500 mr-2">
                          {models.length} models
                        </span>
                        {expandedDataset === `${language}_${datasetName}` ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </div>
                    </div>

                    {expandedDataset === `${language}_${datasetName}` && (
                      <div className="p-4">
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                          {models.map((model) => (
                            <div
                              key={model.model}
                              className="border border-gray-200 rounded-lg p-4 hover:border-indigo-500 hover:shadow-md transition-all duration-300"
                            >
                              <h5 className="font-medium text-gray-900 mb-3 truncate">
                                {model.model}
                              </h5>

                              <div className="space-y-3 mb-4">
                                <div>
                                  <div className="flex justify-between text-sm mb-1">
                                    <span className="text-gray-500">
                                      Test Accuracy
                                    </span>
                                    <span className="font-medium">
                                      {(model.test_accuracy * 100).toFixed(1)}%
                                    </span>
                                  </div>
                                  <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                      className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                                      style={{
                                        width: `${model.test_accuracy * 100}%`,
                                      }}
                                    ></div>
                                  </div>
                                </div>

                                <div>
                                  <div className="flex justify-between text-sm mb-1">
                                    <span className="text-gray-500">
                                      Val Accuracy
                                    </span>
                                    <span className="font-medium">
                                      {(model.val_accuracy * 100).toFixed(1)}%
                                    </span>
                                  </div>
                                  <div className="w-full bg-gray-200 rounded-full h-2">
                                    <div
                                      className="bg-green-500 h-2 rounded-full transition-all duration-500"
                                      style={{
                                        width: `${model.val_accuracy * 100}%`,
                                      }}
                                    ></div>
                                  </div>
                                </div>
                              </div>

                              <button
                                onClick={() =>
                                  alert(
                                    `View details for ${model.model} in ${language} - ${datasetName}`,
                                  )
                                }
                                className="w-full flex items-center justify-center px-4 py-2 border border-indigo-500 text-indigo-500 rounded-md hover:bg-indigo-500 hover:text-white transition-colors duration-300"
                              >
                                <Eye className="h-4 w-4 mr-2" />
                                View Details
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    )
  }

  // Display loading indicator
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    )
  }

  return (
    <div
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12"
      id="benchmarks"
    >
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">
          Speech Emotion Recognition Benchmarks
        </h2>
        <p className="text-gray-600 mb-8 max-w-3xl">
          Explore our comprehensive benchmarking results for fine-tuned speech
          models across various languages and datasets. Compare performance
          metrics and access detailed analysis for each model.
        </p>

        {/* View toggle */}
        <div className="flex items-center space-x-2 mb-6">
          <button
            className={`p-2 rounded-md ${viewMode === 'card' ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600'}`}
            onClick={() => setViewMode('card')}
            title="Card View"
          >
            <Grid className="h-5 w-5" />
          </button>
          <button
            className={`p-2 rounded-md ${viewMode === 'table' ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-600'}`}
            onClick={() => setViewMode('table')}
            title="Table View"
          >
            <List className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Content based on view mode */}
      {viewMode === 'card' ? (
        <CardView />
      ) : (
        <div className="bg-white shadow rounded-lg p-6">
          <p className="text-center text-gray-500">
            Table view will be implemented next
          </p>
        </div>
      )}
    </div>
  )
}

export default BenchmarkComponent
