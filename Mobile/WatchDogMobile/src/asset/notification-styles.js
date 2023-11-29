// src/asset/notification-styles.js
import { StyleSheet } from 'react-native';
import { commonStyles } from './style';

export const notificationStyles = StyleSheet.create({
  ...commonStyles,
  container: {
    ...commonStyles.container,
    alignItems: 'center',
  },
  label: {
    ...commonStyles.label,
    marginTop: 10,
  },
  infoText: {
    marginBottom: 20,
  },
  buttonContainer: {
    margin: 20,
    width: '80%',
  },
  linkText: {
    color: 'blue',
    textDecorationLine: 'underline',
  },
});
