import React, { useState } from 'react';
import ShortenURLForm from './components/ShortenURLForm';
import URLResult from './components/URLResult';
import './App.css';

function App() {
    const [shortURL, setShortURL] = useState(null);

    return (
        <div className="app-container">
            <h1>URL Shortener</h1>
            <ShortenURLForm setShortURL={setShortURL} />
            {shortURL && <URLResult shortURL={shortURL} />}
        </div>
    );
}

export default App;