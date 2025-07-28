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
console.log('🔧 Configuration API_BASE_URL utilisée:', API_BASE_URL);
console.log('🔧 Expo config disponible:', Constants.expoConfig?.extra?.API_BASE_URL);

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
      console.log('🔍 Headers de la requête:', {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      });
      const response = await fetch(`${API_BASE_URL}/api/roles/`);
      console.log('📡 Réponse API rôles:', response.status, response.statusText);
      console.log('📡 Content-Type reçu:', response.headers.get('content-type'));
      
      if (response.ok) {
        // Log du contenu de la réponse pour debug
        const responseText = await response.text();
        console.log('📡 Contenu de la réponse (premiers 200 chars):', responseText.substring(0, 200));
        
        try {
          const roles = JSON.parse(responseText);
          console.log('✅ Rôles récupérés:', roles.length, 'rôles');
          const formattedRoles = roles.map((role: any) => ({
            label: role.label,
            value: role.value
          }));
          setItemsFonction(formattedRoles);
          console.log('📝 Rôles formatés pour dropdown:', formattedRoles);
        } catch (parseError) {
          console.error('❌ Erreur de parsing JSON:', parseError);
          console.error('❌ Contenu reçu n\'est pas du JSON valide');
          // Fallback vers les données statiques
          setItemsFonction([
            { label: 'Directeur Général', value: 'Directeur Général' },
            { label: 'Responsable Informatique', value: 'Responsable Informatique' },
            { label: 'Secrétaire', value: 'Secrétaire' },
            { label: 'Comptable', value: 'Comptable' },
            { label: 'Agent Guichet', value: 'Agent Guichet' },
          ]);
        }
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
    // Validation d'email plus permissive pour Gmail et autres domaines
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const isValid = emailRegex.test(email);
    console.log('📧 Test validation email:', {
      email: email,
      regex: emailRegex.toString(),
      isValid: isValid
    });
    return isValid;
  };

  const validatePassword = (password: string) => {
    // Validation pour exactement 4 chiffres
    const passwordRegex = /^\d{4}$/;
    return passwordRegex.test(password);
  };

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

  // Génération de suggestions alternatives pour nom d'utilisateur
  const generateUsernameSuggestions = (baseUsername: string) => {
    const suggestions = [];
    const base = baseUsername.toUpperCase();
    
    // Suggestions avec numéros simples
    for (let i = 1; i <= 5; i++) {
      suggestions.push(`${base}${i}`);
    }
    
    // Suggestions avec numéros à deux chiffres
    for (let i = 1; i <= 3; i++) {
      const num = i.toString().padStart(2, '0');
      suggestions.push(`${base}${num}`);
    }
    
    // Suggestions avec année courante
    const currentYear = new Date().getFullYear();
    suggestions.push(`${base}${currentYear}`);
    suggestions.push(`${base}${currentYear.toString().slice(-2)}`);
    
    return suggestions;
  };

  // Vérification de la disponibilité du nom d'utilisateur avec suggestions
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
        body: JSON.stringify({ username: username.toUpperCase() }),
      });
      const data = await response.json();
      
      if (data.available) {
        setUsernameAvailable(true);
      } else {
        // Si le nom d'utilisateur n'est pas disponible, proposer des alternatives
        setUsernameAvailable(false);
        
        if (data.suggestions && data.suggestions.length > 0) {
          // Afficher les suggestions de l'API
          const suggestionText = data.suggestions.slice(0, 3).join(', ');
          Alert.alert(
            'Nom d\'utilisateur déjà utilisé',
            `Le nom "${username}" est déjà pris. Suggestions disponibles : ${suggestionText}`,
            [
              {
                text: 'Choisir un autre',
                style: 'cancel'
              },
              {
                text: 'Utiliser ' + data.suggestions[0].toUpperCase(),
                onPress: () => {
                  setUsername(data.suggestions[0].toUpperCase());
                  setUsernameAvailable(true);
                }
              }
            ]
          );
        } else {
          // Générer des suggestions localement si l'API n'en fournit pas
          const suggestions = generateUsernameSuggestions(username);
          const suggestionText = suggestions.slice(0, 3).join(', ');
          Alert.alert(
            'Nom d\'utilisateur déjà utilisé',
            `Le nom "${username}" est déjà pris. Suggestions : ${suggestionText}`,
            [
              {
                text: 'Choisir un autre',
                style: 'cancel'
              },
              {
                text: 'Utiliser ' + suggestions[0],
                onPress: () => {
                  setUsername(suggestions[0].toUpperCase());
                  setUsernameAvailable(true);
                }
              }
            ]
          );
        }
      }
    } catch (error) {
      console.error('Erreur lors de la vérification du nom d\'utilisateur:', error);
      setUsernameAvailable(null);
    } finally {
      setCheckingUsername(false);
    }
  };

  // Auto-suggestion désactivée - le champ nom d'utilisateur reste vide
  // useEffect(() => {
  //   if (nom.trim() && !username) {
  //     const suggested = suggestUsername(nom);
  //     setUsername(suggested);
  //     if (suggested) {
  //       checkUsernameAvailability(suggested);
  //     }
  //   }
  // }, [nom]);

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
    console.log('🔍 Début validation formulaire');
    console.log('📊 État des champs:', {
      agence, nom, username, telephone, email, password, confirmPassword, fonction,
      usernameAvailable
    });
    
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

    const trimmedNom = nom.trim();
    if (!trimmedNom) {
      newErrors.nom = 'Le nom complet est requis';
      isValid = false;
      console.log('❌ Nom complet vide');
    } else if (!validateNom(trimmedNom)) {
      newErrors.nom = 'Veuillez entrer votre nom et prénom (au moins 2 mots)';
      isValid = false;
      console.log('❌ Nom complet format invalide:', `"${nom}" -> "${trimmedNom}"`);
      // Corriger automatiquement l'espace
      setNom(trimmedNom);
    } else {
      console.log('✅ Nom complet valide:', trimmedNom);
    }
    

    const trimmedUsername = username.trim();
    if (!trimmedUsername) {
      newErrors.username = 'Le nom d\'utilisateur est requis';
      isValid = false;
      console.log('❌ Username vide');
    } else if (!validateUsername(trimmedUsername)) {
      newErrors.username = 'Le nom d\'utilisateur doit contenir 3-30 caractères (lettres, chiffres, _)';
      isValid = false;
      console.log('❌ Username format invalide:', `"${username}" -> "${trimmedUsername}"`);
      // Corriger automatiquement l'espace
      setUsername(trimmedUsername);
    } else if (usernameAvailable === false) {
      newErrors.username = 'Ce nom d\'utilisateur est déjà pris';
      isValid = false;
      console.log('❌ Username déjà pris');
    } else if (usernameAvailable === null) {
      newErrors.username = 'Vérification du nom d\'utilisateur en cours...';
      isValid = false;
      console.log('⏳ Username en cours de vérification');
    } else {
      console.log('✅ Username valide:', username);
    }

    if (!telephone.trim()) {
      newErrors.telephone = 'Le numéro de téléphone est requis';
      isValid = false;
    } else if (!validateTelephone(telephone)) {
      newErrors.telephone = 'Format de téléphone invalide (8-15 chiffres)';
      isValid = false;
    }

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      newErrors.email = "L'email est requis";
      isValid = false;
      console.log('❌ Email vide');
    } else if (!validateEmail(trimmedEmail)) {
      newErrors.email = "Format d'email invalide (exemple: nomprenom@domaine.com)";
      isValid = false;
      console.log('❌ Email format invalide:', `"${email}" -> "${trimmedEmail}"`);
      // Corriger automatiquement l'espace
      setEmail(trimmedEmail);
    } else {
      console.log('✅ Email valide:', trimmedEmail);
    }

    if (!password) {
      newErrors.password = 'Le mot de passe est requis';
      isValid = false;
    } else if (!validatePassword(password)) {
      newErrors.password = 'Le mot de passe doit contenir exactement 4 chiffres';
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
      console.log('❌ Fonction non sélectionnée');
    } else {
      console.log('✅ Fonction valide:', fonction);
    }
    
    console.log('🏁 Résultat validation:', isValid ? 'SUCCÈS' : 'ÉCHEC');
    console.log('🚨 Erreurs détectées:', newErrors);
    
    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      console.log('🚀 Tentative de création de compte via API:', `${API_BASE_URL}/api/register/`);
      
      const userData = {
        username: username.trim(),
        email: email.trim(),
        password: password,
        confirmPassword: confirmPassword,
        nom: nom.trim(), // Backend attend 'nom' pas 'nom_complet'
        telephone: telephone.trim(),
        agence: agence,
        fonction: fonction
      };
      
      console.log('📊 Données envoyées:', userData);
      
      const response = await fetch(`${API_BASE_URL}/api/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
      });
      
      console.log('📡 Réponse API:', response.status, response.statusText);
      
      if (response.ok) {
        const result = await response.json();
        console.log('✅ Compte créé avec succès:', result);
        
        // Afficher un message de succès puis rediriger automatiquement
        Alert.alert(
          'Compte créé avec succès', 
          'Votre compte a été créé. Vous allez être redirigé vers la page de connexion.',
          [
            { 
              text: 'OK', 
              onPress: () => {
                // Redirection automatique vers la page de connexion
                router.replace('/');
              }
            }
          ]
        );
      } else {
        const errorData = await response.json();
        console.error('❌ Erreur API:', errorData);
        
        // Afficher l'erreur spécifique de l'API
        const errorMessage = errorData.error || errorData.message || 'Une erreur est survenue lors de la création du compte.';
        Alert.alert('Erreur lors de la création du compte', errorMessage);
      }
    } catch (error) {
      console.error('❌ Erreur réseau:', error);
      Alert.alert('Erreur', 'Impossible de se connecter au serveur. Vérifiez votre connexion internet.');
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
                const upperText = text.toUpperCase();
                setNom(upperText);
                setErrors({ ...errors, nom: '' });
                // Note: Pas d'auto-suggestion du nom d'utilisateur
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
                const upperText = text.toUpperCase();
                setUsername(upperText);
                setErrors({ ...errors, username: '' });
              }}
              autoCorrect={false}
            />
            {errors.username && usernameAvailable !== true ? (
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
              onPress={() => {
                console.log('🔴 BOUTON CLIQUE - Début du processus');
                console.log('📊 État actuel des champs:', {
                  agence, nom, username, telephone, email, password, confirmPassword, fonction
                });
                console.log('🔄 Appel de handleSubmit...');
                handleSubmit();
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