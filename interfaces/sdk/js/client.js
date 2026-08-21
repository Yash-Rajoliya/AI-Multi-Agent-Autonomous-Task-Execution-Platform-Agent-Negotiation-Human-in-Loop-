const axios = require("axios");

class AIClient {
  constructor(baseUrl, apiKey = null) {
    this.baseUrl = baseUrl;
    this.headers = apiKey ? { Authorization: `Bearer ${apiKey}` } : {};
  }

  async createTask(payload) {
    const res = await axios.post(
      `${this.baseUrl}/v1/tasks`,
      payload,
      { headers: this.headers }
    );
    return res.data;
  }

  async runWorkflow(payload) {
    const res = await axios.post(
      `${this.baseUrl}/v1/workflows/run`,
      payload,
      { headers: this.headers }
    );
    return res.data;
  }
}

module.exports = { AIClient };