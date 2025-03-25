import { SendIcon, UploadIcon } from './components/Icons'
import Button from './parts/Button'

const Home = () => {
  return (
    <div className="h-full flex flex-col justify-end p-3 w-full">
      <div className="overflow-scroll">
        <div className="w-8/12 m-auto flex-grow">
          
        </div>
      </div>
      <div className="m-auto w-8/12 bg-secondary-200 rounded-xl p-3">
        <input
          placeholder="Chat with DBreeze"
          className=" bg-transparent w-full outline-none border-none focus:outline-none focus:border-none focus:ring-0"
        />
        <div className=" flex justify-between items-center">
          <Button className="bg-transparent hover:bg-transparent text-primary-900">
            <UploadIcon />
          </Button>
          <Button className=" rounded-full w-8 h-8">
            <SendIcon strokeWidth={3} />
          </Button>
        </div>
      </div>
    </div>
  )
}

export default Home
