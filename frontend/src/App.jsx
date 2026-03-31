import './App.css'
import { Route,Routes } from 'react-router-dom'
import Home from './pages/Home'
import ProductPage from './pages/ProductPage'
import MainNavbar from './components/MainNavbar'

function App() {

  return (
    <>
    <MainNavbar/>
      <Routes>
          <Route path="/" element={<Home/>}/>
          <Route path="/product/:id" element={<ProductPage/>}/>
      </Routes>
    </>
  )
}

export default App
