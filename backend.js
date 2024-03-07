import express from 'express';
import mysql2 from 'mysql2';
import cors from 'cors';

const app = express();
const port = 5000;

app.use(express.json());
app.use(cors());


// Define API routes for each database here
app.post('/get-user-data', (req, res) => {
    
});

// Start the Express.js server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});