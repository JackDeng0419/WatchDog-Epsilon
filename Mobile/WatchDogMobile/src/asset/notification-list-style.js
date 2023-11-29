// src/asset/notification-list-style.js
import { StyleSheet } from 'react-native';
import { commonStyles } from '../asset/style';

export const notificationStyles = StyleSheet.create({
  ...commonStyles,
  infoRow: {
    ...commonStyles.infoRow,
    justifyContent: 'space-between',
  },
});