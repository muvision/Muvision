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

export default function Footer() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
    return (
      <footer className="bg-white border-t mt-10 border-theme">
        <nav className="mx-auto flex items-center justify-between p-10 lg:px-8" aria-label="Global">
            <Popover.Group className="flex items-center">
                <a href="https://github.com/muvision/Muvision" className="text-gray-400 text-s font-light leading-6 hover:text-theme hover:scale-110 transform transition ease-in-out duration-150">
                <div className="flex items-center"> {/* Center content vertically */}
                    <img className="opacity-50 h-12 w-auto scale-50" src="./github-mark.svg" alt="" />
                    <span className="ml-2">Github Repo</span> {}
                </div>
                </a>
            </Popover.Group>
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
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  <a
                    href="#"
                    className="-mx-3 block rounded-lg px-3 py-2  font-semibold text-gray-900 hover:text-theme hover:scale-130 transform transition ease-in-out duration-150"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    HOME
                  </a>
                </div>
              </div>
            </div>
          </Dialog.Panel>
        </Dialog>
      </footer>
    )
  }