// src/App.js

import React, { Component } from 'react';
import './App.css';
import ShortenURLForm from './components/ShortenUrlForm';
import URLResult from './components/UrlResult';
import { BrowserRouter as Router } from 'react-router-dom';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            shortURL: '',
            qrCode: ''
        };

        // Bind the method to access 'this'
        this.setShortURL = this.setShortURL.bind(this);
    }

    setShortURL(newURL, qrCode) {
        this.setState({ shortURL: newURL, qrCode });
    }

    render() {
        const { shortURL, qrCode } = this.state;
        console.log("Host URL: " + process.env.PUBLIC_URL);

        return (
            <Router basename={process.env.PUBLIC_URL}>
                <div className="app-container">
                    <h1>URL Compressor</h1>
                    <ShortenURLForm setShortURL={this.setShortURL} />
                    {shortURL && <URLResult shortURL={shortURL} qrCode={qrCode} />}
                </div>
            </Router>
        );
    }
}

export default App;
