// src/components/UrlResult.js

import React from 'react';
import './UrlResult.css';

function URLResult({ shortURL, qrCode }) {
    const copyToClipboard = () => {
        navigator.clipboard.writeText(shortURL);
        alert('Short URL copied to clipboard!');
    };

    return (
        <div className="url-result">
            <p>Your shortened URL:</p>
            <div className="short-url-container">
                <input type="text" value={shortURL} readOnly className="short-url-input" />
                <button onClick={copyToClipboard} className="copy-button">
                    Copy
                </button>
            </div>
            <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" className="qr-code-image" />
        </div>
    );
}

export default URLResult;
