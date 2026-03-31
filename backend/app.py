from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


app = Flask(__name__)

FRONTEND_DIR = (Path(__file__).resolve().parent / ".." / "frontend").resolve()


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
        plan.append(
            {
                "day": f"Day {i}",
                "focus": topic,
                "level": level,
                "recommended_activity": study_method,
                "time_block_minutes": 25,
                "blocks": session_blocks,
            }
        )
    return plan


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "personalized-learning-api"})


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/<path:filename>")
def static_files(filename: str):
    return send_from_directory(FRONTEND_DIR, filename)


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
