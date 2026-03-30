import React from 'react'
import { useNavigate } from 'react-router-dom'

export default function Card({id, name, price, src }) {
  const navigate = useNavigate()
  return (
    <div onClick={() => navigate(`/product/${id}`)} className="flex flex-col border rounded border-slate-600 bg-white items-center justify-center p-4 gap-4 hover:shadow-md">
      <div className="shrink-0">
        <img className="h-30 w-full object-cover rounded" src={src} alt={name} />
      </div>
      <div>
        <p className="text-lg font-medium text-slate-800">{name}</p>
        <p className="font-normal text-slate-500">Rs : {price}</p>
      </div>
    </div>
  )
}
