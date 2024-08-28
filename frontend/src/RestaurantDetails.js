import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Modal from './components/modal'; // Import the Modal component

function RestaurantDetails() {
  const { restaurantId } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [googleRating, setGoogleRating] = useState(null); // State for Google Rating
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userId, setUserId] = useState('');
  const [comment, setComment] = useState('');
  const [rating, setRating] = useState('');
  const [averageUserRating, setAverageUserRating] = useState(null); // State for average user rating

  useEffect(() => {
    async function fetchData() {
      try {
        const restaurantData = await fetch(`http://localhost:5000/api/v1/restaurants/${restaurantId}`).then(res => res.json());
        const reviewsData = await fetch(`http://localhost:5000/api/v1/restaurants/${restaurantId}/userreviews`).then(res => res.json());

        // Calculate the average user rating
        if (reviewsData.length > 0) {
          const totalRating = reviewsData.reduce((sum, review) => sum + parseFloat(review.rating), 0);
          const averageRating = (totalRating / reviewsData.length).toFixed(2); // Round to 2 decimal places
          setAverageUserRating(averageRating);
        } else {
          setAverageUserRating('No ratings available');
        }

        // Fetch Google rating
        const googleRatingData = await fetch(`http://localhost:5000/place_details?place_name=${restaurantData.name}`).then(res => res.json());
        
        setRestaurant(restaurantData);
        setReviews(reviewsData);
        setGoogleRating(googleRatingData.result?.rating || 'No rating available'); // Set Google Rating
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [restaurantId]);

  const toggleModal = () => setIsModalOpen(!isModalOpen);

  const handleReviewSubmit = async (e) => {
    e.preventDefault();

    // Validate input before sending the request
    if (!userId || !comment || !rating) {
        console.error("All fields are required");
        return;
    }

    if (isNaN(rating) || rating < 0 || rating > 10) {
        console.error("Rating must be a number between 0 and 10");
        return;
    }

    try {
        // Update payload keys to match the backend expectations
        const payload = { user_id: userId, comment, rating };
        
        const response = await fetch(`http://localhost:5000/api/v1/restaurants/${restaurantId}/userreviews`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const newReview = await response.json();
            setReviews([...reviews, newReview]);
            setComment('');
            setRating('');
            setUserId('');
            
            // Recalculate average rating if needed
            const updatedReviews = [...reviews, newReview];
            const totalRating = updatedReviews.reduce((sum, review) => sum + parseFloat(review.rating), 0);
            const averageRating = (totalRating / updatedReviews.length).toFixed(2);
            setAverageUserRating(averageRating);
        } else {
            const errorData = await response.json();
            console.error('Failed to post review:', errorData.message || 'Unknown error');
        }
    } catch (err) {
        console.error('Failed to submit review:', err);
    }
};

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <button onClick={toggleModal}>Show Details</button>
      <Modal isOpen={isModalOpen} close={toggleModal}>
        <h1>{restaurant?.name}</h1>
        <p>City ID: {restaurant?.city_id}</p>
        <p>Average User Rating: {averageUserRating}</p> {/* Display average user rating */}
        <p>Google Rating: {googleRating*2}</p> {/* Display Google Rating */}
        <h2>Reviews</h2>
        {reviews.length > 0 ? (
          <ul>
            {reviews.map(review => (
              <li key={review.id}>
                <p>{review.comment}</p>
                <p>Rating: {review.rating}</p>
                <p>Date: {new Date(review.date).toLocaleDateString()}</p>
              </li>
            ))}
          </ul>
        ) : <p>No reviews available.</p>}
        <form onSubmit={handleReviewSubmit}>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="User ID"
            required
          />
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Comment"
            required
          />
          <input
            type="number"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            placeholder="Rating"
            required
          />
          <button type="submit">Add Review</button>
        </form>
      </Modal>
    </div>
  );
}

export default RestaurantDetails;
