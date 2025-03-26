import React, { useEffect, useState } from 'react'
import {
  Grid,
  List,
  ChevronDown,
  ArrowLeft,
  ChevronUp,
  X,
  FileText,
  Image,
} from 'lucide-react'

// Define TypeScript interfaces for our data structure
interface ModelData {
  model: string
  val_accuracy: number
  test_accuracy: number
  logs_path: string
}

interface DatasetData {
  [datasetName: string]: ModelData[]
}

export interface BenchmarkData {
  [language: string]: DatasetData
}

interface HomePageProps {
  goToHome: () => void
  data: BenchmarkData
  baseLogsPath?: string
}

const BenchmarkComponent = ({
  data,
  baseLogsPath,
  goToHome,
}: HomePageProps) => {
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card')
  const [expandedDatasets, setExpandedDatasets] = useState<
    Record<string, boolean>
  >({})
  const [selectedModel, setSelectedModel] = useState<{
    language: string
    dataset: string
    model: ModelData
  } | null>(null)
  const [activeTab, setActiveTab] = useState<
    'info' | 'logs' | 'visualizations'
  >('info')
  const [selectedLogFile, setSelectedLogFile] =
    useState<string>('loss_curve.png')
  const [logContent, setLogContent] = useState('Loading...')

  useEffect(() => {
    if (selectedLogFile?.endsWith('.txt')) {
      const logFilePath = `/${baseLogsPath}/${selectedModel?.model.logs_path}/${selectedModel?.model.logs_path}_${selectedLogFile}`

      fetch(logFilePath)
        .then((response) => response.text())
        .then(setLogContent)
        .catch(() => setLogContent('Error loading file'))
    }
  }, [baseLogsPath, selectedModel, selectedLogFile])

  // Toggle dataset expansion in card view
  const toggleDataset = (language: string, dataset: string) => {
    const key = `${language}-${dataset}`
    setExpandedDatasets((prev) => ({
      ...prev,
      [key]: !prev[key],
    }))
  }

  // Select a model to view details
  const handleSelectModel = (
    language: string,
    dataset: string,
    model: ModelData,
  ) => {
    setSelectedModel({ language, dataset, model })
    setActiveTab('info')
  }

  // Close the detail view
  const handleCloseDetail = () => {
    setSelectedModel(null)
    setSelectedLogFile('loss_curve.png')
  }

  // Helper function to get color based on accuracy
  const getAccuracyColor = (accuracy: number): string => {
    if (accuracy >= 0.8) return 'bg-green-100 text-green-800'
    if (accuracy >= 0.6) return 'bg-blue-100 text-blue-800'
    if (accuracy >= 0.4) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  // Helper function to find the best model in a dataset
  const getBestModel = (models: ModelData[]): ModelData => {
    return models.reduce(
      (best, current) =>
        current.test_accuracy > best.test_accuracy ? current : best,
      models[0],
    )
  }

  return (
    <div className="container mx-auto p-4">
      {/* View switching controls */}
      <div className=" mb-6">
        <a
          onClick={goToHome}
          href="#benchmarks"
          className="inline-flex items-center py-3 text-base font-medium rounded-md"
        >
          <ArrowLeft className="ml-2 h-5 w-5" />
          Back to Home
        </a>
        <h2 className="text-3xl font-bold text-gray-900 mb-6">
          Speech Emotion Recognition Benchmarks
        </h2>
        <p className="text-gray-600 mb-8 max-w-3xl">
          Explore our comprehensive benchmarking results for fine-tuned speech
          models across various languages and datasets. Compare performance
          metrics and access detailed analysis for each model.
        </p>
        {/* <h1 className="text-2xl font-bold text-gray-800">Benchmark Results</h1> */}
        <div className="flex space-x-2 justify-end">
          <button
            onClick={() => setViewMode('card')}
            className={`p-2 rounded-md ${viewMode === 'card' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100'}`}
          >
            <Grid size={20} />
          </button>
          <button
            onClick={() => setViewMode('table')}
            className={`p-2 rounded-md ${viewMode === 'table' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100'}`}
          >
            <List size={20} />
          </button>
        </div>
      </div>

      {/* Card View */}
      {viewMode === 'card' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(data).map(([language, datasets]) => (
            <div key={language} className="col-span-1">
              <div className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="bg-gray-50 px-4 py-3 border-b">
                  <h3 className="text-lg font-semibold text-gray-800">
                    {language}
                  </h3>
                </div>
                <div className="divide-y">
                  {Object.entries(datasets).map(([datasetName, models]) => {
                    const bestModel = getBestModel(models)
                    const isExpanded =
                      expandedDatasets[`${language}-${datasetName}`]

                    return (
                      <div key={datasetName} className="px-4 py-3">
                        <div className="flex justify-between items-center">
                          <h4 className="text-md font-medium text-gray-700">
                            {datasetName}
                          </h4>
                          <button
                            onClick={() => toggleDataset(language, datasetName)}
                            className="p-1 rounded-full hover:bg-gray-100"
                          >
                            {isExpanded ? (
                              <ChevronUp size={18} />
                            ) : (
                              <ChevronDown size={18} />
                            )}
                          </button>
                        </div>

                        {/* Best model card */}
                        <div
                          className="mt-2 p-3 border rounded-md cursor-pointer hover:bg-gray-50"
                          onClick={() =>
                            handleSelectModel(language, datasetName, bestModel)
                          }
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-medium text-gray-900">
                              {bestModel.model}
                            </span>
                            <span className="text-sm text-gray-500">
                              Best Model
                            </span>
                          </div>
                          <div className="mt-2 flex space-x-2">
                            <span
                              className={`px-2 py-1 rounded-full text-xs ${getAccuracyColor(bestModel.test_accuracy)}`}
                            >
                              Test: {(bestModel.test_accuracy * 100).toFixed(1)}
                              %
                            </span>
                            <span
                              className={`px-2 py-1 rounded-full text-xs ${getAccuracyColor(bestModel.val_accuracy)}`}
                            >
                              Val: {(bestModel.val_accuracy * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>

                        {/* Expanded models list */}
                        {isExpanded && (
                          <div className="mt-3 space-y-2">
                            {models
                              .filter(
                                (model) => model.model !== bestModel.model,
                              )
                              .map((model) => (
                                <div
                                  key={model.model}
                                  className="p-2 border rounded-md cursor-pointer hover:bg-gray-50"
                                  onClick={() =>
                                    handleSelectModel(
                                      language,
                                      datasetName,
                                      model,
                                    )
                                  }
                                >
                                  <div className="text-sm font-medium text-gray-800">
                                    {model.model}
                                  </div>
                                  <div className="mt-1 flex space-x-2">
                                    <span
                                      className={`px-2 py-0.5 rounded-full text-xs ${getAccuracyColor(model.test_accuracy)}`}
                                    >
                                      Test:{' '}
                                      {(model.test_accuracy * 100).toFixed(1)}%
                                    </span>
                                    <span
                                      className={`px-2 py-0.5 rounded-full text-xs ${getAccuracyColor(model.val_accuracy)}`}
                                    >
                                      Val:{' '}
                                      {(model.val_accuracy * 100).toFixed(1)}%
                                    </span>
                                  </div>
                                </div>
                              ))}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Table View */}
      {viewMode === 'table' && (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Language
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Dataset
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Val Accuracy
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Test Accuracy
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {Object.entries(data).flatMap(([language, datasets]) =>
                Object.entries(datasets).flatMap(([datasetName, models]) =>
                  models.map((model, idx) => (
                    <tr
                      key={`${language}-${datasetName}-${model.model}-${idx}`}
                      className="hover:bg-gray-50 cursor-pointer"
                      onClick={() =>
                        handleSelectModel(language, datasetName, model)
                      }
                    >
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {language}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {datasetName}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {model.model}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${getAccuracyColor(model.val_accuracy)}`}
                        >
                          {(model.val_accuracy * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${getAccuracyColor(model.test_accuracy)}`}
                        >
                          {(model.test_accuracy * 100).toFixed(1)}%
                        </span>
                      </td>
                    </tr>
                  )),
                ),
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Detail Modal */}
      {selectedModel && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] h-[38rem] flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center p-4 border-b">
              <h2 className="text-xl font-semibold text-gray-800">
                {selectedModel.model.model} - {selectedModel.dataset} (
                {selectedModel.language})
              </h2>
              <button
                onClick={handleCloseDetail}
                className="p-1 rounded-full hover:bg-gray-100"
              >
                <X size={24} />
              </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b">
              <button
                className={`px-4 py-2 font-medium ${activeTab === 'info' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('info')}
              >
                Model Information
              </button>
              <button
                className={`px-4 py-2 font-medium ${activeTab === 'logs' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('logs')}
              >
                Log Files
              </button>
              <button
                className={`px-4 py-2 font-medium ${activeTab === 'visualizations' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('visualizations')}
              >
                Visualizations
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-auto p-4">
              {activeTab === 'info' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-lg font-medium text-gray-800 mb-2">
                        Model Details
                      </h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Language:</span>
                          <span className="font-medium">
                            {selectedModel.language}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Dataset:</span>
                          <span className="font-medium">
                            {selectedModel.dataset}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Model:</span>
                          <span className="font-medium">
                            {selectedModel.model.model}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Logs Path:</span>
                          <span className="font-medium">
                            {selectedModel.model.logs_path}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h3 className="text-lg font-medium text-gray-800 mb-2">
                        Performance Metrics
                      </h3>
                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="text-gray-600">
                              Validation Accuracy:
                            </span>
                            <span
                              className={`font-medium ${selectedModel.model.val_accuracy >= 0.8 ? 'text-green-600' : selectedModel.model.val_accuracy >= 0.6 ? 'text-blue-600' : selectedModel.model.val_accuracy >= 0.4 ? 'text-yellow-600' : 'text-red-600'}`}
                            >
                              {(selectedModel.model.val_accuracy * 100).toFixed(
                                1,
                              )}
                              %
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                              className={`h-2.5 rounded-full ${
                                selectedModel.model.val_accuracy >= 0.8
                                  ? 'bg-green-600'
                                  : selectedModel.model.val_accuracy >= 0.6
                                    ? 'bg-blue-600'
                                    : selectedModel.model.val_accuracy >= 0.4
                                      ? 'bg-yellow-600'
                                      : 'bg-red-600'
                              }`}
                              style={{
                                width: `${selectedModel.model.val_accuracy * 100}%`,
                              }}
                            ></div>
                          </div>
                        </div>

                        <div>
                          <div className="flex justify-between mb-1">
                            <span className="text-gray-600">
                              Test Accuracy:
                            </span>
                            <span
                              className={`font-medium ${selectedModel.model.test_accuracy >= 0.8 ? 'text-green-600' : selectedModel.model.test_accuracy >= 0.6 ? 'text-blue-600' : selectedModel.model.test_accuracy >= 0.4 ? 'text-yellow-600' : 'text-red-600'}`}
                            >
                              {(
                                selectedModel.model.test_accuracy * 100
                              ).toFixed(1)}
                              %
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5">
                            <div
                              className={`h-2.5 rounded-full ${
                                selectedModel.model.test_accuracy >= 0.8
                                  ? 'bg-green-600'
                                  : selectedModel.model.test_accuracy >= 0.6
                                    ? 'bg-blue-600'
                                    : selectedModel.model.test_accuracy >= 0.4
                                      ? 'bg-yellow-600'
                                      : 'bg-red-600'
                              }`}
                              style={{
                                width: `${selectedModel.model.test_accuracy * 100}%`,
                              }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'logs' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="col-span-1 bg-gray-50 p-4 rounded-lg">
                    <h3 className="text-lg font-medium text-gray-800 mb-4">
                      Log Files
                    </h3>
                    <ul className="space-y-2">
                      <li>
                        <button
                          className="flex items-center space-x-2 w-full p-2 rounded hover:bg-gray-200 text-left"
                          onClick={() => setSelectedLogFile(`loss_curve.png`)}
                        >
                          <Image size={16} />
                          <span>Loss Curve</span>
                        </button>
                      </li>
                      <li>
                        <button
                          className="flex items-center space-x-2 w-full p-2 rounded hover:bg-gray-200 text-left"
                          onClick={() =>
                            setSelectedLogFile(`test_classification_report.txt`)
                          }
                        >
                          <FileText size={16} />
                          <span>Test Classification Report</span>
                        </button>
                      </li>
                      <li>
                        <button
                          className="flex items-center space-x-2 w-full p-2 rounded hover:bg-gray-200 text-left"
                          onClick={() =>
                            setSelectedLogFile(`test_confusion_matrix.png`)
                          }
                        >
                          <Image size={16} />
                          <span>Test Confusion Matrix</span>
                        </button>
                      </li>
                      <li>
                        <button
                          className="flex items-center space-x-2 w-full p-2 rounded hover:bg-gray-200 text-left"
                          onClick={() =>
                            setSelectedLogFile(`val_classification_report.txt`)
                          }
                        >
                          <FileText size={16} />
                          <span>Validation Classification Report</span>
                        </button>
                      </li>
                      <li>
                        <button
                          className="flex items-center space-x-2 w-full p-2 rounded hover:bg-gray-200 text-left"
                          onClick={() =>
                            setSelectedLogFile('val_confusion_matrix.png')
                          }
                        >
                          <Image size={16} />
                          <span>Validation Confusion Matrix</span>
                        </button>
                      </li>
                    </ul>
                  </div>

                  <div className="col-span-1 md:col-span-2 bg-white border rounded-lg p-4">
                    {selectedLogFile ? (
                      <>
                        <h3 className="text-lg font-medium text-gray-800 mb-4">
                          {selectedLogFile}
                        </h3>
                        {selectedLogFile.endsWith('.txt') ? (
                          <pre className="bg-gray-50 p-4 rounded-lg overflow-auto max-h-96 text-sm">
                            {logContent}
                          </pre>
                        ) : (
                          <div className="flex justify-center">
                            <img
                              src={`/${baseLogsPath}/${selectedModel.model.logs_path}/${selectedModel.model.logs_path}_${selectedLogFile}`}
                              alt={selectedLogFile}
                              className="max-w-full max-h-96 object-contain"
                            />
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                        <p>Select a log file to view its contents</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'visualizations' && (
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">
                      Model Performance Comparison
                    </h3>
                    <div className="bg-white border rounded-lg p-4">
                      <img
                        src={`${baseLogsPath}/${selectedModel.language}_${selectedModel.dataset}_comparison.png`}
                        alt="Model Comparison"
                        className="max-w-full object-contain mx-auto"
                      />
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-medium text-gray-800 mb-4">
                      Cross-Dataset Performance
                    </h3>
                    <div className="bg-white border rounded-lg p-4">
                      <img
                        src={`${baseLogsPath}/${selectedModel.model.model}_cross_dataset_comparison.png`}
                        alt="Cross-Dataset Comparison"
                        className="max-w-full object-contain mx-auto"
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default BenchmarkComponent
