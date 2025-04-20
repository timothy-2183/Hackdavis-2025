import { useState } from 'react'
import './Tag.css'

function Tag(tagData) {

  return (
    <div className='tag' style={{backgroundColor: tagData.color || 'red'}}>
        {tagData.text}
    </div>
  )
}

export default Tag