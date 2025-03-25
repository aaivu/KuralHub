import { useState, useEffect, useLayoutEffect } from 'react'
import TopNav from './components/TopNav'
import { Theme } from './utils/type'
import Home from './Home'
import { useKeycloak } from '@react-keycloak/web'

const App = () => {
  const [theme, setTheme] = useState<Theme>('light')
  const { initialized } = useKeycloak()

  useLayoutEffect(() => {
    const theme = localStorage.getItem('theme')
    if (theme === 'light' || theme === 'dark') {
      setTheme(theme as Theme)
    }
  }, [])

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prv) => {
      const theme = prv === 'dark' ? 'light' : 'dark'
      localStorage.setItem('theme', theme)
      return theme
    })
  }
  return (
    <div className="bg-secondary-50 h-screen w-screen flex flex-col text-primary-950">
      {initialized ? (
        <>
          <header className="w-full h-fit">
            <TopNav theme={theme} toggleTheme={toggleTheme} />
          </header>
          <main className="flex flex-grow w-screen overflow-hidden text-sm">
            <div className="w-full  h-full">
              <Home />
            </div>
          </main>
        </>
      ) : (
        <div className="flex w-full h-full justify-center items-center ">
          <span
            style={{ height: '40px', width: '40px' }}
            className="border-primary-500 dbreeze-loader"
          ></span>
        </div>
      )}
    </div>
  )
}

export default App
