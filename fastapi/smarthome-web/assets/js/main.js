const dev_mode = true
const base_url = dev_mode ? 'http://localhost:8050/ambientes' : 'https://smarthome-api-c5fj.onrender.com/ambientes'
const url = new URL(window.location.href);
