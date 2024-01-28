import { useState } from "react";
import ChatDotsIcon from "./assets/chat-dots.svg?react";
import RightArrowIcon from "./assets/right-arrow.svg?react";

const ChatBox = ({ onSubmit }) => {
  const [chatText, setChatText] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const sendChatMessage = async (e) => {
    e.preventDefault();
    document.activeElement?.blur();

    setChatText("");
    onSubmit(chatText);
  };

  const isSendDisabled = chatText === "";

  return (
    <form
      className={
        "relative bg-white rounded-sm transition " +
        (isFocused ? "shadow-xl" : "shadow-lg")
      }
      onSubmit={sendChatMessage}
    >
      <input
        type="text"
        className="block py-4 px-12 w-full bg-transparent border-transparent !outline-none focus:border-transparent focus:ring-0"
        placeholder="Message..."
        value={chatText}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        onChange={(e) => setChatText(e.target.value)}
      />
      <div className="absolute top-1/2 transform -translate-y-1/2 left-4 text-slate-300">
        <ChatDotsIcon strokeWidth={2} className="w-5 h-5" />
      </div>
      <button
        className="flex absolute top-1/2 transform -translate-y-1/2 right-4 text-slate-400"
        aria-label="Send"
        type="submit"
        disabled={isSendDisabled}
      >
        <RightArrowIcon strokeWidth={2} className="w-5 h-5" />
      </button>
    </form>
  );
};

export default ChatBox;
