import * as SecureStore from 'expo-secure-store';
import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import Constants from 'expo-constants';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  KeyboardAvoidingView,
  Platform
} from 'react-native';

const API_BASE_URL = Constants.expoConfig.extra.API_BASE_URL;

async function logout(router: any) {
  await SecureStore.deleteItemAsync('employe_id');
  await SecureStore.deleteItemAsync('token');
  router.replace('/');
}

export default function LoginScreen() {
  const router = useRouter();
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
        // Ici tu peux stocker le token si besoin
        // Récupérer l'employe_id de l'utilisateur connecté
        try {
          if (data.access) {
            // Toujours stocker le token JWT sous la clé 'token'
            await SecureStore.setItemAsync('token', data.access);
          }
          const token = data.access;
          const meResponse = await fetch(`${API_BASE_URL}/api/pointages/employe/me/`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          const meData = await meResponse.json();
          if (meResponse.ok && meData.id) {
            await SecureStore.setItemAsync('employe_id', String(meData.id));
            router.push('/marquepresence');
          } else {
            setError("Impossible de récupérer l'identifiant employé. Contactez l'administrateur.");
            await SecureStore.deleteItemAsync('employe_id');
            await SecureStore.deleteItemAsync('token');
            return;
          }
        } catch (e) {
          setError("Erreur lors de la récupération de l'identifiant employé. Veuillez réessayer.");
          await SecureStore.deleteItemAsync('employe_id');
          await SecureStore.deleteItemAsync('token');
          return;
        }
      } else {
        setError(data?.detail || data?.non_field_errors?.[0] || 'Identifiants invalides');
      }
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError('Erreur réseau inconnue.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (              
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
      style={styles.container}
    >
      <View style={styles.container2}> 
        {/* Affichage de l'URL d'API utilisée pour diagnostic */}
        <Text style={{ color: 'blue', fontSize: 12, marginBottom: 8 }}>
          API: {API_BASE_URL}
        </Text>
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
          <TextInput
            style={styles.input}
            placeholder="Nom d'utilisateur"
            placeholderTextColor="#888"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Mot de passe"
            placeholderTextColor="#888"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />

          {error ? <Text style={{color: 'red', marginBottom: 8, textAlign: 'center'}}>{error}</Text> : null}

          <TouchableOpacity
            style={[styles.button, (!username.trim() || !password.trim() || loading) && {opacity: 0.5}]}
            onPress={handleLogin}
            disabled={!username.trim() || !password.trim() || loading}
          >
            <Text style={styles.buttonText}>{loading ? 'Connexion...' : 'Connexion'}</Text>
          </TouchableOpacity>

          <TouchableOpacity style={[styles.button, {backgroundColor:'#f87171', marginTop:12}]} onPress={() => logout(router)}>
            <Text style={styles.buttonText}>Déconnexion</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => router.push('/creationcompte')}>
            <Text style={styles.link}>Créer un compte</Text>
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  container2: {
    backgroundColor: '#fff',
  },
  logo: {
    width: '100%',
    height: 300,
    resizeMode: 'contain',
    marginTop: 60,
  },
  container1: {
    flex: 1,
    width: '100%',
    backgroundColor: '#fff',
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
  button: {
    backgroundColor: '#F0874E',
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: 'center',
    marginBottom: 16,
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
