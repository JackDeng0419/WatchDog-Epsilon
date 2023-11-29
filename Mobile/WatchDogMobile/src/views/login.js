// src/views/login.js
import React, { useState, useContext, useEffect } from 'react';
import { View } from 'react-native';
import { Input, Button } from '@rneui/base';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faLock, faEnvelope } from '@fortawesome/free-solid-svg-icons';

import { SUCCESS_STATUS, ERROR_STATUS, loginUser, } from '../apis/serve-api';
import { Auth } from '../components/auth';
import Alert from '../components/alert';

import { loginStyles as styles } from '../asset/login-style';

const Login = ({ navigation }) => {
  const { setUserToken, userToken } = useContext(Auth); // 这里我们同时获取 setUserToken 和 userToken

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async () => {
    if (!email || !password) {
      setErrorMessage("Please fill in both email and password.");
      setShowError(true);
      return;
    }

    const response = await loginUser(email, password);
    if (response.status === SUCCESS_STATUS) {
      setUserToken(response.data.token);
    } else if (response.status === ERROR_STATUS) {
      setErrorMessage(response.data.message);
      setShowError(true);
    }
  };

  useEffect(() => {
    if (userToken) {
      navigation.reset({
        index: 0,
        routes: [{ name: 'Home' }],
      });
    }
  }, [userToken]);

  return (
    <View style={styles.container}>
      <Input
        placeholder="Email"
        leftIcon={<FontAwesomeIcon icon={faEnvelope} />}
        value={email}
        onChangeText={setEmail}
      />

      <Input
        placeholder='Password'
        leftIcon={<FontAwesomeIcon icon={faLock} />}
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <Button
        title="Login"
        onPress={handleLogin}
        containerStyle={styles.buttonContainer}
        disabled={!email || !password}
      />

      <Button
        title="Register"
        type="clear"
      />

      <Alert
        isVisible={showError}
        title="Login failed"
        body={errorMessage}
        positiveButton={{
          text: 'OK',
          backgroundColor: 'grey',
          onPress: () => setShowError(false)
        }}
      />
    </View>
  );
};

export default Login;
