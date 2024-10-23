import React, { useState } from 'react';
import axios from 'axios';
import './ShortenUrlForm.css';

function ShortenURLForm({ setShortURL }) {
    const [originalURL, setOriginalURL] = useState('');
    const [expirationTime, setExpirationTime] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://localhost:8000/shorten', {
                original_url: originalURL,
                expiration_time: expirationTime ? parseInt(expirationTime, 10) : null,
            });
            setShortURL(response.data.short_url);
            setOriginalURL('');
            setExpirationTime('');
        } catch (error) {
            alert('Error creating short URL');
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="shorten-form">
            <input
                type="url"
                placeholder="Enter the long URL"
                value={originalURL}
                onChange={(e) => setOriginalURL(e.target.value)}
                required
            />
            <input
                type="number"
                placeholder="Expiration time in seconds (optional)"
                value={expirationTime}
                onChange={(e) => setExpirationTime(e.target.value)}
            />
            <button type="submit">Shorten URL</button>
        </form>
    );
}

export default ShortenURLForm;
