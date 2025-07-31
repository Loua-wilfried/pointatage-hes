import * as SecureStore from 'expo-secure-store';
import React, { useState, useEffect, useLayoutEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert, Animated } from 'react-native';
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { router, useNavigation } from 'expo-router';
import { ArrowLeft, Camera, CircleAlert as AlertCircle, CheckCircle, XCircle } from 'lucide-react-native';
import Constants from 'expo-constants';

const API_BASE_URL = Constants.expoConfig?.extra?.API_BASE_URL || '';

export default function ScanScreen() {
  const navigation = useNavigation();
  
  // Configuration du header avec une approche plus stable
  React.useEffect(() => {
    const configureHeader = () => {
      navigation.setOptions({
        headerShown: true,
        title: "",
        headerStyle: {
          backgroundColor: '#fff',      // Couleur de fond du header
          shadowColor: '#fff',             // Couleur de l'ombre (iOS)
          shadowOffset: { height: 4 },     // Décalage vertical de l'ombre (iOS)
          shadowOpacity: 1,                // Opacité de l'ombre (iOS)
          shadowRadius: 8,                 // Flou de l'ombre (iOS)
          elevation: 10,                   // Ombre portée (Android)
          borderBottomWidth: 0,            // Masque la bordure du bas (iOS)
          borderBottomColor: "transparent", // Bordure du bas invisible
        },
        headerTitleStyle: { color: '#fff', fontWeight: 'bold', fontSize: 22 },
        headerTintColor: '#000',
        headerTitleAlign: 'center',
      });
    };
    
    // Délai léger pour éviter les conflits de timing
    const timer = setTimeout(configureHeader, 0);
    return () => clearTimeout(timer);
  }, [navigation]);

  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [scanned, setScanned] = useState(false);
  
  // États pour les messages temporaires
  const [showMessage, setShowMessage] = useState(false);
  const [messageType, setMessageType] = useState<'success' | 'error'>('success');
  const [messageText, setMessageText] = useState('');
  const fadeAnim = useState(new Animated.Value(0))[0];

  useEffect(() => {
    if (!permission?.granted) {
      requestPermission();
    }
  }, [permission]);

  // Fonction pour afficher un message temporaire
  const showTemporaryMessage = (type: 'success' | 'error', text: string) => {
    setMessageType(type);
    setMessageText(text);
    setShowMessage(true);
    
    // Animation d'apparition
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start();
    
    // Disparition automatique après 1 seconde
    setTimeout(() => {
      Animated.timing(fadeAnim, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }).start(() => {
        setShowMessage(false);
        // Redirection vers marquepresence dans TOUS les cas (succès ET erreur)
        router.replace('/marquepresence');
      });
    }, 1000);
  };

  const handleBarCodeScanned = async ({ type, data }: { type: string; data: string }) => {
    if (scanned) return;
    setScanned(true);

    let qrData;
    try {
      qrData = JSON.parse(data); // Le QR doit contenir un JSON
    } catch (e) {
      showTemporaryMessage('error', '❌ QR Code Invalide\nFormat non reconnu');
      return;
    }

    try {
      // Récupérer employe_id du stockage sécurisé après login
      const employe_id = await SecureStore.getItemAsync('employe_id');
      if (!employe_id) {
        showTemporaryMessage('error', '❌ Erreur\nImpossible de récupérer l\'identifiant employé');
        return;
      }
      
      const token = await SecureStore.getItemAsync('token');
      if (!token) {
        Alert.alert("Erreur", "Token d'authentification manquant. Veuillez vous reconnecter.", [
          { text: 'OK', onPress: () => router.replace('/') }
        ]);
        setScanned(false);
        return;
      }

      console.log('Token récupéré:', token.substring(0, 20) + '...');
      console.log('Données QR:', qrData);
      console.log('Employe ID:', employe_id);

      const response = await fetch(`${API_BASE_URL}/api/pointages/scan_qr_code/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          employe_id: employe_id,
          agence_id: qrData.agence_id,
          type: qrData.type
        }),
      });

      console.log('Statut de la réponse:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.log('Erreur de réponse:', errorText);
        
        let errorMessage = "Erreur lors de l'enregistrement";
        try {
          const errorJson = JSON.parse(errorText);
          errorMessage = errorJson.detail || errorJson.message || errorMessage;
        } catch (e) {
          errorMessage = errorText || errorMessage;
        }
        
        // Si c'est une erreur de token, rediriger vers la connexion
        if (response.status === 401 || errorMessage.includes('token')) {
          Alert.alert("Session expirée", "Votre session a expiré. Veuillez vous reconnecter.", [
            { text: 'OK', onPress: () => router.replace('/') }
          ]);
          return;
        }
        
        throw new Error(errorMessage);
      }

      const result = await response.json();
      console.log('Résultat du scan:', result);
      
      showTemporaryMessage('success', '✅ Pointage Réussi\nEnregistré avec succès!');
      
    } catch (err: any) {
      console.error('Erreur lors du scan:', err);
      
      // Extraire un message d'erreur plus lisible
      let errorMessage = err.message || "Impossible d'enregistrer le pointage";
      
      console.log('Message d\'erreur original:', errorMessage);
      
      // Gestion spéciale pour l'erreur de double pointage
      if (errorMessage.includes('déjà effectué un pointage')) {
        // Extraire le type de pointage (entree ou sortie)
        const match = errorMessage.match(/pointage '(\w+)'/); 
        const typePointage = match ? match[1] : 'pointage';
        const typeDisplay = typePointage === 'entree' ? 'entrée' : 'sortie';
        errorMessage = `⚠️ Pointage Déjà Effectué\nVous avez déjà fait votre ${typeDisplay} aujourd'hui`;
      } else if (errorMessage.includes('ErrorDetail')) {
        // Nettoyer les messages d'erreur du backend - amélioration de la regex
        const cleanMessage = errorMessage.replace(/\[ErrorDetail\(string="(.+?)", code='[^']*'\)\]/g, '$1');
        errorMessage = `❌ Erreur de Pointage\n${cleanMessage}`;
      } else {
        errorMessage = `❌ Erreur\n${errorMessage}`;
      }
      
      console.log('Message d\'erreur traité:', errorMessage);
      
      showTemporaryMessage('error', errorMessage);
    }
  };

  const handleGoBack = () => {
    router.back();
  };

  if (!permission) {
    return (
      <View style={styles.container}>
        <View style={styles.loadingContainer}>
          <Camera size={48} color="#6366f1" />
          <Text style={styles.loadingText}>Chargement de la caméra...</Text>
        </View>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <View style={styles.permissionContainer}>
          <AlertCircle size={64} color="#ef4444" strokeWidth={1.5} />
          <Text style={styles.permissionTitle}>Permission requise</Text>
          <Text style={styles.permissionText}>
            Nous avons besoin de votre permission pour accéder à la caméra
          </Text>
          <TouchableOpacity
            style={styles.permissionButton}
            onPress={requestPermission}
          >
            <Text style={styles.permissionButtonText}>Autoriser la caméra</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Scan QR Code</Text>
        <View style={styles.placeholder} />
      </View>

      <View style={styles.cameraContainer}>
        <CameraView
          style={styles.camera}
          facing={facing}
          onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
          barcodeScannerSettings={{
            barcodeTypes: ['qr'],
          }}
        >
          <View style={styles.overlay}>
            <View style={styles.scanArea}>
              <View style={[styles.corner, styles.topLeft]} />
              <View style={[styles.corner, styles.topRight]} />
              <View style={[styles.corner, styles.bottomLeft]} />
              <View style={[styles.corner, styles.bottomRight]} />
            </View>
          </View>
        </CameraView>
      </View>

      <View style={styles.footer}>
        <Text style={styles.instructionText}>
          Pointez la caméra vers un code QR
        </Text>
      </View>

      {/* Message temporaire */}
      {showMessage && (
        <Animated.View 
          style={[
            styles.messageContainer,
            {
              opacity: fadeAnim,
              backgroundColor: messageType === 'success' ? '#10b981' : '#ef4444'
            }
          ]}
        >
          <View style={styles.messageContent}>
            {messageType === 'success' ? (
              <CheckCircle size={24} color="white" strokeWidth={2} />
            ) : (
              <XCircle size={24} color="white" strokeWidth={2} />
            )}
            <Text style={styles.messageText}>{messageText}</Text>
          </View>
        </Animated.View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
  },
  loadingText: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 16,
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
    paddingHorizontal: 24,
  },
  permissionTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#1e293b',
    marginTop: 24,
    marginBottom: 12,
    textAlign: 'center',
  },
  permissionText: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
    maxWidth: 300,
  },
  permissionButton: {
    backgroundColor: '#6366f1',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 32,
    marginBottom: 16,
  },
  permissionButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingTop: 60,
    paddingBottom: 16,
    backgroundColor: '#fff',
  },

  headerTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000',
    position: 'relative',
    left: 120,
  },
  placeholder: {
    width: 60,
  },
  cameraContainer: {
    flex: 1,
    overflow: 'hidden',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scanArea: {
    width: 250,
    height: 250,
    position: 'relative',
  },
  corner: {
    position: 'absolute',
    width: 30,
    height: 30,
    borderColor: '#6366f1',
    borderWidth: 4,
  },
  topLeft: {
    top: 0,
    left: 0,
    borderRightWidth: 0,
    borderBottomWidth: 0,
  },
  topRight: {
    top: 0,
    right: 0,
    borderLeftWidth: 0,
    borderBottomWidth: 0,
  },
  bottomLeft: {
    bottom: 0,
    left: 0,
    borderRightWidth: 0,
    borderTopWidth: 0,
  },
  bottomRight: {
    bottom: 0,
    right: 0,
    borderLeftWidth: 0,
    borderTopWidth: 0,
  },
  footer: {
    backgroundColor: '#fff',
    paddingVertical: 20,
    paddingHorizontal: 24,
    alignItems: 'center',
  },
  instructionText: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
    marginBottom: 16,
  },
  scanAgainButton: {
    backgroundColor: '#6366f1',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 24,
  },
  scanAgainButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  messageContainer: {
    position: 'absolute',
    top: '40%',
    left: 20,
    right: 20,
    borderRadius: 12,
    paddingVertical: 20,
    paddingHorizontal: 24,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
    zIndex: 1000,
  },
  messageContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  messageText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 12,
    textAlign: 'center',
    lineHeight: 22,
  },
});