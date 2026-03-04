import React from "react";

interface ContactButtonProps {
  text?: string;
}

const ContactButton: React.FC<ContactButtonProps> = ({ text }) => {
  return (
    <button className="bg-primaryGreen text-white border border-primaryBorder  px-4 md:px-6 py-2.5 md:py-3 rounded text-xs tracking-widest uppercase font-medium hover:opacity-80 transition">
      {text}
    </button>
  );
};

export default ContactButton;
