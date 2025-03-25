import { ArrowRight } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-indigo-600">KuralHub</h1>
            </div>
            <nav className="flex space-x-8">
              <a href="#" className="text-gray-500 hover:text-gray-900 font-medium">Home</a>
              <a href="#benchmarks" className="text-gray-500 hover:text-gray-900 font-medium">Benchmarks</a>
              <a href="#about" className="text-gray-500 hover:text-gray-900 font-medium">About</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Hero Section */}
          <div className="text-center mb-16">
            <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
              Speech Emotion Recognition Benchmarking
            </h2>
            <p className="mt-6 max-w-3xl mx-auto text-xl text-gray-500">
              Comprehensive evaluation of state-of-the-art speech emotion recognition models across multiple languages and language families.
            </p>
            <div className="mt-10">
              <a 
                href="#benchmarks" 
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
              >
                See Our Benchmarks
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Featured Models Section */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Featured Models</h3>
            <div className="bg-white shadow overflow-hidden rounded-lg">
              <div className="px-6 py-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 text-sm text-gray-700">
                <div className="bg-indigo-50 p-3 rounded-lg text-center">HuBERT-base</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">HuBERT-large</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">Wav2Vec2-base</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">Wav2Vec2-large</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">Wav2Vec2-XLS-R</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">WavLM-base</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">WavLM-large</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">Whisper-small</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">Whisper-large</div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">XLS-R-300M</div>
              </div>
            </div>
          </div>

          {/* Image Placeholders Section */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Research Highlights</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Image Placeholder 1 */}
              <div className="bg-white shadow rounded-lg overflow-hidden">
                <div className="aspect-w-16 aspect-h-9 bg-gray-200 flex items-center justify-center">
                  <img 
                    src="/api/placeholder/800/450" 
                    alt="Research visualization placeholder" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-6">
                  <h4 className="text-lg font-medium text-gray-900">Cross-lingual Performance Analysis</h4>
                  <p className="mt-2 text-gray-600">
                    Visualizing how different models perform across language families and emotion categories.
                  </p>
                </div>
              </div>
              
              {/* Image Placeholder 2 */}
              <div className="bg-white shadow rounded-lg overflow-hidden">
                <div className="aspect-w-16 aspect-h-9 bg-gray-200 flex items-center justify-center">
                  <img 
                    src="/api/placeholder/800/450" 
                    alt="Dataset distribution placeholder" 
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-6">
                  <h4 className="text-lg font-medium text-gray-900">Dataset Distribution</h4>
                  <p className="mt-2 text-gray-600">
                    Overview of the various SER datasets included in our comprehensive benchmarking study.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-400">
            <p>© 2025 KuralHub - Speech Emotion Recognition Benchmarking Platform</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;