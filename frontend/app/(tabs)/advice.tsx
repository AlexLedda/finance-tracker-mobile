import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
} from 'react-native';
import api from '../../utils/api';
import { Ionicons } from '@expo/vector-icons';

export default function AdviceScreen() {
  const [advice, setAdvice] = useState('');
  const [loading, setLoading] = useState(false);
  const [context, setContext] = useState('');

  const getAdvice = async () => {
    setLoading(true);
    try {
      const response = await api.post('/advice', { context });
      setAdvice(response.data.advice);
    } catch (error) {
      console.error('Error getting advice:', error);
      setAdvice('Errore nel recupero dei consigli. Riprova più tardi.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Ionicons name="bulb" size={48} color="#FF9500" />
        <Text style={styles.headerTitle}>Consigli AI</Text>
        <Text style={styles.headerSubtitle}>
          Ricevi consigli personalizzati basati sulle tue finanze
        </Text>
      </View>

      <View style={styles.inputCard}>
        <Text style={styles.label}>Domanda specifica (opzionale)</Text>
        <TextInput
          style={styles.textArea}
          placeholder="es. Come posso risparmiare di più?"
          value={context}
          onChangeText={setContext}
          multiline
          numberOfLines={3}
        />
        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={getAdvice}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <>
              <Ionicons name="sparkles" size={20} color="#fff" />
              <Text style={styles.buttonText}>Ottieni Consigli</Text>
            </>
          )}
        </TouchableOpacity>
      </View>

      {advice && (
        <View style={styles.adviceCard}>
          <View style={styles.adviceHeader}>
            <Ionicons name="chatbubbles" size={24} color="#007AFF" />
            <Text style={styles.adviceTitle}>I tuoi consigli personalizzati</Text>
          </View>
          <Text style={styles.adviceText}>{advice}</Text>
        </View>
      )}

      <View style={styles.tipCard}>
        <Ionicons name="information-circle" size={24} color="#007AFF" />
        <View style={styles.tipContent}>
          <Text style={styles.tipTitle}>Come funziona?</Text>
          <Text style={styles.tipText}>
            L'AI analizza le tue transazioni, budget e obiettivi per fornirti consigli personalizzati.
            Puoi anche fare domande specifiche per ricevere suggerimenti mirati.
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#fff',
    padding: 24,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 12,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
    textAlign: 'center',
  },
  inputCard: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  textArea: {
    backgroundColor: '#f5f5f5',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    marginBottom: 16,
    minHeight: 80,
    textAlignVertical: 'top',
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  adviceCard: {
    backgroundColor: '#fff',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  adviceHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 8,
  },
  adviceTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  adviceText: {
    fontSize: 16,
    color: '#333',
    lineHeight: 24,
  },
  tipCard: {
    backgroundColor: '#E3F2FD',
    margin: 16,
    marginTop: 0,
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    gap: 12,
  },
  tipContent: {
    flex: 1,
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
    marginBottom: 4,
  },
  tipText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
});