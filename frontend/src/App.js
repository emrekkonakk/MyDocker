import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import RestaurantDetails from './RestaurantDetails';
import './App.css';


function App() {
  const [countries, setCountries] = useState([]);
  const [cities, setCities] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [restaurants, setRestaurants] = useState([]);
  const [sortType, setSortType] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');
  const [newRestaurantName, setNewRestaurantName] = useState('');

  useEffect(() => {
    fetch(`http://localhost:5000/api/v1/countries`)
      .then(response => response.json())
      .then(data => setCountries(data))
      .catch(error => console.error('Failed to fetch countries', error));
  }, []);

  useEffect(() => {
    if (selectedCountry) {
      fetch(`http://localhost:5000/api/v1/countries/${selectedCountry}/cities`)
        .then(response => response.json())
        .then(data => {
          setCities(data);
          setSelectedCity('');
          setRestaurants([]);
        })
        .catch(error => console.error('Failed to fetch cities', error));
    } else {
      setCities([]);
      setSelectedCity('');
      setRestaurants([]);
    }
  }, [selectedCountry]);

  useEffect(() => {
    if (selectedCity) {
      fetch(`http://localhost:5000/api/v1/cities/${selectedCity}/restaurants?sort=${sortOrder}&type=${sortType}`)
        .then(response => response.json())
        .then(data => {
          console.log('Restaurants:', data);
          setRestaurants(data);
        })
        .catch(error => console.error('Failed to fetch restaurants', error));
    } else {
      setRestaurants([]);
    }
  }, [selectedCity, sortOrder, sortType]);

  const handleAddRestaurant = async () => {
    if (!newRestaurantName.trim()) {
      alert('Please enter a restaurant name.');
      return;
    }
    try {
      const response = await fetch(`http://localhost:5000/api/v1/cities/${selectedCity}/restaurants`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newRestaurantName })
      });
      if (response.ok) {
        const addedRestaurant = await response.json();
        setRestaurants([...restaurants, addedRestaurant]);
        setNewRestaurantName('');
      } else {
        console.error('Failed to add restaurant');
      }
    } catch (error) {
      console.error('Error adding restaurant:', error);
    }
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <select value={selectedCountry} onChange={e => setSelectedCountry(e.target.value)}>
            <option value="">Select a country</option>
            {countries.map(country => <option key={country.id} value={country.id}>{country.name}</option>)}
          </select>
          <select value={selectedCity} onChange={e => setSelectedCity(e.target.value)} disabled={!selectedCountry}>
            <option value="">Select a city</option>
            {cities.map(city => <option key={city.id} value={city.id}>{city.name}</option>)}
          </select>
          <select value={sortType} onChange={e => setSortType(e.target.value)}>
            <option value="name">Sort by Name</option>
            <option value="rating">Sort by Rating</option>
          </select>
          <select value={sortOrder} onChange={e => setSortOrder(e.target.value)}>
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
          {selectedCity && (
            <>
              <input
                type="text"
                placeholder="New restaurant name"
                value={newRestaurantName}
                onChange={e => setNewRestaurantName(e.target.value)}
              />
              <button onClick={handleAddRestaurant}>Add Restaurant</button>
            </>
          )}
          {restaurants.length ? (
            <ul>
              {restaurants.map(restaurant => (
                <li key={restaurant.id}>
                  <Link to={`/restaurants/${restaurant.id}`}>
                    {restaurant.name} - {restaurant.userrating || 'Not Rated'}
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p>No restaurants found or selected.</p>
          )}
        </header>
        <Routes>
          <Route path="/restaurants/:restaurantId" element={<RestaurantDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
