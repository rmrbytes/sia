const ErrorBlock = ({ children }) => (
  <blockquote className="text-gray-800 border-l-4 border-red-400 pl-4 text-sm font-semibold">
    {children}
  </blockquote>
);

export default ErrorBlock;