def test_get_bookings_empty(client):
    response = client.get("/api/bookings")

    assert response.status_code == 200
    assert response.json() == []


def test_create_booking(client):
    booking = {
        "customer_name": "Rahul",
        "destination": "Manali",
        "travel_date": "2026-12-25",
        "number_of_people": 3,
        "status": "confirmed",
    }

    response = client.post("/api/bookings", json=booking)

    assert response.status_code == 201

    data = response.json()

    assert data["customer_name"] == "Rahul"
    assert data["destination"] == "Manali"
    assert data["number_of_people"] == 3
    assert data["status"] == "confirmed"
    assert "id" in data
    assert "created_at" in data


def test_get_booking_by_id(client):
    booking = {
        "customer_name": "Priya",
        "destination": "Kerala",
        "travel_date": "2027-01-10",
        "number_of_people": 2,
        "status": "confirmed",
    }

    create_response = client.post("/api/bookings", json=booking)
    booking_id = create_response.json()["id"]

    response = client.get(f"/api/bookings/{booking_id}")

    assert response.status_code == 200
    assert response.json()["id"] == booking_id
    assert response.json()["destination"] == "Kerala"


def test_update_booking(client):
    booking = {
        "customer_name": "Arjun",
        "destination": "Jaipur",
        "travel_date": "2027-02-15",
        "number_of_people": 2,
        "status": "pending",
    }

    create_response = client.post("/api/bookings", json=booking)
    booking_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/bookings/{booking_id}",
        json={
            "destination": "Udaipur",
            "status": "confirmed",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["destination"] == "Udaipur"
    assert data["status"] == "confirmed"
    assert data["customer_name"] == "Arjun"


def test_delete_booking(client):
    booking = {
        "customer_name": "Neha",
        "destination": "Goa",
        "travel_date": "2027-03-20",
        "number_of_people": 2,
        "status": "confirmed",
    }

    create_response = client.post("/api/bookings", json=booking)
    booking_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/bookings/{booking_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/bookings/{booking_id}")

    assert get_response.status_code == 404