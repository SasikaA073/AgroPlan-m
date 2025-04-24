import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Map from './components/Map';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Map />} />
          <Route path="/elevation" element={<Map />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
