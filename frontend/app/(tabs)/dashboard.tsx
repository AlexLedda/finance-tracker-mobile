import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Dimensions,
  TouchableOpacity,
} from 'react-native';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../utils/api';
import { Stats } from '../../types';
import { BarChart, PieChart } from 'react-native-gifted-charts';
import { Ionicons } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryChartData = () => {
    if (!stats || !stats.category_expenses) return [];
    
    const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
    
    return Object.entries(stats.category_expenses).map(([category, amount], index) => ({
      value: amount,
      label: category,
      color: colors[index % colors.length],
    }));
  };

  const getIncomeExpenseData = () => {
    if (!stats) return [];
    
    return [
      { value: stats.recent_income, label: 'Entrate', frontColor: '#4CAF50' },
      { value: stats.recent_expenses, label: 'Uscite', frontColor: '#F44336' },
    ];
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={loading} onRefresh={fetchStats} />
      }
    >
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Ciao, {user?.name}!</Text>
          <Text style={styles.subtitle}>Ecco il tuo riepilogo finanziario</Text>
        </View>
        <TouchableOpacity onPress={logout} style={styles.logoutButton}>
          <Ionicons name="log-out-outline" size={24} color="#FF3B30" />
        </TouchableOpacity>
      </View>

      {stats && (
        <>
          <View style={styles.balanceCard}>
            <Text style={styles.balanceLabel}>Saldo Totale</Text>
            <Text style={[styles.balanceAmount, stats.balance >= 0 ? styles.positive : styles.negative]}>
              €{stats.balance.toFixed(2)}
            </Text>
            <View style={styles.balanceDetails}>
              <View style={styles.balanceItem}>
                <Ionicons name="arrow-up-circle" size={20} color="#4CAF50" />
                <Text style={styles.balanceItemText}>€{stats.total_income.toFixed(2)}</Text>
              </View>
              <View style={styles.balanceItem}>
                <Ionicons name="arrow-down-circle" size={20} color="#F44336" />
                <Text style={styles.balanceItemText}>€{stats.total_expenses.toFixed(2)}</Text>
              </View>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Ultimi 30 giorni</Text>
            <View style={styles.chartCard}>
              {getIncomeExpenseData().length > 0 && (
                <BarChart
                  data={getIncomeExpenseData()}
                  width={width - 80}
                  height={200}
                  barWidth={60}
                  spacing={40}
                  noOfSections={4}
                  yAxisThickness={0}
                  xAxisThickness={1}
                  xAxisColor="#e0e0e0"
                  yAxisTextStyle={{ color: '#666' }}
                  showGradient
                />
              )}
            </View>
          </View>

          {getCategoryChartData().length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Spese per Categoria</Text>
              <View style={styles.chartCard}>
                <PieChart
                  data={getCategoryChartData()}
                  radius={100}
                  showText
                  textColor="#000"
                  textSize={12}
                  showValuesAsLabels
                  labelsPosition="outward"
                />
                <View style={styles.legend}>
                  {getCategoryChartData().map((item, index) => (
                    <View key={index} style={styles.legendItem}>
                      <View style={[styles.legendColor, { backgroundColor: item.color }]} />
                      <Text style={styles.legendText}>
                        {item.label}: €{item.value.toFixed(2)}
                      </Text>
                    </View>
                  ))}
                </View>
              </View>
            </View>
          )}

          <View style={styles.statsGrid}>
            <View style={styles.statCard}>
              <Ionicons name="receipt-outline" size={32} color="#007AFF" />
              <Text style={styles.statValue}>{stats.transaction_count}</Text>
              <Text style={styles.statLabel}>Transazioni</Text>
            </View>
            <View style={styles.statCard}>
              <Ionicons name="trending-up" size={32} color="#4CAF50" />
              <Text style={styles.statValue}>€{stats.recent_income.toFixed(0)}</Text>
              <Text style={styles.statLabel}>Entrate (30gg)</Text>
            </View>
          </View>
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#fff',
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  logoutButton: {
    padding: 8,
  },
  balanceCard: {
    backgroundColor: '#007AFF',
    margin: 16,
    padding: 24,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  balanceLabel: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  balanceAmount: {
    fontSize: 40,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 8,
  },
  positive: {
    color: '#fff',
  },
  negative: {
    color: '#ffcccb',
  },
  balanceDetails: {
    flexDirection: 'row',
    marginTop: 16,
    gap: 24,
  },
  balanceItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  balanceItemText: {
    fontSize: 16,
    color: '#fff',
    fontWeight: '600',
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  chartCard: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  legend: {
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  legendColor: {
    width: 16,
    height: 16,
    borderRadius: 4,
    marginRight: 8,
  },
  legendText: {
    fontSize: 14,
    color: '#666',
  },
  statsGrid: {
    flexDirection: 'row',
    padding: 16,
    gap: 16,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
});