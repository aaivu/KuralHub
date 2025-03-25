import BenchmarkComponent from './BenchMark'
import HomePage from './Home'

const App = () => {
  let page = 'bench'
  return <>{page == 'home' ? <HomePage /> : <BenchmarkComponent />}</>
}

export default App
