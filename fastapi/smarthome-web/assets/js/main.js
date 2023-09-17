const dev_mode = false
const base_url = dev_mode ? 'http://localhost:8050/ambientes' : 'https://smarthome-api-mnq8.onrender.com/ambientes'
const url = new URL(window.location.href);
