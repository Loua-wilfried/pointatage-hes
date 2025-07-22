import { router } from "expo-router";
import React from "react";
import { View, Text, TouchableOpacity, StyleSheet, Dimensions } from "react-native";
import { useNavigation } from 'expo-router';
import { useLayoutEffect } from 'react';

const { width } = Dimensions.get('window');

export default function MarquePresence() {
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

    return (
        <View style={styles.container}>
            {/* Header moderne */}
            <View style={styles.header}>
                <Text style={styles.headerTitle}>MARQUE-PRÉSENCE MR/MDE</Text>
                <View style={styles.headerLine} />
            </View>

            {/* Carte Arrivée */}
            <View style={[styles.card, styles.shadowElevation]}>
                <View style={styles.cardHeader}>
                    <View style={[styles.cardBadge, styles.arrivalBadge]}>
                        <Text style={styles.badgeText}>ARRIVÉE</Text>
                    </View>
                    <View style={styles.timeIndicator}>
                        <Text style={styles.timeText}>08:00 - 12:00</Text>
                    </View>
                </View>
                
                <View style={styles.buttonGroup}>
                    <TouchableOpacity 
                        style={[styles.button, styles.scanButton]} 
                        onPress={() => router.push('/scan')}
                    >
                        <Text style={styles.buttonText}>SCANNER QR CODE</Text>
                    </TouchableOpacity>
                    <TouchableOpacity 
                        style={[styles.button, styles.geoButton]} 
                        onPress={() => router.push('/')}
                    >
                        <Text style={styles.buttonText}>GÉOLOCALISATION</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* Carte Départ */}
            <View style={[styles.card, styles.shadowElevation, {marginTop: 30}]}>
                <View style={styles.cardHeader}>
                    <View style={[styles.cardBadge, styles.departureBadge]}>
                        <Text style={styles.badgeText}>DÉPART</Text>
                    </View>
                    <View style={styles.timeIndicator}>
                        <Text style={styles.timeText}>13:00 - 17:00</Text>
                    </View>
                </View>
                
                <View style={styles.buttonGroup}>
                    <TouchableOpacity 
                        style={[styles.button, styles.scanButton]} 
                        onPress={() => router.push('/scan')}
                    >
                        <Text style={styles.buttonText}>SCANNER QR CODE</Text>
                    </TouchableOpacity>
                    <TouchableOpacity 
                        style={[styles.button, styles.geoButton]} 
                        onPress={() => router.push('/')}
                    >
                        <Text style={styles.buttonText}>GÉOLOCALISATION</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* Footer discret */}
            <View style={styles.footer}>
                <Text style={styles.footerText}>V.1.0 • ©2025 HES-FINANCE</Text>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8f8f8',
        paddingHorizontal: 25,
        paddingTop: 40,
    },
    header: {
        marginBottom: 35,
        alignItems: 'center',
    },
    headerTitle: {
        fontSize: 16,
        fontWeight: '800',
        color: '#000',
        letterSpacing: 1.8,
        textTransform: 'uppercase',
    },
    headerLine: {
        height: 4,
        width: width * 0.3,
        backgroundColor: '#FF6D00',
        marginTop: 10,
        borderRadius: 2,
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 16,
        padding: 25,
        borderWidth: 1,
        borderColor: '#e0e0e0',
    },
    shadowElevation: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.1,
        shadowRadius: 15,
        elevation: 8,
    },
    cardHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 25,
    },
    cardBadge: {
        paddingVertical: 8,
        paddingHorizontal: 20,
        borderRadius: 20,
    },
    arrivalBadge: {
        backgroundColor: 'rgba(255,109,0,0.15)',
        borderWidth: 1.5,
        borderColor: '#FF6D00',
    },
    departureBadge: {
        backgroundColor: 'rgba(0,0,0,0.08)',
        borderWidth: 1.5,
        borderColor: '#000',
    },
    badgeText: {
        fontSize: 14,
        fontWeight: '700',
        letterSpacing: 1,
    },
    timeIndicator: {
        backgroundColor: '#f0f0f0',
        paddingVertical: 6,
        paddingHorizontal: 12,
        borderRadius: 12,
    },
    timeText: {
        fontSize: 12,
        fontWeight: '600',
        color: '#555',
    },
    buttonGroup: {
        width: '100%',
    },
    button: {
        paddingVertical: 16,
        borderRadius: 12,
        width: '100%',
        alignItems: 'center',
        marginBottom: 12,
        flexDirection: 'row',
        justifyContent: 'center',
    },
    scanButton: {
        backgroundColor: '#FF6D00',
    },
    geoButton: {
        backgroundColor: '#000',
    },
    buttonText: {
        color: '#fff',
        fontSize: 15,
        fontWeight: '700',
        letterSpacing: 0.5,
    },
    footer: {
        marginTop: 40,
        alignItems: 'center',
    },
    footerText: {
        fontSize: 11,
        color: '#999',
        letterSpacing: 0.5,
    },
});