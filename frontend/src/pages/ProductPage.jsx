import axios from 'axios'
import React from 'react'
import { useState,useEffect } from 'react'
import { useParams } from 'react-router-dom'

export default function ProductPage() {
    const [product,setProductData] = useState(null)
    const {id} = useParams()
    const fetchProductData = async ()=> {
        const response = await axios.get(`http://127.0.0.1:8000/api/product/${id}/`)
        setProductData(response.data)
    }
    useEffect(()=>{
        fetchProductData()
    },[])
    if (!product)
        return <p>LOADING</p>
  return (
    <div>
        <img className='h-48 w-48' src={product.images[0]?.image} alt="" />
        {product.name}
        {product.price}
    </div>
  )
}
