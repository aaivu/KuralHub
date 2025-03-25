import {
  ArrowRight,
  Award,
  BookOpen,
  Github,
  LinkedinIcon,
  Users,
  Cpu,
  FileBarChart2,
} from 'lucide-react'

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-indigo-600">KuralHub</h1>
            </div>
            <nav className="flex space-x-8">
              <a
                href="#"
                className="text-gray-500 hover:text-gray-900 font-medium"
              >
                Home
              </a>
              <a
                href="#benchmarks"
                className="text-gray-500 hover:text-gray-900 font-medium"
              >
                Benchmarks
              </a>
              <a
                href="#about"
                className="text-gray-500 hover:text-gray-900 font-medium"
              >
                About Us
              </a>
              <a
                href="https://github.com/kuralhub/ser-benchmarks"
                className="text-gray-500 hover:text-gray-900"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="w-6 h-6" />
              </a>
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
              Comprehensive evaluation of speech models fine-tuned for emotion
              recognition tasks across multiple languages and language families.
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
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Cpu className="mr-2" />
              Models Used for SER Fine-tuning
            </h3>
            <div className="bg-white shadow overflow-hidden rounded-lg">
              <div className="px-6 py-5 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 text-sm text-gray-700">
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  HuBERT-base
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  HuBERT-large
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  Wav2Vec2-base
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  Wav2Vec2-large
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  Wav2Vec2-XLS-R
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  WavLM-base
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  WavLM-large
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  Whisper-small
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  Whisper-large
                </div>
                <div className="bg-indigo-50 p-3 rounded-lg text-center">
                  XLS-R-300M
                </div>
              </div>
            </div>
          </div>

          {/* Image Placeholders Section */}
          <div className="mb-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <FileBarChart2 className="mr-2" />
              Research Highlights
            </h3>
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
                  <h4 className="text-lg font-medium text-gray-900">
                    Cross-lingual Performance Analysis
                  </h4>
                  <p className="mt-2 text-gray-600">
                    Visualizing how different models perform across language
                    families and emotion categories.
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
                  <h4 className="text-lg font-medium text-gray-900">
                    Dataset Distribution
                  </h4>
                  <p className="mt-2 text-gray-600">
                    Overview of the various SER datasets included in our
                    comprehensive benchmarking study.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* About Our Team Section */}
          <div id="about" className="mb-16">
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Users className="mr-2" />
              About Our Team
            </h3>
            <div className="bg-white shadow rounded-lg overflow-hidden">
              <div className="p-6">
                <p className="text-gray-700 mb-8">
                  We are a dedicated research team focused on advancing speech
                  emotion recognition technology across different languages and
                  language families. Our benchmarking platform provides
                  comprehensive evaluations of state-of-the-art speech models
                  fine-tuned for emotion recognition tasks.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {/* Team Member 1 - Senior Lecturer */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-center mb-4">
                      <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center">
                        <Award className="w-12 h-12 text-indigo-600" />
                      </div>
                      <h4 className="font-bold text-lg">Dr. Jane Doe</h4>
                      <p className="text-gray-500 text-sm">Senior Lecturer</p>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Leading researcher in speech processing and emotion
                      recognition with 15+ years of experience.
                    </p>
                    <div className="flex justify-center space-x-3">
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Github className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <LinkedinIcon className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <BookOpen className="w-5 h-5" />
                      </a>
                    </div>
                  </div>

                  {/* Team Member 2 - Student */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-center mb-4">
                      <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center">
                        <Users className="w-12 h-12 text-indigo-600" />
                      </div>
                      <h4 className="font-bold text-lg">Alex Smith</h4>
                      <p className="text-gray-500 text-sm">PhD Researcher</p>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Specialized in cross-lingual speech emotion recognition
                      and neural network architecture.
                    </p>
                    <div className="flex justify-center space-x-3">
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Github className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <LinkedinIcon className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <BookOpen className="w-5 h-5" />
                      </a>
                    </div>
                  </div>

                  {/* Team Member 3 - Student */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-center mb-4">
                      <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center">
                        <Users className="w-12 h-12 text-indigo-600" />
                      </div>
                      <h4 className="font-bold text-lg">Maria Garcia</h4>
                      <p className="text-gray-500 text-sm">PhD Researcher</p>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Focused on data collection, preprocessing, and model
                      fine-tuning for emotion detection.
                    </p>
                    <div className="flex justify-center space-x-3">
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Github className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <LinkedinIcon className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <BookOpen className="w-5 h-5" />
                      </a>
                    </div>
                  </div>

                  {/* Team Member 4 - Student */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-center mb-4">
                      <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-3 flex items-center justify-center">
                        <Users className="w-12 h-12 text-indigo-600" />
                      </div>
                      <h4 className="font-bold text-lg">David Kim</h4>
                      <p className="text-gray-500 text-sm">PhD Researcher</p>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">
                      Specializes in benchmarking methodologies and multilingual
                      dataset curation.
                    </p>
                    <div className="flex justify-center space-x-3">
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Github className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <LinkedinIcon className="w-5 h-5" />
                      </a>
                      <a
                        href="#"
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <BookOpen className="w-5 h-5" />
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-gray-900 to-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center mb-6">
                <h3 className="text-white text-xl font-bold">KuralHub</h3>
                <div className="ml-2 w-2 h-2 rounded-full bg-indigo-500"></div>
              </div>
              <p className="text-gray-400 mb-6">
                A comprehensive benchmarking platform for speech emotion
                recognition across multiple languages and language families.
              </p>
              <div className="flex space-x-4">
                <a
                  href="https://github.com/kuralhub/ser-benchmarks"
                  className="bg-gray-700 p-2 rounded-full hover:bg-indigo-600 transition-colors duration-300"
                >
                  <Github className="w-5 h-5 text-white" />
                </a>
                <a
                  href="#"
                  className="bg-gray-700 p-2 rounded-full hover:bg-indigo-600 transition-colors duration-300"
                >
                  <LinkedinIcon className="w-5 h-5 text-white" />
                </a>
                <a
                  href="#"
                  className="bg-gray-700 p-2 rounded-full hover:bg-indigo-600 transition-colors duration-300"
                >
                  <BookOpen className="w-5 h-5 text-white" />
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-white text-lg font-bold mb-6">Quick Links</h3>
              <ul className="space-y-3">
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white flex items-center transition-colors duration-300"
                  >
                    <div className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></div>
                    Home
                  </a>
                </li>
                <li>
                  <a
                    href="#benchmarks"
                    className="text-gray-400 hover:text-white flex items-center transition-colors duration-300"
                  >
                    <div className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></div>
                    Benchmarks
                  </a>
                </li>
                <li>
                  <a
                    href="#about"
                    className="text-gray-400 hover:text-white flex items-center transition-colors duration-300"
                  >
                    <div className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></div>
                    About Us
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/kuralhub/ser-benchmarks"
                    className="text-gray-400 hover:text-white flex items-center transition-colors duration-300"
                  >
                    <div className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></div>
                    GitHub Repository
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-white flex items-center transition-colors duration-300"
                  >
                    <div className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></div>
                    Publications
                  </a>
                </li>
              </ul>
            </div>

            <div>
              <h3 className="text-white text-lg font-bold mb-6">Contact</h3>
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="bg-indigo-600 p-2 rounded-md mr-3 mt-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                  <div>
                    <p className="text-white font-medium">Email</p>
                    <p className="text-gray-400">contact@kuralhub.org</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="bg-indigo-600 p-2 rounded-md mr-3 mt-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                  </div>
                  <div>
                    <p className="text-white font-medium">Location</p>
                    <p className="text-gray-400">
                      Department of Computer Science
                      <br />
                      University Research Center
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 mb-4 md:mb-0">
              © 2025 KuralHub - Speech Emotion Recognition Benchmarking
              Platform. All rights reserved.
            </p>
            <div className="flex space-x-6 text-gray-400">
              Designed by <strong className=" pl-1"> Luxshan Thavarasa</strong>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default HomePage
