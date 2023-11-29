// src/asset/patient-list-style.js
import { StyleSheet } from 'react-native';
import { commonStyles } from './style';

export const patientListStyles = StyleSheet.create({
  ...commonStyles,
  infoRow: {
    ...commonStyles.infoRow,
    justifyContent: 'space-between',
  },
  enabled: {
    color: 'green',
  },
  disabled: {
    color: 'gray',
  },
  warning: {
    color: 'red',
  },
});
