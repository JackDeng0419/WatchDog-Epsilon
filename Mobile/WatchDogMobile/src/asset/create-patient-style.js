// src/asset/create-patient-style.js
import { StyleSheet } from 'react-native';
import { commonStyles } from './style';

export const createPatientStyles = StyleSheet.create({
  ...commonStyles,
  label: {
    ...commonStyles.label,
    marginTop: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 4,
    padding: 10,
    marginBottom: 15,
  },
});
