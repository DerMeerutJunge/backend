const express = require("express");
const fs = require("fs");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.PORT || 3000;

const DB_FILE = "data.json";

// Initialize DB if not exists
if (!fs.existsSync(DB_FILE)) {
  fs.writeFileSync(DB_FILE, JSON.stringify({ waitlist: [], survey: [] }));
}

app.get("/", (req, res) => {
  res.send("OK);
});

// Save waitlist
app.post("/waitlist", (req, res) => {
  const data = JSON.parse(fs.readFileSync(DB_FILE));

  data.waitlist.push({
    ...req.body,
    createdAt: new Date()
  });

  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));

  res.json({ success: true });
});

// Save survey
app.post("/survey", (req, res) => {
  const data = JSON.parse(fs.readFileSync(DB_FILE));

  data.survey.push({
    ...req.body,
    createdAt: new Date()
  });

  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));

  res.json({ success: true });
});

app.get("/admin/data", (req, res) => {
  const key = req.query.key;

  if (key !== process.env.ADMIN_KEY) {
    return res.status(403).json({ error: "Unauthorized" });
  }

  const data = fs.readFileSync(DB_FILE);
  res.setHeader("Content-Type", "application/json");
  res.send(data);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost: {$PORT}`);
});
