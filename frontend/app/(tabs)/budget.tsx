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
import { Budget } from '../../types';
import { Ionicons } from '@expo/vector-icons';
import { ProgressBar } from 'react-native';

const CATEGORIES = [
  'Alimentari',
  'Trasporti',
  'Intrattenimento',
  'Bollette',
  'Salute',
  'Shopping',
  'Altro',
];

const PERIODS = ['monthly', 'weekly'];

export default function BudgetScreen() {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [limit, setLimit] = useState('');
  const [period, setPeriod] = useState('monthly');

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    try {
      const response = await api.get('/budgets');
      setBudgets(response.data);
    } catch (error) {
      console.error('Error fetching budgets:', error);
    } finally {
      setLoading(false);
    }
  };

  const addBudget = async () => {
    if (!limit) {
      Alert.alert('Errore', 'Inserisci un limite di budget');
      return;
    }

    try {
      await api.post('/budgets', {
        category,
        limit: parseFloat(limit),
        period,
      });
      setModalVisible(false);
      resetForm();
      fetchBudgets();
    } catch (error: any) {
      Alert.alert('Errore', error.response?.data?.detail || 'Impossibile creare il budget');
    }
  };

  const deleteBudget = async (id: string) => {
    Alert.alert(
      'Conferma',
      'Vuoi eliminare questo budget?',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            try {
              await api.delete(`/budgets/${id}`);
              fetchBudgets();
            } catch (error) {
              Alert.alert('Errore', 'Impossibile eliminare il budget');
            }
          },
        },
      ]
    );
  };

  const resetForm = () => {
    setCategory(CATEGORIES[0]);
    setLimit('');
    setPeriod('monthly');
  };

  const getProgressPercentage = (budget: Budget) => {
    return Math.min((budget.spent / budget.limit) * 100, 100);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return '#F44336';
    if (percentage >= 70) return '#FF9800';
    return '#4CAF50';
  };

  const renderBudget = ({ item }: { item: Budget }) => {
    const percentage = getProgressPercentage(item);
    const color = getProgressColor(percentage);

    return (
      <View style={styles.budgetCard}>
        <View style={styles.budgetHeader}>
          <View style={styles.budgetInfo}>
            <Text style={styles.budgetCategory}>{item.category}</Text>
            <Text style={styles.budgetPeriod}>
              {item.period === 'monthly' ? 'Mensile' : 'Settimanale'}
            </Text>
          </View>
          <TouchableOpacity onPress={() => item.id && deleteBudget(item.id)}>
            <Ionicons name="trash-outline" size={20} color="#FF3B30" />
          </TouchableOpacity>
        </View>

        <View style={styles.budgetAmount}>
          <Text style={styles.budgetSpent}>€{item.spent.toFixed(2)}</Text>
          <Text style={styles.budgetLimit}> / €{item.limit.toFixed(2)}</Text>
        </View>

        <View style={styles.progressBarContainer}>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressBarFill,
                { width: `${percentage}%`, backgroundColor: color },
              ]}
            />
          </View>
          <Text style={[styles.progressText, { color }]}>{percentage.toFixed(0)}%</Text>
        </View>

        {percentage >= 90 && (
          <View style={styles.warningBanner}>
            <Ionicons name="warning" size={16} color="#F44336" />
            <Text style={styles.warningText}>Budget quasi esaurito!</Text>
          </View>
        )}
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={budgets}
        renderItem={renderBudget}
        keyExtractor={(item) => item.id || Math.random().toString()}
        contentContainerStyle={styles.list}
        refreshing={loading}
        onRefresh={fetchBudgets}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="wallet-outline" size={64} color="#ccc" />
            <Text style={styles.emptyText}>Nessun budget impostato</Text>
            <Text style={styles.emptySubtext}>Crea il tuo primo budget per monitorare le spese</Text>
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
              <Text style={styles.modalTitle}>Nuovo Budget</Text>
              <TouchableOpacity onPress={() => setModalVisible(false)}>
                <Ionicons name="close" size={28} color="#333" />
              </TouchableOpacity>
            </View>

            <ScrollView>
              <Text style={styles.label}>Categoria</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categoryScroll}>
                {CATEGORIES.map((cat) => (
                  <TouchableOpacity
                    key={cat}
                    style={[styles.categoryChip, category === cat && styles.categoryChipActive]}
                    onPress={() => setCategory(cat)}
                  >
                    <Text style={[styles.categoryChipText, category === cat && styles.categoryChipTextActive]}>
                      {cat}
                    </Text>
                  </TouchableOpacity>
                ))}
              </ScrollView>

              <Text style={styles.label}>Limite di Spesa</Text>
              <TextInput
                style={styles.input}
                placeholder="0.00"
                value={limit}
                onChangeText={setLimit}
                keyboardType="decimal-pad"
              />

              <Text style={styles.label}>Periodo</Text>
              <View style={styles.periodSelector}>
                <TouchableOpacity
                  style={[styles.periodButton, period === 'monthly' && styles.periodButtonActive]}
                  onPress={() => setPeriod('monthly')}
                >
                  <Text style={[styles.periodButtonText, period === 'monthly' && styles.periodButtonTextActive]}>
                    Mensile
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.periodButton, period === 'weekly' && styles.periodButtonActive]}
                  onPress={() => setPeriod('weekly')}
                >
                  <Text style={[styles.periodButtonText, period === 'weekly' && styles.periodButtonTextActive]}>
                    Settimanale
                  </Text>
                </TouchableOpacity>
              </View>

              <TouchableOpacity style={styles.addButton} onPress={addBudget}>
                <Text style={styles.addButtonText}>Crea Budget</Text>
              </TouchableOpacity>
            </ScrollView>
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
  budgetCard: {
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
  budgetHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  budgetInfo: {
    flex: 1,
  },
  budgetCategory: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  budgetPeriod: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  budgetAmount: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 8,
  },
  budgetSpent: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  budgetLimit: {
    fontSize: 16,
    color: '#666',
  },
  progressBarContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
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
  warningBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFEBEE',
    padding: 8,
    borderRadius: 8,
    marginTop: 12,
    gap: 8,
  },
  warningText: {
    fontSize: 12,
    color: '#F44336',
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
  categoryScroll: {
    marginBottom: 16,
  },
  categoryChip: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#f5f5f5',
    marginRight: 8,
  },
  categoryChipActive: {
    backgroundColor: '#007AFF',
  },
  categoryChipText: {
    fontSize: 14,
    color: '#666',
  },
  categoryChipTextActive: {
    color: '#fff',
    fontWeight: '600',
  },
  periodSelector: {
    flexDirection: 'row',
    marginBottom: 24,
    gap: 12,
  },
  periodButton: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    alignItems: 'center',
  },
  periodButtonActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  periodButtonText: {
    fontSize: 16,
    color: '#666',
  },
  periodButtonTextActive: {
    color: '#fff',
    fontWeight: '600',
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
});