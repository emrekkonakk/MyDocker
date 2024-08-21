import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Modal from './components/modal'; // Import the Modal component

function RestaurantDetails() {
  const { restaurantId } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userId, setUserId] = useState('');
  const [comment, setComment] = useState('');
  const [rating, setRating] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const restaurantData = await fetch(`http://localhost:5000/api/v1/restaurants/${restaurantId}`).then(res => res.json());
        const reviewsData = await fetch(`http://localhost:5000/api/v1/restaurants/${restaurantId}/userreviews`).then(res => res.json());

        setRestaurant(restaurantData);
        setReviews(reviewsData);
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
    try {
      const payload = { userId, comment, rating };
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
      } else {
        throw new Error('Failed to post review');
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
        <p>User Rating: {restaurant?.userrating || 'Not Rated'}</p>
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
