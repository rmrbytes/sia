import { forwardRef, useState } from 'react';


const InputText = forwardRef(
  ({ id, label, value, placeholder, ...rest }, ref) => {

    // states
    const [isFocused, setIsFocused] = useState(false);
    // functions
    const handleFocus = () => setIsFocused(true);
    const handleBlur = () => setIsFocused(false);

    return (
      <div className="relative mb-6">
        <label htmlFor={id}
          className={`absolute left-0 transform transition-all duration-200 ease-in-out ${value || isFocused
            ? 'text-xs -top-4 text-gray-700'
            : 'text-base top-2.5 text-gray-500'
            }`}
        >
          {label}
        </label>
        <input
          ref={ref}
          id={id}
          name={id}
          type="text"
          value={value}
          placeholder={isFocused ? placeholder : ''}
          autoComplete="off"
          onFocus={handleFocus}
          onBlur={handleBlur}
          className={`w-full border-b-2 ${
            isFocused ? 'border-black' : 'border-gray-300'
          } focus:outline-none py-2 bg-transparent`}
          {...rest} // Spread the rest of the input props
        />
      </div>
    );
  }
);

export default InputText;
