import React from 'react'

export default function Card({ name, price, src }) {
  return (
    <div className="flex flex-col border rounded border-slate-600 bg-white items-center p-4 gap-4 hover:shadow-md">
      <div className="shrink-0">
        <img className="h-24 w-24 object-cover rounded" src={src} alt={name} />
      </div>
      <div>
        <p className="text-lg font-medium text-slate-800">{name}</p>
        <p className="font-normal text-slate-500">Rs : {price}</p>
      </div>
    </div>
  )
}
