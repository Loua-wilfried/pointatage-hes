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
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import DropDownPicker from 'react-native-dropdown-picker';
import { useNavigation } from 'expo-router';
import { useLayoutEffect } from 'react';

const API_BASE_URL = Constants.expoConfig.extra.API_BASE_URL;

export default function CreationCompte() {
  const [nom, setNom] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [numero, setNumero] = useState('');
  const [errors, setErrors] = useState({
    nom: '',
    email: '',
    password: '',
    confirmPassword: '',
    fonction: '',
    agence: '',
    numero: '',
    nomUtilisateur: '', // Ajouté
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

  // Picker pour la fonction
  const [openFonction, setOpenFonction] = useState(false);
  const [fonction, setFonction] = useState(null);
  const [itemsFonction, setItemsFonction] = useState([
    { label: 'Directeur Général', value: 'Directeur Général' },
    { label: 'Responsable Informatique', value: 'Responsable Informatique' },
  ]);

  // Picker pour l'agence
  const [openAgence, setOpenAgence] = useState(false);
  const [agence, setAgence] = useState(null);
  const [itemsAgence, setItemsAgence] = useState([
    { label: 'Agence1', value: 'Agence Principale' },
  ]);

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

  const [nomUtilisateur, setNomUtilisateur] = useState('');

  const validateForm = () => {
    let isValid = true;
    const newErrors = {
      nom: '',
      email: '',
      password: '',
      confirmPassword: '',
      fonction: '',
      agence: '',
      numero: '',
      nomUtilisateur: '', // Ajouté
    };

    if (!nom.trim()) {
      newErrors.nom = 'Le nom est requis';
      isValid = false;
    } else if (!validateNom(nom)) {
      newErrors.nom = 'Veuillez entrer votre nom et prénom (au moins 2 mots)';
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

    if (!agence) {
      newErrors.agence = 'Veuillez sélectionner une agence';
      isValid = false;
    }

    if (!numero || numero.length !== 10) {
      newErrors.numero = 'Le numéro doit contenir exactement 10 chiffres';
      isValid = false;
    }

    if (!nomUtilisateur.trim()) {
      newErrors.nomUtilisateur = "Le nom d'utilisateur est requis";
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
              style={[styles.input, errors.nomUtilisateur ? styles.inputError : null]}
              placeholder="Nom d'utilisateur"
              placeholderTextColor="#888"
              value={nomUtilisateur}
              onChangeText={text => {
                setNomUtilisateur(text);
                setErrors({ ...errors, nomUtilisateur: '' });
              }}
              autoCapitalize="none"
              autoCorrect={false}
            />
            {errors.nomUtilisateur ? (
              <Text style={styles.errorText}>{errors.nomUtilisateur}</Text>
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

            <TextInput
              style={[styles.input, errors.numero ? styles.inputError : null]}
              placeholder="numéro"
              placeholderTextColor="#888"
              autoCapitalize="none"
              keyboardType="numeric"
              maxLength={10}
              value={numero}
              onChangeText={text => {
                const onlyNums = text.replace(/[^0-9]/g, '');
                setNumero(onlyNums);
                setErrors({ ...errors, numero: '' });
              }}
            />
            {errors.numero ? (
              <Text style={styles.errorText}>{errors.numero}</Text>
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
                    // Envoi vers API ici si nécessaire
                    Alert.alert('Succès', 'Compte créé avec succès', [
                      {
                        text: 'OK',
                        onPress: () => router.push('/marquepresence'),
                      },
                    ]);
                  } catch (error) {
                    Alert.alert(
                      'Erreur',
                      'Une erreur est survenue lors de la création du compte. Veuillez réessayer.'
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