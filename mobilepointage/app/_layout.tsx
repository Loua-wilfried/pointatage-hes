


// On utilise le composant Stack d'expo-router pour gérer la navigation entre les écrans
import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack initialRouteName="splash">
      {/* Splash personnalisé affiché en premier au démarrage */}
      <Stack.Screen name="splash" options={{ headerShown: false }} />
      {/* Page principale de l'application, affichée après le splash */}
      <Stack.Screen name="index" options={{ headerShown: false }} />
      {/* Ajoute ici les autres écrans si besoin */}
    </Stack>
  );
}
