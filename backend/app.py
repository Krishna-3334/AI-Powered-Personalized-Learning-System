from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path


app = Flask(__name__)
CORS(app)

# Resolve frontend directory (sibling folder to backend)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@app.get("/")
def serve_index():
    """Serve the frontend index.html at the root so visiting / won't 404."""
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.get("/<path:filename>")
def serve_static(filename: str):
    """Serve static frontend assets (js, css, images) from the frontend folder."""
    return send_from_directory(str(FRONTEND_DIR), filename)


def build_recommendations(profile: dict) -> list[dict]:
    subject = profile.get("subject", "General Learning")
    level = profile.get("level", "Beginner")
    style = profile.get("learning_style", "Visual")
    minutes_per_day = int(profile.get("minutes_per_day", 60))

    # Lightweight recommendation logic to keep this starter project fast and runnable.
    style_content_map = {
        "Visual": "Watch a concise concept video and create a mind map",
        "Reading/Writing": "Read a chapter and summarize key points",
        "Auditory": "Listen to a lesson and explain concepts aloud",
        "Kinesthetic": "Build a mini exercise or hands-on example",
    }
    study_method = style_content_map.get(style, style_content_map["Visual"])

    session_blocks = max(1, minutes_per_day // 25)
    topics = [
        f"{subject} fundamentals",
        f"{subject} intermediate problem solving",
        f"{subject} real-world application project",
    ]

    plan = []
    for i, topic in enumerate(topics, start=1):
        # Provide a YouTube search URL for the topic so the frontend can
        # show related videos. Using a search URL avoids requiring an API
        # key or hard-coded video IDs while still surfacing relevant content.
        from urllib.parse import quote_plus

        query = quote_plus(f"{subject} {topic}")
        video_search_url = f"https://www.youtube.com/results?search_query={query}"

        plan.append(
            {
                "day": f"Day {i}",
                "focus": topic,
                "level": level,
                "recommended_activity": study_method,
                "time_block_minutes": 25,
                "blocks": session_blocks,
                "video_search_url": video_search_url,
            }
        )
    return plan


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "personalized-learning-api"})


@app.post("/api/recommend")
def recommend():
    profile = request.get_json(silent=True) or {}
    if not profile:
        return jsonify({"error": "Profile data is required"}), 400

    response = {
        "learner": profile.get("name", "Learner"),
        "goal": profile.get("goal", "Improve learning outcomes"),
        "recommendations": build_recommendations(profile),
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
