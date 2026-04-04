import React from 'react'
import { useParams } from 'react-router-dom'
import PageLoader from '../components/PageLoader'
import useFetch from '../hooks/useFetch'
import ReviewCard from '../components/ReviewCard'
import Spinner from '../components/Spinner'

export default function ProductPage() {

    const {id} = useParams()
    const {data,loading,error} = useFetch(`http://127.0.0.1:8000/api/product/${id}/`)
    const {data: reviews,loading:reviewsLoading,error:reviewsError} = useFetch(`http://127.0.0.1:8000/api/product/${id}/reviews/`)

    if (loading) return <PageLoader/>

    if(error) return <div>ERROR</div>
        
  return (
    <div className='flex flex-col mx-auto max-w-5xl p-3 gap-5'>
        <div className='flex flex-col md:flex-row mx-auto justify-center gap-5'>
            <div className='overflow-hidden  rounded-md shadow-lg'>
                <img className='md:h-96 w-full object-cover rounded-md' src={data.images[0]?.image} alt={data.name} />
            </div>
            <div className='flex flex-col items-start md:max-w-xl rounded-md p-5 gap-1 md:min-w-60 bg-linear-to-b from-gray-200 to-gray-300 shadow-lg inset-shadow-sm inset-shadow-gray-50'>
                <p className='text-lg font-semibold'>{data.name}</p>
                <p className='text-md'>{data.info}</p>
                <p className='font-bold'>Rs : {data.price}</p>
                <div className='flex flex-col gap-2 mt-2 md:justify-center w-full'>
                    <button className='bg-orange-400 p-2 rounded-md font-semibold w-full md:w-auto inset-shadow-sm inset-shadow-orange-200 shadow-sm hover:bg-orange-300'>ADD TO CART</button>
                    <button className='bg-yellow-400 p-2 rounded-md font-semibold w-full md:w-auto inset-shadow-sm inset-shadow-yellow-200 shadow-sm hover:bg-yellow-300'>BUY NOW</button>
                </div>
            </div>
        </div>

        <div className='flex flex-col bg-linear-to-b from-gray-200 to-gray-300 p-3 rounded-md inset-shadow-sm inset-shadow-gray-50 shadow-lg'>
            <h2 className='text-lg font-semibold'>Reviews</h2>
            {reviewsLoading && (
                <div className='flex justify-center py-3'>
                    <Spinner/>
                </div>
            )}
            {!reviewsLoading && reviewsError && (
                <p className='text-red-500'>{reviewsError}</p>
            )}
            {!reviewsLoading && reviews?.length === 0 && !reviewsError && (
                <p className='text-slate-600'>No reviews yet.</p>
            )}
            {!reviewsLoading && reviews?.map(review => (
                <ReviewCard key={review.id} {...review}/>
            ))}
        </div>
    </div>
  )
}
