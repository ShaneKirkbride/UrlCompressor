import React from 'react'; // Core React library
import ReactDOM from 'react-dom'; // DOM-specific methods
import App from './App'; // Main App component

// Render the App component into the DOM inside the element with id 'root'
ReactDOM.render(
    <React.StrictMode>
        <App />  {/* Renders your main application */}
    </React.StrictMode>,
    document.getElementById('root') // DOM element where the app is mounted
);
