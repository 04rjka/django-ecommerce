import React from 'react'
import { useParams } from 'react-router-dom'
import PageLoader from '../components/PageLoader'
import useFetch from '../hooks/useFetch'

export default function ProductPage() {

    const {id} = useParams()
    const {data,loading,error} = useFetch(`http://127.0.0.1:8000/api/product/${id}/`)

    if (loading) return <PageLoader/>

    if(error) return <div>ERROR</div>
        
  return (
    <div className='flex flex-col md:flex-row mx-auto justify-center gap-5 p-3'>
        <div className='overflow-hidden  rounded-md shadow-lg'>
            <img className='md:h-96 w-full object-cover rounded-md' src={data.images[0]?.image} alt={data.name} />
        </div>
        <div className='flex flex-col items-start  rounded-md p-5 gap-1 md:min-w-60 bg-linear-to-b from-gray-200 to-gray-300 shadow-lg inset-shadow-sm inset-shadow-gray-50'>
            <p className='text-lg font-semibold'>{data.name}</p>
            <p className='text-md'>{data.info}</p>
            <p className='font-bold'>Rs : {data.price}</p>
            <div className='flex flex-col gap-1 mt-2 md:justify-center w-full'>
                <button className='bg-orange-400 p-2 rounded-md font-semibold w-full md:w-auto'>ADD TO CART</button>
                <button className='bg-yellow-400 p-2 rounded-md font-semibold w-full md:w-auto'>BUY NOW</button>
            </div>
        </div>
    </div>
  )
}
