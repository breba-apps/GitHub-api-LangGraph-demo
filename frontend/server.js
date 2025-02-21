const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, '')));

app.get('/', async (req, res) => {
  try {
    const response = await fetch('http://localhost:5001/data');
    if (!response.ok) {
      // If the response isn't OK, forward the status and an error message.
      return res.status(response.status).send('Error fetching data');
    }
    const data = await response.text();
    res.send(data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
