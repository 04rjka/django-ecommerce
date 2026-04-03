import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Card({id, name, price, src }) {
  const navigate = useNavigate()
  return (
    <div onClick={() => navigate(`/product/${id}`)} className="flex flex-col rounded-lg bg-linear-to-b from-gray-100 to-gray-200 items-center justify-center p-1 gap-2 shadow-sm/30">
      <div className="shrink-0 w-full">
        <img className="h-30 md:h-48 w-full object-cover rounded-lg" src={src} alt={name} />
      </div>
      <div className='bg-white w-full p-2 rounded-lg'>
        <p className="text-lg font-medium text-slate-800">{name}</p>
        <p className="font-normal text-slate-500">Rs : {price}</p>
      </div>
    </div>
  )
}
