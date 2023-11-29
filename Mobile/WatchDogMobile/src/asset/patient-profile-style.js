// src/asset/patient-profile-style.js

import { StyleSheet } from 'react-native';
import { commonStyles } from './style';

export const patientProfileStyles = StyleSheet.create({
  ...commonStyles,
  label: {
    ...commonStyles.label,
    width: 100,
  },
  infoText: {
    flex: 1,
  },
  switchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
  },
});
