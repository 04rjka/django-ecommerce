import React from 'react'

export default function Card({name,price,src}) {
  return (
    <>
        <div className="w-40 sm:w-60 md:w-75 flex flex-col border rounded border-slate-600 bg-white md:flex-row items-center p-4 max-w-sm mx-auto gap-4 hover:shadow-md">
        <div className="shrink-0">
            <img className="h-24 w-24 object-cover rounded" src={src} alt=""/>
        </div>
        <div>
            <p className="text-lg font-medium text-slate-800">{name}</p>
            <p className="font-normal text-slate-500">Rs : {price}</p>
        </div>
    </div>
    </>
  )
}
