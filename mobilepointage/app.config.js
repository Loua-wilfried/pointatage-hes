import 'dotenv/config';

export default ({ config }) => ({
  ...config,
  name: "mobilepointage",
  slug: "mobilepointage",
  version: "1.0.0",
  extra: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://172.24.1.195:8000',
  },
});
