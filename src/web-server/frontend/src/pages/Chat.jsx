// Chat.tsx

import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { HiArrowCircleUp } from 'react-icons/hi';
import { v4 as uuidv4 } from 'uuid';
import ErrorBlock from '../components/ui/ErrorBlock';
import { getAgentForChat, submitChatPrompt } from '../js/api';

const Chat = () => {
  const { agent } = useParams();
  const containerRef = useRef(null);
  const buttonRef = useRef(null);
  const inputRef = useRef(null);
  const [containerHeight, setContainerHeight] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [agentData, setAgentData] = useState({
    name: '',
    welcome_message: 'Hello! How can I help you today?',
    suggested_prompts: ['', '', ''],
  });

  const [messages, setMessages] = useState([
    { id: uuidv4(), content: agentData.welcome_message, role: 'system' },
  ]);
  const [input, setInput] = useState('');

  const handleSendMessage = async () => {
    if (input.trim()) {
      const userMessage = { id: uuidv4(), content: input, role: 'user' };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput('');
      setLoading(true);

      const data = {
        input: input,
        messages: messages
      };

      try {
        const responsedata = await submitChatPrompt(agent, data);
        const responseMessage = {
          id: uuidv4(),
          content: responsedata.content.toString(),
          role: responsedata.role,
        };
        setMessages((prevMessages) => [...prevMessages, responseMessage]);
      } catch (err) {
        console.error(err);
        setError('Failed to send message.');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSuggestedPrompt = (index) => {
    if (index >= 0 && index < agentData.suggested_prompts.length) {
      setInput(agentData.suggested_prompts[index]);
      inputRef.current?.focus();
    }
  };

  useEffect(() => {
    const handleResize = (entry) => {
      setContainerHeight(entry.contentRect.height);
      window.parent.postMessage(
        { type: 'iframeHeight', height: entry.contentRect.height },
        window.location.origin
      );
    };

    const fetchAgentData = async (agent) => {
      try {
        setLoading(true);
        setError(null);
        const responsedata = await getAgentForChat(agent);
        if (responsedata && responsedata.agent) {
          // get agent data
          const data = responsedata.agent;
          if (data.welcome_message) {
            const welcomeMessage = {
              id: uuidv4(),
              content: data.welcome_message,
              role: 'system',
            };
            setMessages([welcomeMessage]);
          }
          setAgentData({
            name: data.name,
            welcome_message: data.welcome_message,
            suggested_prompts: data.suggested_prompts
          });
        }
      } catch (err) {
        console.error(err);
        setError('Failed to load agent data.');
      } finally {
        setLoading(false);
      }
    };

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        handleResize(entry);
      }
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    if (agent) {
      fetchAgentData(agent);
    }

    return () => {
      resizeObserver.disconnect();
    };
  }, [agent]);

  const string2array = (input) => {
    // Split the input string by commas and limit to 3 elements
    let result = input ? input.split(',').slice(0, 3) : [];

    // Fill the array with empty strings if it's less than 3 items
    while (result.length < 3) {
      result.push('');
    }

    return result;
  }

  return (
    <div ref={containerRef} className="flex flex-col h-max p-4 w-full">
      {/* Suggested Prompts */}
      <div className="flex flex-row gap-4 w-full mb-4">
        {agentData.suggested_prompts.map((prompt, index) => (
          <div
            key={index}
            onClick={() => handleSuggestedPrompt(index)}
            className="flex-1 cursor-pointer rounded-lg bg-gray-100 text-xs font-thin text-gray-800 p-4 border border-gray-200"
          >
            {prompt}
          </div>
        ))}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((message) =>
          message.role === 'user' ? (
            <div
              key={message.id}
              className="my-2 p-2 rounded-lg bg-gray-100 text-gray-800 self-end text-right max-w-[70%] ml-auto"
            >
              {message.content}
            </div>
          ) : (
            <div
              key={message.id}
              className="my-2 p-2 rounded-lg text-black self-start max-w-full mr-auto"
            >
              {message.content}
            </div>
          )
        )}
      </div>

      {/* Input Area */}
      {!loading && !error && (
        <div className="flex items-center rounded-full bg-gray-100 px-4 py-2">

          {/* Text Input */}
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Message your smart agent"
            rows={1}
            className="flex-1 bg-transparent resize-none outline-none overflow-hidden"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
          />

          {/* Send Button */}
          <button
            ref={buttonRef}
            className="cursor-pointer"
            onClick={handleSendMessage}
            aria-label="Send Message"
          >
            <HiArrowCircleUp className="text-3xl" />
          </button>
        </div>
      )}

      {/* Error and Loading Messages */}
      {error && <ErrorBlock>{error}</ErrorBlock>}
      {loading && !error && (
        <div className="px-2 font-thin text-xs md:text-sm lg:text-md text-gray-800">
          Agent is working on your request...
        </div>
      )}
    </div>
  );
};

export default Chat;
