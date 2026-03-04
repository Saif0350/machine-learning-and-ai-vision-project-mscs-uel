import { orbitron } from "@/app/layout";
import React from "react";

const Header = () => {
  return (
    <header className="w-full bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <h1 className={`${orbitron.className} text-2xl font-bold`}>
          Fruit Classification
        </h1>

        {/* Menu */}
        <nav>
          <ul className="flex gap-8 font-plus font-medium text-gray-700">
            <li className="hover:text-black cursor-pointer">Predict</li>
            <li className="hover:text-black cursor-pointer">About Me</li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
