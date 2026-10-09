import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    customer_name: "",
    destination: "",
    travel_date: "",
    number_of_people: 1,
    status: "confirmed",
  });

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/bookings`);

      if (!response.ok) {
        throw new Error("Unable to load bookings");
      }

      const data = await response.json();
      setBookings(data);
      setError("");
    } catch (err) {
      setError("Backend is unavailable. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]:
        name === "number_of_people" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(`${API_URL}/api/bookings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        throw new Error("Unable to create booking");
      }

      setForm({
        customer_name: "",
        destination: "",
        travel_date: "",
        number_of_people: 1,
        status: "confirmed",
      });

      await fetchBookings();
    } catch (err) {
      setError("Could not create the booking. Please try again.");
    }
  };

  const deleteBooking = async (id) => {
    try {
      const response = await fetch(`${API_URL}/api/bookings/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Unable to delete booking");
      }

      await fetchBookings();
    } catch (err) {
      setError("Could not delete the booking.");
    }
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <h1>Adizz</h1>
            <span>Travel & Booking</span>
          </div>
        </div>

        <div className="nav-status">
          <span className="status-dot"></span>
          API Connected
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <p className="eyebrow">TRAVEL MANAGEMENT</p>
            <h2>Plan your next journey.</h2>
            <p className="hero-text">
              Manage your travel bookings from one simple dashboard.
            </p>
          </div>

          <div className="hero-card">
            <span>Total Bookings</span>
            <strong>{bookings.length}</strong>
          </div>
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <div>
                <p className="section-label">NEW BOOKING</p>
                <h3>Create a booking</h3>
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              <label>
                Customer name
                <input
                  name="customer_name"
                  value={form.customer_name}
                  onChange={handleChange}
                  placeholder="Enter customer name"
                  required
                />
              </label>

              <label>
                Destination
                <input
                  name="destination"
                  value={form.destination}
                  onChange={handleChange}
                  placeholder="e.g. Goa"
                  required
                />
              </label>

              <div className="form-row">
                <label>
                  Travel date
                  <input
                    type="date"
                    name="travel_date"
                    value={form.travel_date}
                    onChange={handleChange}
                    required
                  />
                </label>

                <label>
                  People
                  <input
                    type="number"
                    name="number_of_people"
                    min="1"
                    max="20"
                    value={form.number_of_people}
                    onChange={handleChange}
                    required
                  />
                </label>
              </div>

              <label>
                Status
                <select
                  name="status"
                  value={form.status}
                  onChange={handleChange}
                >
                  <option value="confirmed">Confirmed</option>
                  <option value="pending">Pending</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </label>

              <button type="submit">Create Booking</button>
            </form>
          </div>

          <div className="panel bookings-panel">
            <div className="panel-header">
              <div>
                <p className="section-label">YOUR TRIPS</p>
                <h3>Recent bookings</h3>
              </div>

              <button
                className="refresh-button"
                onClick={fetchBookings}
                type="button"
              >
                Refresh
              </button>
            </div>

            {error && <div className="error">{error}</div>}

            {loading ? (
              <div className="empty-state">Loading bookings...</div>
            ) : bookings.length === 0 ? (
              <div className="empty-state">
                <strong>No bookings yet</strong>
                <span>Create your first trip using the form.</span>
              </div>
            ) : (
              <div className="booking-list">
                {bookings.map((booking) => (
                  <article className="booking-card" key={booking.id}>
                    <div className="booking-main">
                      <div className="destination-icon">
                        {booking.destination.charAt(0).toUpperCase()}
                      </div>

                      <div>
                        <h4>{booking.destination}</h4>
                        <p>{booking.customer_name}</p>
                      </div>
                    </div>

                    <div className="booking-details">
                      <span>
                        {new Date(booking.travel_date).toLocaleDateString(
                          "en-IN",
                          {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                          }
                        )}
                      </span>
                      <span>{booking.number_of_people} people</span>
                      <span className={`badge ${booking.status}`}>
                        {booking.status}
                      </span>

                      <button
                        className="delete-button"
                        onClick={() => deleteBooking(booking.id)}
                        type="button"
                      >
                        Delete
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;