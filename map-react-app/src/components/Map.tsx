import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

interface ElevationData {
  latitude: number;
  longitude: number;
  elevation: number;
}

const Map: React.FC = () => {
  const mapRef = useRef<L.Map | null>(null);
  const [elevationData, setElevationData] = useState<ElevationData | null>(null);

  useEffect(() => {
    if (!mapRef.current) {
      // Initialize the map
      mapRef.current = L.map('map').setView([7.8731, 80.7718], 7);

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(mapRef.current);

      // Add click handler for elevation data
      mapRef.current.on('click', async (e) => {
        const { lat, lng } = e.latlng;
        try {
          const response = await axios.get(
            `https://api.open-elevation.com/api/v1/lookup?locations=${lat},${lng}`
          );
          const data = response.data.results[0];
          setElevationData(data);

          // Add marker with elevation popup
          L.marker([lat, lng])
            .addTo(mapRef.current!)
            .bindPopup(`Elevation: ${data.elevation.toFixed(2)} meters`)
            .openPopup();
        } catch (error) {
          console.error('Error fetching elevation data:', error);
        }
      });
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return (
    <div className="map-container">
      <div id="map" style={{ height: 'calc(100vh - 56px)', width: '100%' }} />
      {elevationData && (
        <div className="elevation-info">
          <h3>Elevation Data</h3>
          <p>Latitude: {elevationData.latitude}</p>
          <p>Longitude: {elevationData.longitude}</p>
          <p>Elevation: {elevationData.elevation.toFixed(2)} meters</p>
        </div>
      )}
    </div>
  );
};

export default Map; 