// app/splash.tsx
import React, { useEffect, useRef } from 'react';
import { View, StyleSheet } from 'react-native';
import LottieView from 'lottie-react-native';
import { useRouter } from 'expo-router';

export default function SplashScreen() {
  const animation = useRef<LottieView>(null);
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.replace('/'); // redirige vers la page principale après splash
    }, 5000); // durée avant de rediriger (5 secondes)

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <LottieView
        ref={animation}
        source={require('../assets/animations/test_lottie.json')}
        autoPlay
        loop={false}
        style={styles.animation}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff', // ou ta couleur principale
    justifyContent: 'center',
    alignItems: 'center',
  },
  animation: {
    width: 300,
    height: 300,
  },
});
