const { URLSearchParams } = require('url');

function build_recommendations(profile) {
  const subject = profile.subject || 'General Learning';
  const level = profile.level || 'Beginner';
  const style = profile.learning_style || 'Visual';
  const minutes_per_day = Number(profile.minutes_per_day || 60);

  const style_content_map = {
    Visual: 'Watch a concise concept video and create a mind map',
    'Reading/Writing': 'Read a chapter and summarize key points',
    Auditory: 'Listen to a lesson and explain concepts aloud',
    Kinesthetic: 'Build a mini exercise or hands-on example',
  };
  const study_method = style_content_map[style] || style_content_map['Visual'];

  const session_blocks = Math.max(1, Math.floor(minutes_per_day / 25));
  const topics = [
    `${subject} fundamentals`,
    `${subject} intermediate problem solving`,
    `${subject} real-world application project`,
  ];

  return topics.map((topic, i) => {
    const params = new URLSearchParams({ search_query: `${subject} ${topic}` });
    const video_search_url = `https://www.youtube.com/results?${params.toString()}`;
    return {
      day: `Day ${i + 1}`,
      focus: topic,
      level,
      recommended_activity: study_method,
      time_block_minutes: 25,
      blocks: session_blocks,
      video_search_url,
    };
  });
}

module.exports = (req, res) => {
  const profile = req.method === 'POST' ? req.body : {};
  if (!profile || Object.keys(profile).length === 0) {
    res.status(400).json({ error: 'Profile data is required' });
    return;
  }

  const response = {
    learner: profile.name || 'Learner',
    goal: profile.goal || 'Improve learning outcomes',
    recommendations: build_recommendations(profile),
  };

  res.status(200).json(response);
};
