"use client";
import Image from "next/image";
import React, { useState } from "react";
// import ContactButton from "../ContactButton";
import Link from "next/link";
import gsap from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
gsap.registerPlugin(ScrollToPlugin);
const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const handleScroll = (targetId: any) => {
    const target = document.getElementById(targetId);
    if (target) {
      gsap.to(window, {
        duration: 1,
        scrollTo: { y: target, offsetY: 58 }, // Offset for fixed header, if any
        ease: "power2.inOut",
      });
    }
  };

  return (
    <header className="bg-white sticky top-0 z-50">
      <nav className="container mx-auto flex items-center justify-between py-4 px-5 md:px-10 lg:py-4">
        {/* Logo Section */}
        <h2 className="text-3xl font-semibold tracking-widest text-primaryMain">
          Fruit Classification
        </h2>
        <a href={"#"} className="block w-24 lg:w-32 ">
          {/* <Image
            src=""
            alt=""
            className="w-full object-contain"
            height={200}
            width={500}
            sizes="(min-width: 1040px) 160px, 122px"
            priority
          /> */}
        </a>

        {/* Navigation Links */}
        <div className="hidden lg:flex items-center gap-8 text-xs tracking-widest font-medium uppercase">
          <a
            href="#home"
            onClick={(e) => {
              e.preventDefault();
              handleScroll("home");
            }}
            className="hover-class"
          >
            Predict
          </a>
          <a
            href="#about"
            onClick={(e) => {
              e.preventDefault();
              handleScroll("about");
            }}
            className="hover-class"
          >
            About Me
          </a>
        </div>

        {/* Contact Button */}
        {/* <div className="">
          <ContactButton text="Contact Us" />
        </div> */}

        {/* Hamburger Menu for Mobile */}
        <button
          className="block lg:hidden text-gray-800 focus:outline-none"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle Menu"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d={
                isMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"
              }
            />
          </svg>
        </button>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed top-0 right-0 h-full w-[100%] bg-white z-50 transition-transform transform ease duration-500 ${
          isMenuOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between p-5">
          <a
            onClick={() => setIsMenuOpen(false)}
            href="#"
            className="block w-24"
          >
            {/* <Image
              src="/"
              alt="UXCELLENCE "
              className="w-full object-contain"
              height={200}
              width={500}
              sizes="128px"
              priority
            /> */}
          </a>
          <h2 className="text-3xl font-semibold tracking-widest text-primaryGreen">
            UXCELLENCE
          </h2>
          <button
            onClick={() => setIsMenuOpen(false)}
            className="text-gray-800 focus:outline-none"
            aria-label="Close Menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <ul className="flex flex-col gap-7 p-5 text-xs font-medium uppercase tracking-widest">
          <li onClick={() => setIsMenuOpen(false)}>
            <a href="#" className="hover:text-primaryGreen">
              Home
            </a>
          </li>
          <li onClick={() => setIsMenuOpen(false)}>
            <a href="#about" className="hover:text-primaryGreen">
              About
            </a>
          </li>
          <li onClick={() => setIsMenuOpen(false)}>
            <a href="#portfolio" className="hover:text-primaryGreen">
              Our Portfolio
            </a>
          </li>
          <li onClick={() => setIsMenuOpen(false)}>
            <a href="#services" className="hover:text-primaryGreen">
              Services
            </a>
          </li>
        </ul>
      </div>
      {/* Backdrop */}
      {isMenuOpen && (
        <div
          onClick={() => setIsMenuOpen(false)}
          className="fixed inset-0 bg-black opacity-50 z-40"
        ></div>
      )}
    </header>
  );
};

export default Header;
