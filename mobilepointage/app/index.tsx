import * as SecureStore from 'expo-secure-store';
import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import Constants from 'expo-constants';
import { useNavigation } from 'expo-router';
import { useLayoutEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';

const API_BASE_URL = Constants.expoConfig?.extra?.API_BASE_URL || '';

async function logout(router: any) {
  await SecureStore.deleteItemAsync('employe_id');
  await SecureStore.deleteItemAsync('token');
  router.replace('/');
}

export default function LoginScreen() {
  const router = useRouter();
  const navigation = useNavigation();
  useLayoutEffect(() => {
    navigation.setOptions({
      headerShown: true,
      title: "",
      headerStyle: {
        backgroundColor: '#F0874E',      // Couleur de fond du header
        shadowColor: '#fff',             // Couleur de l'ombre (iOS)
        shadowOffset: { height: 4 },     // Décalage vertical de l'ombre (iOS)
        shadowOpacity: 1,                // Opacité de l'ombre (iOS)
        shadowRadius: 8,                 // Flou de l'ombre (iOS)
        elevation: 10,                   // Ombre portée (Android)
        borderBottomWidth: 0,  
        borderBottomColor: "transparent",          // Masque la bordure du bas (iOS)
      },
      headerTitleStyle: { color: '#fff', fontWeight: 'bold', fontSize: 22 },
      headerTintColor: '#fff',
      headerTitleAlign: 'center',
    });
  }, [navigation]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');


  const handleLogin = async () => {
    setError('');
    if (!username.trim() || !password.trim()) {
      setError("Nom d'utilisateur et mot de passe obligatoires.");
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const text = await response.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        setError("Erreur inattendue côté serveur : " + text.slice(0, 100));
        setLoading(false);
        return;
      }

      if (response.ok && data.access) {
        await SecureStore.setItemAsync('token', data.access);
        const token = data.access;
        const meResponse = await fetch(`${API_BASE_URL}/api/pointages/employe/me/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const meData = await meResponse.json();

        if (meResponse.ok && meData.id) {
          await SecureStore.setItemAsync('employe_id', String(meData.id));
          router.push('/marquepresence');
        } else {
          setError("Impossible de récupérer l'identifiant employé.");
          await logout(router);
        }
      } else {
        setError(data?.detail || data?.non_field_errors?.[0] || 'Identifiants invalides');
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erreur réseau inconnue.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 60 : 0}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.container2}>
          {/* Affichage de l'URL d'API pour debug */}
          <Text style={styles.apiText}>API: {API_BASE_URL}</Text>

          {/* Image en pleine largeur */}
          <Image 
            source={require('../assets/images/font2.png')} 
            style={styles.logo} 
          />
        </View>

        <View style={styles.container1}>
          <View style={styles.formContainer}>
            <Text style={styles.title}>
              Bienvenue 👋 sur notre application de pointage
            </Text>

            {/* Champ Nom d'utilisateur */}
            <TextInput
              style={styles.input}
              placeholder="Nom d'utilisateur"
              placeholderTextColor="#888"
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />


            {/* Champ Mot de passe */}
            <TextInput
              style={styles.input}
              placeholder="Mot de passe"
              placeholderTextColor="#888"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />

            {/* Message d'erreur */}
            {error ? <Text style={styles.errorText}>{error}</Text> : null}

            {/* Bouton Connexion */}
            <TouchableOpacity
              style={[styles.button, (!username.trim() || !password.trim() || loading) && {opacity: 0.5}]}
              onPress={handleLogin}
              disabled={!username.trim() || !password.trim() || loading}
            >
              <Text style={styles.buttonText}>
                {loading ? 'Connexion...' : 'Connexion'}
              </Text>
            </TouchableOpacity>

            {/* Bouton Déconnexion caché mais fonctionnel */}
            <TouchableOpacity
              style={[styles.button, styles.hiddenButton]}
              onPress={() => logout(router)}
            >
              <Text style={styles.buttonText}>Déconnexion</Text>
            </TouchableOpacity>

            {/* Lien Création de compte */}
            <TouchableOpacity onPress={() => router.push('/creationcompte')}>
              <Text style={styles.link}>Créer un compte</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'flex-end',
    //position: 'relative'
  },
  container2: {
    backgroundColor: '#fff',
  },
  logo: {
    width: '100%',       // ➤ prend toute la largeur
    height: 350,
    resizeMode: 'cover', // ➤ couvre la largeur sans déformation
    bottom: 70,
  },
  apiText: {
    color: 'black',
    fontSize: 12,
    marginBottom: 8,
    textAlign: 'center',
    zIndex: 1000,
    position: 'relative',
    bottom: -650,
    right: 100,
    
  },
  container1: {
    width: '100%',
    backgroundColor: '#fff',
    position: 'relative',
    top: -70,
  },
  formContainer: {
    padding: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  input: {
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
    paddingVertical: 14,
    paddingHorizontal: 16,
    marginBottom: 16,
    fontSize: 16,
  },
  errorText: {
    color: 'red',
    marginBottom: 8,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#F0874E',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    marginBottom: 16,
  },
  hiddenButton: {
    opacity: 0,
    height: 0,
    marginBottom: 0,
    paddingVertical: 0,
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  link: {
    textAlign: 'center',
    color: '#F0874E',
    fontSize: 14,
    marginTop: 4,
  },
});
