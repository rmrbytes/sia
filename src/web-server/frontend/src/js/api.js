// api.js
import axios from 'axios';

// The X-Requested-With header
const X_REQUEST_STR = 'XteNATqxnbBkPa6TCHcK0NTxOM1JVkQl'
// Create BaseURL
const baseUrl = window.location.origin;

// Standard Error handler
const handleAxiosError = (error) => {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      // Server responded with an error status
      const errorMessage = error.response.data.detail || 'An error occurred on the server';
      throw new Error(errorMessage);
    } else if (error.request) {
      throw new Error('No response received from the server. Please try again later.');
    }
  } else if (error instanceof Error) {
    throw new Error(error.message);
  } else {
    throw new Error('An unexpected error occurred');
  }
};

// get agent for chat which is a subset of normal get agent
export const getAgentForChat = async (agentname) => {
  try {
    const response = await axios.get(`${baseUrl}/api/chat/${agentname}`,
      {
        withCredentials: true,
        headers: { 'X-Requested-With': X_REQUEST_STR },
      });
    return response.data;
  }
  catch (e) {
    handleAxiosError(e);
  }
}

// submit chat prompt to llm
export const submitChatPrompt = async (agentname, data) => {
  try {
    const response = await axios.post(`${baseUrl}/api/chat/${agentname}`,
      data,
      {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/plain;charset=utf-8',
          'X-Requested-With': X_REQUEST_STR
        },
      });
    return response.data;
  }
  catch (e) {
    handleAxiosError(e);
  }
}
