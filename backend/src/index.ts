import cors from "cors";
import "dotenv/config";
import express from "express";

const app = express();
const port = Number(process.env.PORT) || 4000;
const appOrigin =
  process.env.APP_URL ??
  "https://animated-space-doodle-jgx9prvx9rrc5pwx-3001.app.github.dev";

app.use(
  cors({
    origin: appOrigin,
    credentials: true,
  }),
);

app.use(express.json());

app.get("/health", (_req, res) => {
  try {
    res.json({ status: "ok", service: "meetpilot-app" });
  } catch {
    res.status(500).json({
      success: false,
      message: "Internal server error",
    });
  }
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Backend running on http://localhost:${port}`);
});
