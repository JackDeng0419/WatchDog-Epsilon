// src/views/user-profile.js
import React, { useState, useContext } from 'react';
import { View, Text } from 'react-native';
import { Button, Card } from '@rneui/base';

import { SUCCESS_STATUS, logoutUser } from '../apis/serve-api';
import AppHeader from '../components/header';
import { Auth } from '../components/auth';

import { userProfileStyles as styles } from '../asset/user-profile-styles';

const UserProfile = ({ navigation }) => {
  const [username, setUsername] = useState('JohnDoe123');
  const [role, setRole] = useState('Admin');

  const { setUserToken } = useContext(Auth);

  const handleLogout = async () => {
    const response = await logoutUser();
    if (response.status === SUCCESS_STATUS) {
      setUserToken(null);
      navigation.navigate('Login');
    }
  };

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />

      <Card containerStyle={styles.card}>
        <Card.Title>User Profile</Card.Title>
        <Card.Divider />
        <View style={styles.infoRow}>
          <Text style={styles.label}>Username:</Text>
          <Text style={styles.infoText}>{username}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.label}>Role:</Text>
          <Text style={styles.infoText}>{role}</Text>
        </View>
      </Card>

      <Card containerStyle={styles.card}>
        <Button
          title="Logout"
          color="red"
          onPress={handleLogout}
          containerStyle={styles.buttonContainer}
        />
      </Card>
    </View>
  );
};

export default UserProfile;
