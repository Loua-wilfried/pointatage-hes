import React, { useState, useEffect, useLayoutEffect } from 'react';
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
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import DropDownPicker from 'react-native-dropdown-picker';
import * as SecureStore from 'expo-secure-store';
import { useNavigation } from 'expo-router';
import { NavigationProp } from '@react-navigation/native';

const API_BASE_URL = Constants.expoConfig?.extra?.API_BASE_URL || 'http://10.0.2.2:8000';

export default function CreationCompte() {
  const [nom, setNom] = useState('');
  const [username, setUsername] = useState('');
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  const [checkingUsername, setCheckingUsername] = useState(false);
  const [telephone, setTelephone] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({
    agence: '',
    nom: '',
    username: '',
    telephone: '',
    email: '',
    password: '',
    confirmPassword: '',
    fonction: '',
  });
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
        borderBottomWidth: 0,            // Masque la bordure du bas (iOS)
        borderBottomColor: "transparent", // Bordure du bas invisible
      },
      headerTitleStyle: { color: '#fff', fontWeight: 'bold', fontSize: 22 },
      headerTintColor: '#fff',
      headerTitleAlign: 'center',
    });
  }, [navigation]);

  // Types pour les dropdowns
  type DropdownItem = { label: string; value: string };

  // Picker pour la fonction
  const [openFonction, setOpenFonction] = useState(false);
  const [fonction, setFonction] = useState(null);
  const [itemsFonction, setItemsFonction] = useState<DropdownItem[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(true);

  // Picker pour l'agence
  const [openAgence, setOpenAgence] = useState(false);
  const [agence, setAgence] = useState(null);
  const [itemsAgence, setItemsAgence] = useState<DropdownItem[]>([]);
  const [loadingAgences, setLoadingAgences] = useState(true);

  // Récupération dynamique des rôles depuis l'API
  const fetchRoles = async () => {
    try {
      setLoadingRoles(true);
      console.log('🔍 Tentative de récupération des rôles depuis:', `${API_BASE_URL}/api/roles/`);
      const response = await fetch(`${API_BASE_URL}/api/roles/`);
      console.log('📡 Réponse API rôles:', response.status, response.statusText);
      if (response.ok) {
        const roles = await response.json();
        console.log('✅ Rôles récupérés:', roles.length, 'rôles');
        const formattedRoles = roles.map((role: any) => ({
          label: role.label,
          value: role.value
        }));
        setItemsFonction(formattedRoles);
        console.log('📝 Rôles formatés pour dropdown:', formattedRoles);
      } else {
        console.error('Erreur lors de la récupération des rôles:', response.status);
        // Fallback vers les données statiques en cas d'erreur
        setItemsFonction([
          { label: 'Directeur Général', value: 'Directeur Général' },
          { label: 'Responsable Informatique', value: 'Responsable Informatique' },
          { label: 'Secrétaire', value: 'Secrétaire' },
          { label: 'Comptable', value: 'Comptable' },
          { label: 'Agent Guichet', value: 'Agent Guichet' },
        ]);
      }
    } catch (error) {
      console.error('Erreur réseau lors de la récupération des rôles:', error);
      // Fallback vers les données statiques
      setItemsFonction([
        { label: 'Directeur Général', value: 'Directeur Général' },
        { label: 'Responsable Informatique', value: 'Responsable Informatique' },
        { label: 'Secrétaire', value: 'Secrétaire' },
        { label: 'Comptable', value: 'Comptable' },
        { label: 'Agent Guichet', value: 'Agent Guichet' },
      ]);
    } finally {
      setLoadingRoles(false);
    }
  };

  // Récupération dynamique des agences depuis l'API
  const fetchAgences = async () => {
    try {
      setLoadingAgences(true);
      console.log('🔍 Tentative de récupération des agences depuis:', `${API_BASE_URL}/api/agences/`);
      const response = await fetch(`${API_BASE_URL}/api/agences/`);
      console.log('📡 Réponse API agences:', response.status, response.statusText);
      if (response.ok) {
        const agences = await response.json();
        const formattedAgences = agences.map((agence: any) => ({
          label: agence.label,
          value: agence.value
        }));
        setItemsAgence(formattedAgences);
      } else {
        console.error('Erreur lors de la récupération des agences:', response.status);
        // Fallback vers les données statiques en cas d'erreur
        setItemsAgence([
          { label: 'Agence Principale', value: 'Agence Principale' },
          { label: 'Agence Secondaire', value: 'Agence Secondaire' },
          { label: 'Agence Régionale Nord', value: 'Agence Régionale Nord' },
          { label: 'Agence Régionale Sud', value: 'Agence Régionale Sud' },
          { label: 'Agence Mobile', value: 'Agence Mobile' },
        ]);
      }
    } catch (error) {
      console.error('Erreur réseau lors de la récupération des agences:', error);
      // Fallback vers les données statiques
      setItemsAgence([
        { label: 'Agence Principale', value: 'Agence Principale' },
        { label: 'Agence Secondaire', value: 'Agence Secondaire' },
        { label: 'Agence Régionale Nord', value: 'Agence Régionale Nord' },
        { label: 'Agence Régionale Sud', value: 'Agence Régionale Sud' },
        { label: 'Agence Mobile', value: 'Agence Mobile' },
      ]);
    } finally {
      setLoadingAgences(false);
    }
  };

  // useEffect pour charger les données au montage du composant
  useEffect(() => {
    fetchRoles();
    fetchAgences();
  }, []);

  const validateNom = (nom: string) => {
    return nom.trim().split(' ').length >= 2;
  };

  const validateEmail = (email: string) => {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string) => {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    return passwordRegex.test(password);
  };

<<<<<<< HEAD
  const validateUsername = (username: string) => {
    const usernameRegex = /^[a-zA-Z0-9_]{3,30}$/;
    return usernameRegex.test(username);
  };

  const validateTelephone = (telephone: string) => {
    const phoneRegex = /^[+]?[0-9]{8,15}$/;
    return phoneRegex.test(telephone.replace(/\s/g, ''));
  };

  // Auto-suggestion du nom d'utilisateur basé sur le nom complet
  const suggestUsername = (nomComplet: string) => {
    const parts = nomComplet.toLowerCase().trim().split(' ');
    if (parts.length >= 2) {
      return parts[0][0] + parts[1]; // "jean dupont" → "jdupont"
    }
    return parts[0] || ''; // "jean" → "jean"
  };

  // Vérification de la disponibilité du nom d'utilisateur
  const checkUsernameAvailability = async (username: string) => {
    if (!username || username.length < 3) {
      setUsernameAvailable(null);
      return;
    }

    setCheckingUsername(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/check-username/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.toLowerCase() }),
      });
      const data = await response.json();
      setUsernameAvailable(data.available);
    } catch (error) {
      console.error('Erreur lors de la vérification du nom d\'utilisateur:', error);
      setUsernameAvailable(null);
    } finally {
      setCheckingUsername(false);
    }
  };

  // Auto-suggestion quand le nom change
  useEffect(() => {
    if (nom.trim() && !username) {
      const suggested = suggestUsername(nom);
      setUsername(suggested);
      if (suggested) {
        checkUsernameAvailability(suggested);
      }
    }
  }, [nom]);

  // Vérification du nom d'utilisateur avec délai
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (username) {
        checkUsernameAvailability(username);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [username]);

  const validateForm = () => {
    let isValid = true;
    const newErrors = {
      agence: '',
      nom: '',
      username: '',
      telephone: '',
      email: '',
      password: '',
      confirmPassword: '',
      fonction: '',
    };

    if (!agence) {
      newErrors.agence = 'Veuillez sélectionner une agence';
      isValid = false;
    }

    if (!nom.trim()) {
      newErrors.nom = 'Le nom complet est requis';
      isValid = false;
    } else if (!validateNom(nom)) {
      newErrors.nom = 'Veuillez entrer votre nom et prénom (au moins 2 mots)';
      isValid = false;
    }
    

    if (!username.trim()) {
      newErrors.username = 'Le nom d\'utilisateur est requis';
      isValid = false;
    } else if (!validateUsername(username)) {
      newErrors.username = 'Le nom d\'utilisateur doit contenir 3-30 caractères (lettres, chiffres, _)';
      isValid = false;
    } else if (usernameAvailable === false) {
      newErrors.username = 'Ce nom d\'utilisateur est déjà pris';
      isValid = false;
    }

    if (!telephone.trim()) {
      newErrors.telephone = 'Le numéro de téléphone est requis';
      isValid = false;
    } else if (!validateTelephone(telephone)) {
      newErrors.telephone = 'Format de téléphone invalide (8-15 chiffres)';
      isValid = false;
    }

    if (!email.trim()) {
      newErrors.email = "L'email est requis";
      isValid = false;
    } else if (!validateEmail(email)) {
      newErrors.email = "Format d'email invalide (exemple: nomprenom@domaine.com)";
      isValid = false;
    }

    if (!password) {
      newErrors.password = 'Le mot de passe est requis';
      isValid = false;
    } else if (!validatePassword(password)) {
      newErrors.password = 'Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule et un chiffre';
      isValid = false;
    }

    if (!confirmPassword) {
      newErrors.confirmPassword = 'Veuillez confirmer votre mot de passe';
      isValid = false;
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Les mots de passe ne correspondent pas';
      isValid = false;
    }

    if (!fonction) {
      newErrors.fonction = 'Veuillez sélectionner une fonction';
      isValid = false;
    }
    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      // Envoi vers API ici si nécessaire
      Alert.alert('Succès', 'Compte créé avec succès', [
        { text: 'OK', onPress: () => router.push('/') },
      ]);
    } catch (error) {
      Alert.alert('Erreur', 'Une erreur est survenue lors de la création du compte. Veuillez réessayer.');
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView
        contentContainerStyle={{ flexGrow: 1 }}
        keyboardShouldPersistTaps="handled"
      >
        <Image source={require('../assets/images/font1.png')} style={styles.logo} />
        <View style={styles.container1}>
          <View style={styles.formContainer}>
            <Text style={styles.title}>Créer un compte</Text>

            {/* Picker pour l'agence */}
            <View style={{ zIndex: 1000, marginBottom: 16 }}>
              <DropDownPicker
                open={openAgence}
                value={agence}
                items={itemsAgence}
                setOpen={setOpenAgence}
                setValue={setAgence}
                setItems={setItemsAgence}
                placeholder="Veuillez sélectionner une agence"
                style={[styles.dropdown, errors.agence ? styles.inputError : null]}
                dropDownContainerStyle={styles.dropdownContainer}
                listMode="SCROLLVIEW"
                onOpen={() => setOpenFonction(false)}
              />
              {errors.agence ? (
                <Text style={styles.errorText}>{errors.agence}</Text>
              ) : null}
            </View>

            <TextInput
              style={[styles.input, errors.nom ? styles.inputError : null]}
              placeholder="Nom complet"
              placeholderTextColor="#888"
              value={nom}
              onChangeText={(text) => {
                setNom(text);
                setErrors({ ...errors, nom: '' });
              }}
              autoCorrect={false}
            />
            {errors.nom ? (
              <Text style={styles.errorText}>{errors.nom}</Text>
            ) : null}

            <TextInput
              style={[styles.input, errors.username ? styles.inputError : null]}
              placeholder="Nom d'utilisateur"
              placeholderTextColor="#888"
              value={username}
              onChangeText={(text) => {
                setUsername(text);
                setErrors({ ...errors, username: '' });
              }}
              autoCorrect={false}
            />
            {errors.username ? (
              <Text style={styles.errorText}>{errors.username}</Text>
            ) : null}
            {usernameAvailable === true ? (
              <Text style={styles.successText}>✓ Nom d'utilisateur disponible</Text>
            ) : null}
            {checkingUsername ? (
              <Text style={styles.infoText}>Vérification...</Text>
            ) : null}

            <TextInput
              style={[styles.input, errors.telephone ? styles.inputError : null]}
              placeholder="Numéro de téléphone"
              placeholderTextColor="#888"
              value={telephone}
              onChangeText={(text) => {
                setTelephone(text);
                setErrors({ ...errors, telephone: '' });
              }}
              keyboardType="phone-pad"
              autoCorrect={false}
            />
            {errors.telephone ? (
              <Text style={styles.errorText}>{errors.telephone}</Text>
            ) : null}

            <TextInput
              style={[styles.input, errors.email ? styles.inputError : null]}
              placeholder="Adresse e-mail professionnelle"
              placeholderTextColor="#888"
              value={email}
              onChangeText={(text) => {
                setEmail(text);
                setErrors({ ...errors, email: '' });
              }}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
            />
            {errors.email ? (
              <Text style={styles.errorText}>{errors.email}</Text>
            ) : null}

            <View style={[styles.passwordContainer, errors.password ? styles.inputError : null]}>
              <TextInput
                style={styles.passwordInput}
                placeholder="Mot de passe"
                placeholderTextColor="#888"
                secureTextEntry={!showPassword}
                value={password}
                onChangeText={(text) => {
                  setPassword(text);
                  setErrors({ ...errors, password: '' });
                }}
                autoCorrect={false}
              />
              <TouchableOpacity
                style={styles.icon}
                onPress={() => setShowPassword(!showPassword)}
              >
                <Ionicons
                  name={showPassword ? 'eye-off' : 'eye'}
                  size={24}
                  color="#888"
                />
              </TouchableOpacity>
            </View>
            {errors.password ? (
              <Text style={styles.errorText}>{errors.password}</Text>
            ) : null}

            <View
              style={[
                styles.passwordContainer,
                errors.confirmPassword ? styles.inputError : null,
                { marginTop: 8 },
              ]}
            >
              <TextInput
                style={styles.passwordInput}
                placeholder="Confirmer le mot de passe"
                placeholderTextColor="#888"
                secureTextEntry={!showPassword}
                value={confirmPassword}
                onChangeText={(text) => {
                  setConfirmPassword(text);
                  setErrors({ ...errors, confirmPassword: '' });
                }}
                autoCorrect={false}
              />
              <TouchableOpacity
                style={styles.icon1}
                onPress={() => setShowPassword(!showPassword)}
              >
                <Ionicons
                  name={showPassword ? 'eye-off' : 'eye'}
                  size={24}
                  color="#888"
                />
              </TouchableOpacity>
            </View>
            {errors.confirmPassword ? (
              <Text style={styles.errorText}>{errors.confirmPassword}</Text>
            ) : null}



            {/* Picker pour la fonction */}
            <View style={{ zIndex: 2000, marginBottom: 16 }}>
              <DropDownPicker
                open={openFonction}
                value={fonction}
                items={itemsFonction}
                setOpen={setOpenFonction}
                setValue={setFonction}
                setItems={setItemsFonction}
                placeholder="Veuillez sélectionner une fonction"
                style={[styles.dropdown, errors.fonction ? styles.inputError : null]}
                dropDownContainerStyle={styles.dropdownContainer}
                listMode="SCROLLVIEW"
                onOpen={() => setOpenAgence(false)}
              />
              {errors.fonction ? (
                <Text style={styles.errorText}>{errors.fonction}</Text>
              ) : null}
            </View>

            <TouchableOpacity
              style={styles.button}
              onPress={async () => {
                if (await validateForm()) {
                  try {
                    console.log('🚀 Envoi des données d\'enregistrement vers l\'API...');
                    
                    const registrationData = {
                      agence: agence,
                      nom: nom.trim(),
                      username: username.trim(),
                      telephone: telephone.trim(),
                      email: email.trim(),
                      password: password,
                      confirmPassword: confirmPassword,
                      fonction: fonction
                    };
                    
                    console.log('📤 Données envoyées:', { ...registrationData, password: '***', confirmPassword: '***' });
                    
                    const response = await fetch(`${API_BASE_URL}/api/register/`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                      },
                      body: JSON.stringify(registrationData),
                    });
                    
                    const data = await response.json();
                    console.log('📡 Réponse API enregistrement:', response.status, data);
                    
                    if (response.ok) {
                      // Stockage sécurisé du token pour connexion automatique
                      if (data.tokens) {
                        await SecureStore.setItemAsync('access_token', data.tokens.access);
                        await SecureStore.setItemAsync('refresh_token', data.tokens.refresh);
                        console.log('🔐 Tokens stockés avec succès');
                      }
                      
                      Alert.alert(
                        'Compte créé avec succès !',
                        `Bienvenue ${data.user.nom_complet}\n\nMatricule: ${data.employe.matricule}\nAgence: ${data.employe.agence}\nFonction: ${data.employe.fonction}\n\n${data.info}`,
                        [
                          {
                            text: 'Continuer',
                            onPress: () => {
                              console.log('✅ Redirection vers l\'écran de pointage');
                              router.push('/marquepresence');
                            },
                          },
                        ]
                      );
                    } else {
                      // Gestion des erreurs de validation
                      if (data.errors) {
                        console.log('❌ Erreurs de validation:', data.errors);
                        setErrors(prevErrors => ({ ...prevErrors, ...data.errors }));
                        
                        // Afficher la première erreur dans une alerte
                        const firstError = Object.values(data.errors)[0] as string;
                        Alert.alert('Erreur de validation', firstError);
                      } else {
                        Alert.alert('Erreur', data.error || 'Une erreur est survenue lors de la création du compte');
                      }
                    }
                  } catch (error) {
                    console.error('💥 Erreur réseau lors de l\'enregistrement:', error);
                    Alert.alert(
                      'Erreur de connexion',
                      'Impossible de se connecter au serveur. Vérifiez votre connexion internet et réessayez.'
                    );
                  }
                }
              }}
            >
              <Text style={styles.buttonText}>Valider</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push('/')}>
              <Text style={styles.link}>Déjà un compte ? Connexion</Text>
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
    justifyContent: 'flex-end',
  },
  logo: {
    width: '100%',
    height: 300,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginTop: 10,
  },
  container1: {
    flex: 1,
    width: '100%',
    backgroundColor: '#fff',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -3 },
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 10,
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
    marginBottom: 8,
    fontSize: 16,
  },
  inputError: {
    borderWidth: 1,
    borderColor: '#ff0000',
  },
  errorText: {
    color: '#ff0000',
    fontSize: 12,
    marginBottom: 8,
    marginLeft: 4,
  },
  successText: {
    color: '#28a745',
    fontSize: 12,
    marginBottom: 8,
    marginLeft: 4,
  },
  infoText: {
    color: '#6c757d',
    fontSize: 12,
    marginBottom: 8,
    marginLeft: 4,
  },
  icon1: {
    padding: 8,
    marginLeft: 8,
  },
  passwordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
    borderRadius: 10,
    marginBottom: 8,
    paddingHorizontal: 10,
  },
  passwordInput: {
    flex: 1,
    paddingVertical: 14,
    fontSize: 16,
    color: '#000',
  },
  icon: {
    padding: 8,
  },
  dropdown: {
    borderRadius: 10,
    backgroundColor: '#f0f0f0',
    borderWidth: 0,
  },
  dropdownContainer: {
    backgroundColor: '#f0f0f0',
    borderWidth: 0,
    borderRadius: 10,
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