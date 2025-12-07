import { useState, useEffect } from 'react';

const useSelectedText = () => {
  const [selectedText, setSelectedText] = useState('');
  const [selectionPosition, setSelectionPosition] = useState({ x: 0, y: 0 });
  const [isSelectionVisible, setIsSelectionVisible] = useState(false);

  useEffect(() => {
    let timeoutId;

    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length > 5 && text.length < 500) { // Only show for selections longer than 5 characters
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectionPosition({
          x: rect.right + window.scrollX - 30, // Position to the right of selection
          y: rect.top + window.scrollY - 40   // Position above selection
        });

        setSelectedText(text);
        setIsSelectionVisible(true);

        // Auto-hide after 5 seconds if not clicked
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
          setIsSelectionVisible(false);
        }, 5000);
      } else {
        setIsSelectionVisible(false);
        setSelectedText('');
      }
    };

    const debouncedHandleSelection = () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(handleSelection, 100); // Debounce by 100ms
    };

    document.addEventListener('mouseup', debouncedHandleSelection);
    document.addEventListener('selectionchange', debouncedHandleSelection);

    // Cleanup function
    return () => {
      document.removeEventListener('mouseup', debouncedHandleSelection);
      document.removeEventListener('selectionchange', debouncedHandleSelection);
      clearTimeout(timeoutId);
    };
  }, []);

  return {
    selectedText,
    selectionPosition,
    isSelectionVisible,
    clearSelection: () => {
      setSelectedText('');
      setIsSelectionVisible(false);
    }
  };
};

export default useSelectedText;