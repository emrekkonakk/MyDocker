import React from 'react';

const Modal = ({ isOpen, close, children }) => {
  if (!isOpen) return null;

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0, 0, 0, 0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ padding: 20, background: '#fff', borderRadius: 5, position: 'relative' }}>
        <button onClick={close} style={{ position: 'absolute', right: 10, top: 10 }}>Close</button>
        {children}
      </div>
    </div>
  );
};

export default Modal;
