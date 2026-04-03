import axios from 'axios'
import React from 'react'
import { useState,useEffect } from 'react'
import { useParams } from 'react-router-dom'
import PageLoader from '../components/PageLoader'

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
        return <PageLoader/>
        
  return (
    <div className='flex flex-col md:flex-row mx-auto justify-center gap-5 p-3'>
        <div className='overflow-hidden border border-white rounded-md shadow-md'>
            <img className='md:h-96 w-full object-cover rounded-md' src={product.images[0]?.image} alt="" />
        </div>
        <div className='flex flex-col items-start border border-white rounded-md p-5 gap-1 md:min-w-60 bg-linear-to-r from-slate-600 to-purple-600 shadow-md'>
            <p className='text-lg font-semibold'>{product.name}</p>
            <p className='text-md'>{product.info}</p>
            <p className='font-bold'>Rs : {product.price}</p>
            <div className='flex flex-col gap-1 mt-2 md:justify-center w-full'>
                <button className='bg-orange-400 p-2 rounded-md font-semibold w-full md:w-auto'>ADD TO CART</button>
                <button className='bg-yellow-400 p-2 rounded-md font-semibold w-full md:w-auto'>BUY NOW</button>
            </div>
        </div>
    </div>
  )
}
