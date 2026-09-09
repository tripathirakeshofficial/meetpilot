import cors from "cors";
import "dotenv/config";
import express from "express";
import { getPool } from "./db/pool.js";

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

app.get("/health", async (_req, res) => {
  try {
    await getPool().query("SELECT 1");
    res.json({ status: "ok", service: "meetpilot-app", database: "up" });
  } catch {
    res.status(503).json({
      status: "error",
      service: "meetpilot-app",
      database: "down",
    });
  }
});

app.listen(port, "0.0.0.0", () => {
  console.log(`Backend running on http://localhost:${port}`);
});
