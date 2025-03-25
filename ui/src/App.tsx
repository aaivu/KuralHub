import { useState } from 'react'
import BenchmarkComponent, { BenchmarkData } from './BenchMark'
import HomePage from './Home'
import benchmarkData from './benchmark.json'

const App = () => {
  const [currentPage, setCurrentPage] = useState<'home' | 'benchmark'>('home')
  return (
    <>
      {currentPage == 'home' ? (
        <HomePage goToBenchmark={() => setCurrentPage('benchmark')} />
      ) : (
        <BenchmarkComponent
          goToHome={() => setCurrentPage('benchmark')}
          data={benchmarkData as BenchmarkData}
          baseLogsPath="train_val_test_logs"
        />
      )}
    </>
  )
}

export default App
