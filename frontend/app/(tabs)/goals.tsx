import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Modal,
  TextInput,
  Alert,
  ScrollView,
} from 'react-native';
import api from '../../utils/api';
import { Goal } from '../../types';
import { Ionicons } from '@expo/vector-icons';
import { format } from 'date-fns';
import { it } from 'date-fns/locale';

export default function GoalsScreen() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [contributeModalVisible, setContributeModalVisible] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState<Goal | null>(null);
  const [name, setName] = useState('');
  const [targetAmount, setTargetAmount] = useState('');
  const [deadline, setDeadline] = useState('');
  const [contributeAmount, setContributeAmount] = useState('');

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = async () => {
    try {
      const response = await api.get('/goals');
      setGoals(response.data);
    } catch (error) {
      console.error('Error fetching goals:', error);
    } finally {
      setLoading(false);
    }
  };

  const addGoal = async () => {
    if (!name || !targetAmount || !deadline) {
      Alert.alert('Errore', 'Compila tutti i campi');
      return;
    }

    try {
      const deadlineDate = new Date(deadline);
      await api.post('/goals', {
        name,
        target_amount: parseFloat(targetAmount),
        deadline: deadlineDate.toISOString(),
      });
      setModalVisible(false);
      resetForm();
      fetchGoals();
    } catch (error) {
      Alert.alert('Errore', 'Impossibile creare l\'obiettivo');
    }
  };

  const contributeToGoal = async () => {
    if (!contributeAmount || !selectedGoal?.id) {
      Alert.alert('Errore', 'Inserisci un importo');
      return;
    }

    try {
      const amount = parseFloat(contributeAmount);
      await api.put(`/goals/${selectedGoal.id}/contribute?amount=${amount}`);
      setContributeModalVisible(false);
      setContributeAmount('');
      setSelectedGoal(null);
      fetchGoals();
    } catch (error) {
      Alert.alert('Errore', 'Impossibile aggiungere il contributo');
    }
  };

  const deleteGoal = async (id: string) => {
    Alert.alert(
      'Conferma',
      'Vuoi eliminare questo obiettivo?',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            try {
              await api.delete(`/goals/${id}`);
              fetchGoals();
            } catch (error) {
              Alert.alert('Errore', 'Impossibile eliminare l\'obiettivo');
            }
          },
        },
      ]
    );
  };

  const resetForm = () => {
    setName('');
    setTargetAmount('');
    setDeadline('');
  };

  const getProgressPercentage = (goal: Goal) => {
    return Math.min((goal.current_amount / goal.target_amount) * 100, 100);
  };

  const renderGoal = ({ item }: { item: Goal }) => {
    const percentage = getProgressPercentage(item);
    const isCompleted = percentage >= 100;

    return (
      <View style={[styles.goalCard, isCompleted && styles.goalCardCompleted]}>
        <View style={styles.goalHeader}>
          <View style={styles.goalInfo}>
            <Text style={styles.goalName}>{item.name}</Text>
            <Text style={styles.goalDeadline}>
              Scadenza: {format(new Date(item.deadline), 'dd MMM yyyy', { locale: it })}
            </Text>
          </View>
          <TouchableOpacity onPress={() => item.id && deleteGoal(item.id)}>
            <Ionicons name="trash-outline" size={20} color="#FF3B30" />
          </TouchableOpacity>
        </View>

        <View style={styles.goalAmount}>
          <Text style={styles.goalCurrent}>€{item.current_amount.toFixed(2)}</Text>
          <Text style={styles.goalTarget}> / €{item.target_amount.toFixed(2)}</Text>
        </View>

        <View style={styles.progressBarContainer}>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressBarFill,
                { width: `${percentage}%`, backgroundColor: isCompleted ? '#4CAF50' : '#007AFF' },
              ]}
            />
          </View>
          <Text style={[styles.progressText, { color: isCompleted ? '#4CAF50' : '#007AFF' }]}>
            {percentage.toFixed(0)}%
          </Text>
        </View>

        {isCompleted ? (
          <View style={styles.completedBanner}>
            <Ionicons name="checkmark-circle" size={20} color="#4CAF50" />
            <Text style={styles.completedText}>Obiettivo raggiunto!</Text>
          </View>
        ) : (
          <TouchableOpacity
            style={styles.contributeButton}
            onPress={() => {
              setSelectedGoal(item);
              setContributeModalVisible(true);
            }}
          >
            <Ionicons name="add-circle-outline" size={20} color="#007AFF" />
            <Text style={styles.contributeButtonText}>Aggiungi Contributo</Text>
          </TouchableOpacity>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={goals}
        renderItem={renderGoal}
        keyExtractor={(item) => item.id || Math.random().toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={fetchGoals}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="trophy-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>Nessun obiettivo</Text>
            <Text style={styles.emptySubtext}>Crea il tuo primo obiettivo di risparmio</Text>
          </View>
        }
      />

      <TouchableOpacity
        style={styles.fab}
        onPress={() => setModalVisible(true)}
      >
        <Ionicons name="add" size={32} color="#fff" />
      </TouchableOpacity>

      <Modal
        visible={modalVisible}
        animationType="slide"
        transparent
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Nuovo Obiettivo</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={28} color="#333" />
              </TouchableOpacity>
            </View>

            <ScrollView>
              <Text style={styles.label}>Nome Obiettivo</Text>
              <TextInput
                style={styles.input}
                placeholder="es. Vacanza estiva"
                value={name}
                onChangeText={setName}
              />

              <Text style={styles.label}>Importo Obiettivo</Text>
              <TextInput
                style={styles.input}
                placeholder="0.00"
                value={targetAmount}
                onChangeText={setTargetAmount}
                keyboardType="decimal-pad"
              />

              <Text style={styles.label}>Data Scadenza (YYYY-MM-DD)</Text>
              <TextInput
                style={styles.input}
                placeholder="2025-12-31"
                value={deadline}
                onChangeText={setDeadline}
              />

              <TouchableOpacity style={styles.addButton} onPress={addGoal}>
                <Text style={styles.addButtonText}>Crea Obiettivo</Text>
              </TouchableOpacity>
            </ScrollView>
          </View>
        </View>
      </Modal>

      <Modal
        visible={contributeModalVisible}
        animationType="slide"
        transparent
        onRequestClose={() => setContributeModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Aggiungi Contributo</Text>
              <TouchableOpacity onPress={() => setContributeModalVisible(false)}>
                <Ionicons name="close" size={28} color="#333" />
              </TouchableOpacity>
            </View>

            {selectedGoal && (
              <>
                <Text style={styles.selectedGoalName}>{selectedGoal.name}</Text>
                <Text style={styles.selectedGoalProgress}>
                  €{selectedGoal.current_amount.toFixed(2)} / €{selectedGoal.target_amount.toFixed(2)}
                </Text>
              </>
            )}

            <Text style={styles.label}>Importo</Text>
            <TextInput
              style={styles.input}
              placeholder="0.00"
              value={contributeAmount}
              onChangeText={setContributeAmount}
              keyboardType="decimal-pad"
            />

            <TouchableOpacity style={styles.addButton} onPress={contributeToGoal}>
              <Text style={styles.addButtonText}>Aggiungi Contributo</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  list: {
    padding: 16,
  },
  goalCard: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  goalCardCompleted: {
    borderWidth: 2,
    borderColor: '#4CAF50',
  },
  goalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  goalInfo: {
    flex: 1,
  },
  goalName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  goalDeadline: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  goalAmount: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 8,
  },
  goalCurrent: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  goalTarget: {
    fontSize: 16,
    color: '#666',
  },
  progressBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  progressBar: {
    flex: 1,
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
  },
  completedBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E8F5E9',
    padding: 8,
    borderRadius: 8,
    gap: 8,
  },
  completedText: {
    fontSize: 14,
    color: '#4CAF50',
    fontWeight: '600',
  },
  contributeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#E3F2FD',
  },
  contributeButtonText: {
    fontSize: 14,
    color: '#007AFF',
    fontWeight: '600',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 100,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#ccc',
    marginTop: 8,
    textAlign: 'center',
  },
  fab: {
    position: 'absolute',
    right: 16,
    bottom: 16,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 24,
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#f5f5f5',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
    marginBottom: 16,
  },
  addButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 8,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  selectedGoalName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  selectedGoalProgress: {
    fontSize: 16,
    color: '#666',
    marginBottom: 16,
  },
});