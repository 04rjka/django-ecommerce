import React from 'react'
import { useState,useEffect } from 'react'
import Card from '../components/Card'
import axios from "axios"



export default function Home() {
  const [data,setData] = useState([])
  const fetchData = async ()=> {
  const response = await axios.get("http://127.0.0.1:8000/api/products/")
  setData(response.data)
  }

  useEffect(()=>{
    fetchData()
  },[])
  return (
    <div className='grid grid-cols-2 sm:grid-cols-3 p-2 gap-2'>
      {data.map(product =>(
        <Card key={product.id} name={product.name} price={product.price} src={product.images[0]?.image}/>
      ))}
    </div>
  )
}
