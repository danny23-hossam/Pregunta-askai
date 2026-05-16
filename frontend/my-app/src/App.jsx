
import './App.css'
import Header from './Components/Header'
import Footer from './Components/Footer'
import Chat from './Components/Chat'
function App() {


  return (
    <>
    <Header/>
    <div className='chatcontainer'>
        <Chat/>
    </div>
    
    <Footer/>
    </>
  )
}

export default App
