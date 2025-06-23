import React, { useState } from 'react';
import { useRouter } from 'expo-router';
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

export default function LoginScreen() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  return (              
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
      style={styles.container}
    >
      <View style={styles.container2}> 
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
          />
          <TextInput
            style={styles.input}
            placeholder="Mot de passe"
            placeholderTextColor="#888"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />

          <TouchableOpacity style={styles.button} onPress={() => router.push('/marquepresence')}>
            <Text style={styles.buttonText}>Connexion</Text>
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
    height: 350,
    resizeMode: 'cover',
    alignItems: 'center',
    justifyContent: 'center',
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
