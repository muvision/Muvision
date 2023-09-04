import React from 'react'
import Navbar from './Components/NavBar.jsx'
import { WhiteBoard } from './container/WhiteBoard.jsx'
import { Features } from './container/Features.jsx'
import HowItWorks from './container/HowItWorks.jsx'
import { WhatWeDo } from './container/WhatWeDo.jsx'
import Welcome from './Components/Welcome.jsx'

const App = () => {
  return (
    <>
      <Navbar/>
      <div className="mx-8 md:mx-16 lg:mx-20 xl:mx-40">
        <Welcome/>
        <WhatWeDo/>
        <WhiteBoard/>
        <Features/>
        <HowItWorks/>
      </ div>
    </>
  )
}

export default App