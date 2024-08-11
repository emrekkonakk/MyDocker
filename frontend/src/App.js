import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [countries, setCountries] = useState([]);
  const [cities, setCities] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/v1/countries`);
        const data = await response.json();
        if (response.ok) {
          setCountries(data);  // Assuming the API returns an array of country objects
        } else {
          console.error('Failed to fetch countries:', data.message);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchCountries();
  }, []);

  useEffect(() => {
    const fetchCities = async () => {
      if (!selectedCountry) {
        setCities([]);  // Clear cities if no country is selected
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/v1/countries/${selectedCountry}/cities`);
        const data = await response.json();
        if (response.ok) {
          setCities(data);  // Assuming the API returns an array of city objects
        } else {
          console.error('Failed to fetch cities:', data.message);
          setCities([]);  // Clear cities if fetch failed
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setCities([]);  // Clear cities if there's an error
      }
    };

    fetchCities();
  }, [selectedCountry]);

  useEffect(() => {
    const fetchRestaurants = async () => {
      if (!selectedCity) {
        setRestaurants([]);  // Clear restaurants if no city is selected
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/v1/cities/${selectedCity}/restaurants`);
        const data = await response.json();
        if (response.ok) {
          setRestaurants(data);
        } else {
          console.error('Failed to fetch restaurants:', data.message);
          setRestaurants([]);  // Clear restaurants if fetch failed
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setRestaurants([]);  // Clear restaurants if there's an error
      }
    };

    fetchRestaurants();
  }, [selectedCity]);  // This ensures that the fetch operation is re-run when selectedCity changes

  return (
    <div className="App">
      <header className="App-header">
        <select
          value={selectedCountry}
          onChange={e => setSelectedCountry(e.target.value)}
          placeholder="Select a country"
        >
          <option value="">Select a country</option>
          {countries.map(country => (
            <option key={country.id} value={country.id}>{country.name}</option>
          ))}
        </select>
        <select
          value={selectedCity}
          onChange={e => setSelectedCity(e.target.value)}
          placeholder="Select a city"
          disabled={!selectedCountry}  // Disable city selection if no country is selected
        >
          <option value="">Select a city</option>
          {cities.map(city => (
            <option key={city.id} value={city.id}>{city.name}</option>
          ))}
        </select>
        <div>
          {restaurants.length > 0 ? (
            <ul>
              {restaurants.map(restaurant => (
                <li key={restaurant.id}>{restaurant.name}</li>
              ))}
            </ul>
          ) : (
            <p>No restaurants found or select a city to see list.</p>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
