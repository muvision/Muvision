// import React from 'react';
// import './NavBar.css';
// import { GiHamburgerMenu } from 'react-icons/gi';
// import { MdCloseFullscreen } from "react-icons/md";

// const Navbar = () => {
//   const [toggleMenu, setToggleMenu] = React.useState(false);
//   return (
//     <nav className="app__navbar">
//       <ul className="app__navbar-links">
//         <li><a href="#home">HOME</a></li>
//         <li><a href="#whatwedo">WHAT WE DO</a></li>
//         <li><a href="#features">FEATURES</a></li>
//         <li><a href="#howitworks">HOW IT WORKS</a></li>
//         <li><a href="#getApp">GET THE APP</a></li>
//       </ul>
//       <div className="app__navbar-smallscreen">
//         <GiHamburgerMenu color="#000" fontSize={27} onClick={() => setToggleMenu(true)} />
//         {toggleMenu && (
//           <div className="app__navbar-smallscreen_overlay flex__center slide-bottom">
//             <MdCloseFullscreen fontSize={27} className="overlay__close" onClick={() => setToggleMenu(false)} />
//             <ul className="app__navbar-smallscreen_links">
//               <li><a href="#home" onClick={() => setToggleMenu(false)}>Home</a></li>
//               <li><a href="#whatwedo" onClick={() => setToggleMenu(false)}>What We Do</a></li>
//               <li><a href="#features" onClick={() => setToggleMenu(false)}>Features</a></li>
//               <li><a href="#howitworks" onClick={() => setToggleMenu(false)}>How It Works</a></li>
//               <li><a href="#getApp" onClick={() => setToggleMenu(false)}>Get The App</a></li>
//             </ul>
//           </div>
//         )}
//       </div>
//     </nav>
//   );
// };

// export default Navbar;


import { Fragment, useState } from 'react'
import { Dialog, Disclosure, Popover, Transition } from '@headlessui/react'
import {
  ArrowPathIcon,
  Bars3Icon,
  ChartPieIcon,
  CursorArrowRaysIcon,
  FingerPrintIcon,
  SquaresPlusIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { ChevronDownIcon, PhoneIcon, PlayCircleIcon } from '@heroicons/react/20/solid'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="bg-white border-b border-theme mb-5">
      <nav className="mx-auto flex items-center justify-between p-3 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <a href="#" className="">
            <span className="sr-only">Your Company</span>
            <img className="h-12 w-auto scale-150 translate-y-3 mx-[38px] md:mx-[70px] lg:mx-[66px] xl:mx-[146px]" src="./MuvisionLogo.svg" alt="" />
          </a>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <Popover.Group className="hidden lg:flex lg:gap-x-12">
          <a href="#home" className="text-xl font-semibold leading-6 text-gray-900 hover:text-theme hover:scale-110 transform transition ease-in-out duration-150">
            HOME
          </a>
          <a href="#features" className="text-xl font-semibold leading-6 text-gray-900 hover:text-theme hover:scale-110 transform transition ease-in-out duration-150">
            FEATURES
          </a>
          <a href="#howitworks" className="text-xl font-semibold leading-6 text-gray-900 hover:text-theme hover:scale-110 transform transition ease-in-out duration-150">
            HOW IT WORKS
          </a>
        </Popover.Group>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end mx-8 md:mx-16 lg:mx-20 xl:mx-40">
          <a href="#" className="text-sm font-semibold leading-6 text-gray-900">
            <button className="bg-theme hover:bg-theme-stroke text-white font-bold py-2 px-4 rounded my-2 hover:font-bold hover:scale-110 transform transition ease-in-out duration-150">GET THE APP</button>
            
          </a>
        </div>
      </nav>
      <Dialog as="div" className="lg:hidden" open={mobileMenuOpen} onClose={setMobileMenuOpen} >
        <div className="fixed inset-0 z-10" />
        <Dialog.Panel className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10" style={{backgroundColor:'white'}}>
          <div className="flex items-center justify-between">
            <a href="#" className="-m-1.5 p-1.5">
              <span className="sr-only">MuVision</span>
              <svg
                className="h-8 w-auto"
                // src="./MuvisionLogo.svg"
                src= "https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
                alt=""
              />
            </a>
            <button
              type="button"
              className="-m-2.5 rounded-md p-2.5 text-gray-700"
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="sr-only">Close menu</span>
              <XMarkIcon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div className="mt-6 flow-root">
            <div className="-my-6 divide-y divide-gray-500/10">
              <div className="space-y-2 py-6">
                <a
                  href="#home"
                  className=" block rounded-lg px-3 py-2  font-semibold text-gray-900 hover:text-theme hover:scale-130 transform transition ease-in-out duration-150"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  HOME
                </a>
                <a
                  href="#features"
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  FEATURES
                </a>
                <a
                  href="#howitworks"
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  HOW IT WORKS
                </a>
              </div>
              <div className="py-6">
                <a
                  href="#"
                  className="-mx-3 block rounded-lg px-3 py-2.5 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50 text-black"
                >
                  GET THE APP
                </a>
              </div>
            </div>
          </div>
        </Dialog.Panel>
      </Dialog>
    </header>
  )
}