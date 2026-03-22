const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

// Middleware
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Set view engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Hardcoded sample data
let posts = [
  {
    id: 1,
    title: "Welcome to Our App",
    content: "This is a sample post created with hardcoded data.",
    author: "Admin",
    date: new Date("2026-03-15"),
  },
  {
    id: 2,
    title: "How to Use This App",
    content:
      "Simply type your message in the input field below and click Post Message to add a new post.",
    author: "User",
    date: new Date("2026-03-18"),
  },
  {
    id: 3,
    title: "Express & EJS Example",
    content: "This is a simple web application built with Express and EJS.",
    author: "Developer",
    date: new Date("2026-03-20"),
  },
];

let nextId = 4;

// Routes
app.get("/", (req, res) => {
  res.render("index", { posts });
});

app.post("/post", (req, res) => {
  const { title, content, author } = req.body;

  if (title && content && author) {
    posts.push({
      id: nextId++,
      title,
      content,
      author,
      date: new Date(),
    });
  }

  res.redirect("/");
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
