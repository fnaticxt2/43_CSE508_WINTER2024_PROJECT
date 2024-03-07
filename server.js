// server.js
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const path = require("path");
const fs = require("fs"); // Add the 'fs' module for file system operations

const app = express();
const port = 3001;

app.use(cors()); // Enable CORS

// Set up storage for uploaded files
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDirectory = path.resolve(__dirname, "uploads");

    // Ensure the 'uploads' directory exists or create it
    if (!fs.existsSync(uploadDirectory)) {
      fs.mkdirSync(uploadDirectory);
    }

    cb(null, uploadDirectory);
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + "-" + Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage });

// Handle file upload
app.post("/upload", upload.single("resume"), (req, res) => {
  try {
    if (!req.file) {
      throw new Error("No file uploaded.");
    }

    const filePath = path.resolve(__dirname, req.file.path);
    console.log("Resume uploaded:", filePath);

    // Process the uploaded file as needed
    // For example, you can save the file path to a database

    res.json({ success: true, filePath });
  } catch (error) {
    console.error("Error handling file upload:", error.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
