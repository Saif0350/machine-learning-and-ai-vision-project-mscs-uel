import Image from "next/image";
import React from "react";
import ContactButton from "./ContactButton";

const Hero = () => {
  return (
    <div
      id="home"
      className="templateContainer flex flex-col items-center lg:flex-row lg:h-[650px] gap-6 pb-6"
    >
      <div
        data-aos="zoom-out"
        className="w-full lg:w-[60%] my-auto pt-8 lg:pt-0 space-y-4"
      >
        <span className="text-primaryGreen uppercase tracking-widest font-normal text-sm">
          Fruit Classification{" "}
        </span>
        <div className="space-y-1 -ml-1">
          <h1 className="text-primaryDark text-[45px] leading-none lg:text-6xl tracking-wide uppercase font-extrabold">
            Empowering Your
          </h1>
          <h2 className="text-[35px] leading-none lg:text-6xl uppercase text-primaryGreen tracking-wide font-extrabold">
            Digital Journey
          </h2>
        </div>
        <p className="text-sm tracking-wide w-full lg:w-[90%] text-gray-700">
          Web Development. Digital Marketing. SEO. All-in-One Solutions to
          Elevate Your Business.
        </p>
        <ContactButton text="Get in touch" />
      </div>
      {/* ----------------- */}
      <div data-aos="zoom-out" className="w-full mt-5 lg:mt50 lg:w-[40%]">
        <div className="">
          <Image
            src="/bulb.png"
            alt="Hero Image"
            className="lg:h-[450px] bouncing object-contain w-full"
            height={800}
            width={800}
          />
        </div>
        <div className="flex -mt-5 ml-3 items-center justify-center ">
          <Image
            src="/shadow.png"
            className=" h-10 w-48"
            alt="Hero Image"
            height={200}
            width={1000}
          />
        </div>
      </div>
    </div>
  );
};

export default Hero;
