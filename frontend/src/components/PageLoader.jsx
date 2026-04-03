import React from 'react'
import Spinner from './Spinner'

export default function PageLoader() {
  return (
    <div className='h-[calc(100vh-5rem)] flex items-center justify-center'>
            <Spinner/>
    </div>
  )
}
