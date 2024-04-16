import { useEffect, useRef } from "react";

/**
 * Container component that will scroll to the bottom
 * on mount and when the children change.
 *
 * For example, you might consider wrapping your message
 * components this scroll container.
 */
function ScrollContainer({ children }) {
  // Define references to an outer an inner div.
  const outerRef = useRef(null);
  const innerRef = useRef(null);

  // scroll function
  const scrollToBottom = (behavior) => {
    setTimeout(() => {
      outerRef.current.scrollTo({
        top: innerRef.current.scrollHeight,
        left: 0,
        behavior: behavior,
      });
    }, 100); // Adjust the delay as needed
  };

  // scroll to the bottom on mount
  useEffect(
    () => scrollToBottom("instant"),
    [],
  );

  // scroll to the bottom smoothly if children change
  useEffect(
    () => scrollToBottom("smooth"),
    [children],
  );

  // add to the classNames below as needed
  return (
    <div ref={outerRef} className="overflow-y-scroll overflow-x-hidden relative">
      <div ref={innerRef} className="relative">
        {children}
      </div>
    </div>
  );
}


export default ScrollContainer;