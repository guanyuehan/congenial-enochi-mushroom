const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;
const REMOTE_DB_URL = "http://localhost:5000";

// Middleware
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Set view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Routes
app.get("/", async (req, res) => {
  try {
    // Fetch posts from the remote DB server
    const response = await fetch(`${REMOTE_DB_URL}/api/posts`);
    const posts = await response.json();
    res.render("index", { posts });
  } catch (error) {
    console.error("Error fetching posts from remote DB:", error.message);
    // Render with empty posts if the remote DB is unavailable
    res.render("index", { posts: [] });
  }
});

app.post("/post", async (req, res) => {
  const { content } = req.body;

  if (content) {
    try {
      // Send the post to the remote DB server
      await fetch(`${REMOTE_DB_URL}/api/posts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });
    } catch (error) {
      console.error("Error creating post in remote DB:", error.message);
    }
  }

  res.redirect("/");
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server is running on http://localhost:${PORT}`);
  console.log(`Make sure the remote DB server is running on ${REMOTE_DB_URL}`);
});
