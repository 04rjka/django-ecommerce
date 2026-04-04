import React from 'react'

export default function ReviewCard({ user, title, content, created_at}) {
  return (
    <div className='flex flex-col gap-1 rounded-md bg-gray-100 py-2 px-4 mt-2  inset-shadow-sm inset-shadow-slate-50'>
        <div className='flex items-center justify-between'>
        <p className='font-semibold text-slate-800'>{user}</p>
        <p className='text-sm text-slate-500'>{new Date(created_at).toLocaleDateString("en-IN",{
            year:"numeric",
            month:"long",
            day:"numeric"
        })}</p>
        </div>
        <p className='font-medium text-slate-700'>{title}</p>
        <p className='text-slate-600'>{content}</p>
    </div>
  )
}
