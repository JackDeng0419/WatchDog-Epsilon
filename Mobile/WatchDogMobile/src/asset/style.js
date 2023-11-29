// src/asset/style.js
import { StyleSheet } from 'react-native';

export const commonStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 20,
  },
  label: {
    fontWeight: 'bold',
  },
  infoRow: {
    flexDirection: 'row',
    marginVertical: 10,
  },
  buttonContainer: {
    marginTop: 20,
  }
});
