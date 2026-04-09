// Simple health endpoint for Vercel Serverless Function
module.exports = (req, res) => {
  res.status(200).json({ status: 'ok', service: 'personalized-learning-api' });
};
