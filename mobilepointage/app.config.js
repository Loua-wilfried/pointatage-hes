// Configuration Expo pour injecter la variable d'environnement API_BASE_URL
export default ({ config }) => ({
  ...config,
  extra: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://172.24.1.195:8000',
  },
});
