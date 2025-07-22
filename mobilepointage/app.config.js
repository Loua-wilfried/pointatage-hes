import 'dotenv/config';

export default ({ config }) => ({
  ...config,
  name: "mobilepointage",
  slug: "mobilepointage",
  version: "1.0.0",
  extra: {
    // Configuration pour serveur Django local
    // Utilisation de l'adresse IP réelle de la machine (172.24.1.195)
    // Accessible depuis émulateur et device physique
    API_BASE_URL: process.env.API_BASE_URL || 'http://172.24.1.195:8000',
  },
});
