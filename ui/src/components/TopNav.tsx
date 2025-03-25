import { Theme } from '../utils/type'
import { SunIcon, MoonIcon } from './Icons'

interface TopNavProps {
  theme: Theme
  toggleTheme: () => void
}

const TopNav = ({ theme, toggleTheme }: TopNavProps) => {
  return (
    <div className=" bg-secondary-100 flex justify-between p-2 sticky top-0 right-0 border-b-2 border-b-secondary-200">
      <div className="text-xl font-bold tracking-wide">
        <span className="text-primary-950">DB</span>
        <span className="text-primary-800">reeze</span>
      </div>

      <div className=" flex gap-3 text-primary-800">
        <button onClick={toggleTheme}>
          {theme === 'dark' ? <MoonIcon /> : <SunIcon />}
        </button>
      </div>
    </div>
  )
}

export default TopNav
