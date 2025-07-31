import 'dotenv/config';

export default ({ config }) => ({
  ...config,
  name: "mobilepointage",
  slug: "mobilepointage",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/icon.png",
  userInterfaceStyle: "light",
  splash: {
    image: "./assets/splash.png",
    resizeMode: "contain",
    backgroundColor: "#ffffff"
  },
  assetBundlePatterns: [
    "**/*"
  ],
  ios: {
    supportsTablet: true
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#ffffff"
    },
    package: "com.carmel38.mobilepointage"
  },
  web: {
    favicon: "./assets/favicon.png"
  },
  extra: {
    // Configuration pour serveur Django local
    // Utilisation de l'adresse IP réelle de la machine (192.168.37.185)
    // Accessible depuis émulateur et device physique
    API_BASE_URL: process.env.API_BASE_URL || 'http://192.168.37.185:8000',
    eas: {
      projectId: "c529b4ca-f4dc-4695-a759-805efb39a317"
    }
  },
});
