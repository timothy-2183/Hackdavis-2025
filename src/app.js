const express = require('express');
const itemRoutes = require('./routes/itemRoutes');
require('dotenv').config();

const app = express();

app.use(express.json());

// Routes
app.use('/api/items', itemRoutes);

app.get('/', (req, res) => {
  res.send('Welcome to the Express API!');
});

module.exports = app;
