import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface HeaderProps {
  title?: string;
}

export default function Header({ title = "" }: HeaderProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F0874E',
    paddingVertical: 16,
    paddingHorizontal: 20,
    alignItems: 'center',
  },
  title: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});