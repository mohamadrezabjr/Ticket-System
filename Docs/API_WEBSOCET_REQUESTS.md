# Ticket WebSocket Endpoint

## 🌐 Endpoint URL

```
ws://<your-server>/ws/ticket/<ticket_id>/?token=<JWT_TOKEN>
```

* `<ticket_id>`: ID of the ticket.
* `<JWT_TOKEN>`: JSON Web Token for authentication.
* Supports sending **text messages** (`body`) and **files** (`file`, `filename`) up to 10 MB.

---

## 🔗 Connection Example (JavaScript)

```javascript
const ticketId = 1;
const token = "<YOUR_JWT_TOKEN>";
const socket = new WebSocket(`ws://<your-server>/ws/ticket/${ticketId}/?token=${token}`);

socket.onopen = () => {
    console.log("Connected to ticket channel!");
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received:", data);
};

socket.onclose = () => {
    console.log("Disconnected from WebSocket");
};
```

> ⚠️ Note: The server validates the token via your **JWT authentication middleware**. Unauthorized connections will be rejected.

---

## 💬 Sending Messages

**Request (JSON)**

```json
{
    "body": "Hello, this is a test message",
    "file": "iVBORw0KGgoAAAANSUhEUgAA...",  // Base64 encoded file
    "filename": "example.png"
}
```

**Response (broadcast to all clients in the ticket group)**

```json
{

    "pk": 116,
    "body": "Hello, this is a test message",
    "sender": {
        "id": 3,
        "username": "user3",
        "phone": "09123456789",
        "profile_image": "http://<your-server>/media/profiles/profile.png"
    },
    "file": "http://<your-server>/media/files/ticket_1/example.png",
    "created_at": "2025-10-22T17:32:10Z"
}
```

---



### Rules

1. **At least one of `body` or `file` must be provided**; the other can be empty.
2. `file` must be Base64 encoded.
3. Maximum allowed file size: **10 MB**.

---

## Disconnecting

```javascript
socket.onclose = () => {
    console.log("WebSocket closed");
};
```

* Server may disconnect clients automatically or when the user leaves the ticket.
* Unauthorized connections without a valid token will be rejected.

---

## Notes

1. Only authenticated users with access to the ticket can send or receive messages.
2. All messages are broadcasted to **all users connected to the same ticket**.
3. For large files close to 10 MB, consider using chunked upload or HTTP upload with a WebSocket notification.
