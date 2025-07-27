
import './App.css'
import { Route,Routes } from 'react-router-dom'
import Layout from './components/Layout'
import CreatePage from './pages/CreatePage'
import HomePage from './pages/Home'
import FinalVideoPage from './pages/FinalVideoPage'
function App() {

  return (
    
    <Routes>
     
      <Route path="/" element={<Layout/>}>
         <Route index element = {<HomePage/>}></Route>
         <Route path='/create' element={<CreatePage/>}></Route>
         <Route path='/video/:id' element={<FinalVideoPage/>}></Route>
      </Route>
    </Routes>


        
  )
}

export default App
