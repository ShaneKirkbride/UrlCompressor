import React from 'react';
import './UrlResult.css'; // Optional: Separate CSS file for styling
function URLResult({ shortURL }) {
    const copyToClipboard = () => {
        navigator.clipboard.writeText(shortURL);
        alert('Short URL copied to clipboard!');
    };

    return (
        <div className="url-result">
            <p>Your shortened URL:</p>
            <div className="short-url-container">
                <a href={shortURL} target="_blank" rel="noopener noreferrer">
                    {shortURL}
                </a>
                <button onClick={copyToClipboard}>Copy</button>
            </div>
        </div>
    );
}

export default URLResult;