// src/asset/login-style.js
import { StyleSheet } from 'react-native';
import { commonStyles } from './style';

export const loginStyles = StyleSheet.create({
  container: {
    ...commonStyles.container,
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  buttonContainer: {
    marginVertical: 10,
  },
});
